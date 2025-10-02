# actions/actions.py
import json
import os
import re
import unicodedata
from typing import Any, Text, Dict, List, Tuple, Optional
from difflib import SequenceMatcher

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# ========= CONFIG =========
JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "arbol_decision_limpio.json")

MAPA_PROCESOS = {
    "1": "Cáncer de mama",
    "2": "Mama benigna",
    "3": "Cáncer de endometrio",
    "4": "Cáncer de ovario",
    "5": "Cáncer de cérvix",
    "6": "Cáncer de vulva",
    "7": "Cirugía abdominal",
    "8": "Conización",
    "9": "Histeroscopia",
}

UMBRAL_COINCIDENCIA_ALTA = 0.88
UMBRAL_COINCIDENCIA_MEDIA = 0.74

with open(JSON_PATH, "r", encoding="utf-8") as f:
    ARBOL = json.load(f)

# Estado simple (para un único chat en pruebas). En producción: usar slots.
proceso_actual: Optional[str] = None
tema_actual: Optional[str] = None

# ========= Helpers =========
def limpiar(texto: str) -> str:
    if texto is None:
        return ""
    texto = str(texto)
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = "\n".join(line.strip() for line in texto.split("\n"))
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = unicodedata.normalize("NFD", texto).lower().strip()
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def es_codigo_numerico(texto: str) -> bool:
    return bool(re.fullmatch(r"\d+(?:\.\d+)*", texto.strip()))

def prefijo_numerico(clave: str) -> str:
    m = re.match(r"^(\d+(?:\.\d+)*)(?:\s+|$)", clave.strip())
    return m.group(1) if m else ""

def ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, limpiar(a), limpiar(b)).ratio()

def mejor_coincidencia(usuario: str, claves: List[str]) -> Tuple[Optional[str], float]:
    if not claves:
        return None, 0.0
    u = usuario.strip()
    u_clean = limpiar(u)

    # match por número exacto
    if es_codigo_numerico(u):
        for k in claves:
            if prefijo_numerico(k).lower() == u.lower():
                return k, 1.0

    # inclusión de texto
    cand = []
    for k in claves:
        k_clean = limpiar(k)
        if u_clean and (u_clean in k_clean or k_clean in u_clean):
            cand.append((k, 0.92))
    if cand:
        cand.sort(key=lambda x: (ratio(u, x[0]), len(x[0])), reverse=True)
        return cand[0]

    # fuzzy general
    mejor = (None, 0.0)
    for k in claves:
        r = ratio(u, k)
        if r > mejor[1]:
            mejor = (k, r)
    return mejor

def listar_opciones(diccionario: Dict[str, Any]) -> str:
    return "\n".join([f"🔹 {k}" for k in diccionario.keys()])

def flatten_text(valor: Any) -> str:
    """
    Convierte cualquier rama (strings y dicts anidados) en texto plano.
    - No pone "Opción 1/2".
    - Si hay dicts {"1": "...", "2": "..."} saca sus valores en líneas separadas.
    - Mantiene el orden por clave, y respeta el enunciado seguido de SI/NO.
    """
    if isinstance(valor, str):
        return valor
    if isinstance(valor, dict):
        partes: List[str] = []
        for k in sorted(valor.keys(), key=lambda x: [int(t) if t.isdigit() else 9999 for t in re.split(r"\D+", str(x)) if t != ""]):
            partes.append(flatten_text(valor[k]))
        return "\n\n".join([p for p in partes if p])
    return str(valor)

def asegurar_proceso(proceso_texto: str) -> Optional[str]:
    global proceso_actual
    t = proceso_texto.strip()
    if t in MAPA_PROCESOS:
        nombre = MAPA_PROCESOS[t]
        mejor, _ = mejor_coincidencia(nombre, list(ARBOL.keys()))
        if mejor:
            proceso_actual = mejor
            return mejor
    mejor, sc = mejor_coincidencia(t, list(ARBOL.keys()))
    if mejor and sc >= UMBRAL_COINCIDENCIA_MEDIA:
        proceso_actual = mejor
        return mejor
    return None

def asegurar_tema(tema_texto: str) -> Optional[str]:
    global tema_actual, proceso_actual
    if not proceso_actual:
        return None
    temas = ARBOL.get(proceso_actual, {})
    if not isinstance(temas, dict):
        return None
    claves = list(temas.keys())
    mejor, sc = mejor_coincidencia(tema_texto, claves)
    if mejor and (sc >= UMBRAL_COINCIDENCIA_ALTA or es_codigo_numerico(tema_texto) or sc >= UMBRAL_COINCIDENCIA_MEDIA):
        tema_actual = mejor
        return mejor
    return None

def buscar_pregunta(texto: str) -> Optional[Tuple[str, Any]]:
    global proceso_actual, tema_actual
    if not proceso_actual:
        return None

    def _buscar_en(dic: Dict[str, Any], texto_busqueda: str) -> Optional[Tuple[str, Any]]:
        claves = list(dic.keys())
        mejor, sc = mejor_coincidencia(texto_busqueda, claves)
        if mejor and (sc >= UMBRAL_COINCIDENCIA_ALTA or es_codigo_numerico(texto_busqueda) or sc >= UMBRAL_COINCIDENCIA_MEDIA):
            return mejor, dic[mejor]
        return None

    temas = ARBOL.get(proceso_actual, {})
    # 1) Buscar dentro del tema actual
    if tema_actual and isinstance(temas.get(tema_actual, None), dict):
        res = _buscar_en(temas[tema_actual], texto)
        if res:
            return res
    # 2) Buscar en todos los temas del proceso
    for t, sub in temas.items():
        if isinstance(sub, dict):
            res = _buscar_en(sub, texto)
            if res:
                tema_actual = t
                return res
    return None

