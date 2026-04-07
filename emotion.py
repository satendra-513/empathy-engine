"""
emotion.py – Granular Emotion Detection with Intensity Scaling
Uses VADER (rule-based, great for short text) as the primary engine,
augmented with keyword heuristics for nuanced emotion categories.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

# ─── Keyword hint maps ────────────────────────────────────────────────────────
_EXCITED_WORDS   = {"amazing","incredible","awesome","fantastic","brilliant",
                    "wonderful","love","best","thrilled","overjoyed","ecstatic",
                    "outstanding","superb","phenomenal","wow"}
_INQUISITIVE     = {"why","how","what","when","where","who","wonder","curious",
                    "question","tell me","explain","understand"}
_SURPRISED       = {"surprised","shocked","unbelievable","unexpected","cant believe",
                    "no way","really","seriously","omg","oh my"}
_CONCERNED       = {"worried","concern","worried","serious","careful","risk",
                    "problem","issue","trouble","danger","afraid","anxious"}
_FRUSTRATED_KWS  = {"hate","terrible","awful","horrible","useless","worst",
                    "annoying","disgusting","ridiculous","furious","stupid"}

def detect_emotion(text: str) -> dict:
    """
    Returns a dict:
        {
            'emotion':    str,   # one of 8 categories
            'intensity':  float, # 0.0 – 1.0 (how strong the emotion is)
            'compound':   float, # raw VADER compound score
            'label':      str,   # human-friendly label with emoji
        }
    """
    scores  = _analyzer.polarity_scores(text)
    compound = scores["compound"]        # range -1.0 … +1.0
    pos      = scores["pos"]
    neg      = scores["neg"]

    words_lower = set(text.lower().split())
    text_lower  = text.lower()

    # ── Determine emotion category ────────────────────────────────────────────
    if compound >= 0.6 and (words_lower & _EXCITED_WORDS or pos > 0.35):
        emotion = "excited"
    elif compound >= 0.2:
        emotion = "positive"
    elif compound <= -0.5 and (words_lower & _FRUSTRATED_KWS or neg > 0.35):
        emotion = "frustrated"
    elif compound <= -0.2:
        emotion = "negative"
    elif any(kw in text_lower for kw in _SURPRISED):
        emotion = "surprised"
    elif any(kw in text_lower for kw in _CONCERNED):
        emotion = "concerned"
    elif any(w in words_lower for w in _INQUISITIVE) or text.strip().endswith("?"):
        emotion = "inquisitive"
    else:
        emotion = "neutral"

    # ── Intensity: 0 (mild) → 1 (extreme) ────────────────────────────────────
    # Map |compound| from [0, 1] → but cap at 1.0; raise slightly for extreme words
    raw_intensity = abs(compound)
    bonus = 0.15 if words_lower & (_EXCITED_WORDS | _FRUSTRATED_KWS) else 0.0
    intensity = min(1.0, raw_intensity + bonus)

    labels = {
        "excited":     "😄 Excited",
        "positive":    "🙂 Positive",
        "frustrated":  "😤 Frustrated",
        "negative":    "😢 Negative",
        "surprised":   "😲 Surprised",
        "concerned":   "😟 Concerned",
        "inquisitive": "🤔 Inquisitive",
        "neutral":     "😐 Neutral",
    }

    return {
        "emotion":   emotion,
        "intensity": round(intensity, 3),
        "compound":  round(compound, 3),
        "label":     labels[emotion],
    }