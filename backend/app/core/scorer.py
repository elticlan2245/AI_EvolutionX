import re
from typing import Optional


def score_conversation(user_message: str, assistant_message: str) -> float:
    """
    Evalúa la calidad de una conversación entre el usuario y el asistente.

    Parámetros:
        user_message (str): mensaje del usuario.
        assistant_message (str): respuesta del asistente.

    Retorna:
        float: puntuación entre 0.0 y 1.0.
    """

    # Limpieza básica
    user_message = (user_message or "").strip()
    assistant_message = (assistant_message or "").strip()

    # Si la respuesta está vacía, score 0
    if not assistant_message:
        return 0.0

    score = 0.0

    # 1️⃣ Longitud adecuada
    msg_len = len(assistant_message)
    if 50 < msg_len < 2000:
        score += 0.25
    elif msg_len > 2000:
        score += 0.1  # demasiado larga, pero aún válida
    elif msg_len > 20:
        score += 0.1  # corta, pero no vacía

    # 2️⃣ Inclusión de código o estructura técnica
    if any(kw in assistant_message for kw in ["```", "def ", "class ", "import "]):
        score += 0.2

    # 3️⃣ Estructura clara (viñetas, subtítulos, secciones)
    if any(marker in assistant_message for marker in ['- ', '* ', '1.', '##', '**']):
        score += 0.15

    # 4️⃣ Detalle o profundidad (líneas múltiples)
    num_lines = len(assistant_message.splitlines())
    if num_lines > 5:
        score += 0.15
    if num_lines > 15:
        score += 0.05  # aún más detallado

    # 5️⃣ Calidad del mensaje del usuario
    if len(user_message) > 15:
        score += 0.1

    # 6️⃣ Coherencia básica: tiene signos de puntuación o pregunta
    if re.search(r"[.,;!?]", assistant_message):
        score += 0.05

    # 7️⃣ Bonus si contiene emojis o tono humano
    if re.search(r"[😀🙂😉🤔👍🙏❤️]", assistant_message):
        score += 0.05

    # Normalización del puntaje
    score = min(1.0, round(score, 2))
    return score