def texto_menu_principal() -> str:
    return (
        "🏠 Menú principal:\n\n"
        "1️⃣ Cáncer de mama\n"
        "2️⃣ Mama benigna\n"
        "3️⃣ Cáncer de endometrio\n"
        "4️⃣ Cáncer de ovario\n"
        "5️⃣ Cáncer de cérvix\n"
        "6️⃣ Cáncer de vulva\n"
        "7️⃣ Cirugía abdominal\n"
        "8️⃣ Conización\n"
        "9️⃣ Histeroscopia\n\n"
        "✍️ Escribe el número o el nombre del proceso."
    )

# ========= Actions =========
class ActionMostrarTemas(Action):
    def name(self) -> Text:
        return "action_mostrar_temas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global proceso_actual, tema_actual
        tema_actual = None

        texto_usuario = tracker.latest_message.get("text", "").strip()

        # Caso directo 1.2 -> detecta proceso 1 y también intenta fijar tema
        if es_codigo_numerico(texto_usuario) and "." in texto_usuario:
            proc_num = texto_usuario.split(".", 1)[0]
            if asegurar_proceso(proc_num):
                asegurar_tema(texto_usuario)
                if tema_actual:
                    sub = ARBOL[proceso_actual][tema_actual]
                    msg = (
                        f"📁 Has seleccionado: {tema_actual}\n\n"
                        f"Preguntas disponibles:\n{listar_opciones(sub)}\n\n"
                        f"✍️ Escribe el número (p.ej. 1.1.1) o el enunciado."
                    )
                    dispatcher.utter_message(text=msg)
                    return []
            else:
                dispatcher.utter_message(text="⚠️ No encontré ese proceso. Prueba con el nombre o número 1–9.")
                return []

        if asegurar_proceso(texto_usuario):
            temas = ARBOL[proceso_actual]
            if isinstance(temas, dict) and temas:
                msg = (
                    f"📂 Has seleccionado: {proceso_actual}\n\n"
                    f"Temas:\n{listar_opciones(temas)}\n\n"
                    f"✍️ Escribe el número (p.ej. 1.1) o el nombre del tema."
                )
                dispatcher.utter_message(text=msg)
                return []
            else:
                dispatcher.utter_message(text="ℹ️ No hay temas definidos en este proceso.")
                return []

        dispatcher.utter_message(text="⚠️ No encontré ese proceso.\n\n" + texto_menu_principal())
        return []

class ActionMostrarSubtemas(Action):
    def name(self) -> Text:
        return "action_mostrar_subtemas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global proceso_actual, tema_actual

        if not proceso_actual:
            dispatcher.utter_message(text="⚠️ Primero elige un proceso.\n\n" + texto_menu_principal())
            return []

        texto_usuario = tracker.latest_message.get("text", "").strip()

        # Si viene 1.2.3, intentar saltar directo a pregunta
        if es_codigo_numerico(texto_usuario) and texto_usuario.count(".") >= 2:
            proc_num = texto_usuario.split(".", 1)[0]
            asegurar_proceso(proc_num)
            asegurar_tema(".".join(texto_usuario.split(".")[:2]))
            encontrado = buscar_pregunta(texto_usuario)
            if encontrado:
                _, val = encontrado
                dispatcher.utter_message(text=flatten_text(val))
                return []

        if asegurar_tema(texto_usuario):
            sub = ARBOL[proceso_actual][tema_actual]
            if isinstance(sub, dict) and sub:
                msg = (
                    f"📁 Has seleccionado: {tema_actual}\n\n"
                    f"Preguntas:\n{listar_opciones(sub)}\n\n"
                    f"✍️ Escribe el número (p.ej. 1.1.1) o el enunciado de la pregunta."
                )
                dispatcher.utter_message(text=msg)
                return []
            else:
                dispatcher.utter_message(text="ℹ️ No hay subtemas/preguntas en este tema.")
                return []

        dispatcher.utter_message(text="⚠️ No encontré ese tema. Escribe p.ej. 1.1 o un nombre aproximado.")
        return []

class ActionMostrarContenido(Action):
    def name(self) -> Text:
        return "action_mostrar_contenido"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global proceso_actual, tema_actual

        if not proceso_actual:
            dispatcher.utter_message(text="⚠️ Primero elige un proceso.\n\n" + texto_menu_principal())
            return []

        texto_usuario = tracker.latest_message.get("text", "").strip()

        encontrado = buscar_pregunta(texto_usuario)
        if encontrado:
            _, val = encontrado
            dispatcher.utter_message(text=flatten_text(val))
            if tema_actual and proceso_actual:
                dispatcher.utter_message(
                    text=f"↩️ ¿Quieres otra pregunta de **{tema_actual}** o volver al menú?\n"
                         f"- Escribe otro número/enunciado\n- O escribe **volver**"
                )
            return []

        dispatcher.utter_message(text="⚠️ No encontré esa pregunta. Prueba con el número exacto (p.ej. 1.1.1) o parte del enunciado.")
        return []

class ActionVolverMenu(Action):
    def name(self) -> Text:
        return "action_volver_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global proceso_actual, tema_actual
        proceso_actual = None
        tema_actual = None
        dispatcher.utter_message(text=texto_menu_principal())
        return []
