import re

HIGH_IMPORTANCE_KEYWORDS = [
    "matou", "assassinou", "guerra", "roubou", "traiu", "morreu", 
    "aliança", "coroado", "rei", "princesa", "capitão", "incêndio", 
    "artefato", "derrota", "vitória", "revolução", "praga"
]

MEDIUM_IMPORTANCE_KEYWORDS = [
    "negociou", "comprou", "prometeu", "ajudou", "recompensou", 
    "explorou", "encontrou", "guarda", "tábua", "segredo"
]

def calculate_importance(event_text: str) -> float:
    text_lower = event_text.lower()
    score = 0.3  # Base default importance score
    
    for kw in HIGH_IMPORTANCE_KEYWORDS:
        if kw in text_lower:
            score += 0.25
            
    for kw in MEDIUM_IMPORTANCE_KEYWORDS:
        if kw in text_lower:
            score += 0.1
            
    # Clamp score between 0.1 and 1.0
    return min(1.0, max(0.1, round(score, 2)))
