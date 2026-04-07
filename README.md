# 🎤 The Empathy Engine

> An AI-powered service that synthesises **emotionally expressive speech** from plain text — dynamically modulating vocal characteristics based on detected emotion and intensity.

---

## ✨ Features

| Capability | Detail |
|---|---|
| **8 Emotion Categories** | Excited, Positive, Surprised, Inquisitive, Neutral, Concerned, Negative, Frustrated |
| **Intensity Scaling** | Emotion strength (0–100%) proportionally scales rate, pitch, and volume |
| **Multi-Parameter TTS** | Three vocal parameters modulated: **Rate**, **Pitch**, **Volume** |
| **Web UI** | Premium dark-mode interface with audio player and emotion badge |
| **REST API** | JSON endpoint for programmatic access |
| **CLI Mode** | Terminal interface for quick testing |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/empathy_engine.git
cd empathy_engine

pip install -r requirements.txt
# First-time NLTK data (if needed by VADER)
python -c "import vaderSentiment"
```

### 2. Run the Web App

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

### 3. CLI Mode

```bash
# Interactive prompt
python app.py --cli

# Or pass text directly
python app.py --text "This is absolutely incredible news!"
```

### 4. REST API

```bash
curl -X POST http://127.0.0.1:5000/generate \
     -H "Content-Type: application/json" \
     -d '{"text": "Why does this keep happening to me?"}'
```

**Response:**
```json
{
  "text": "Why does this keep happening to me?",
  "emotion": "inquisitive",
  "label": "🤔 Inquisitive",
  "intensity": 0.21,
  "compound": -0.21,
  "audio_url": "/outputs/output_inquisitive_1712512345.wav"
}
```

---

## 📁 Project Structure

```
empathy_engine/
├── app.py              # Flask app — Web UI, REST API, CLI
├── emotion.py          # Emotion detection (VADER + keyword heuristics)
├── tts_engine.py       # TTS synthesis (pyttsx3 — offline, multi-param)
├── requirements.txt
├── outputs/            # Generated audio files (auto-created)
└── templates/
    └── index.html      # Premium dark-mode web UI
```

---

## 🧠 Design Choices

### Emotion Detection — `emotion.py`

**Engine:** [VADER](https://github.com/cjhutto/vaderSentiment) (Valence Aware Dictionary and sEntiment Reasoner)

VADER was chosen because:
- Specifically tuned for short, expressive text (vs. long-form prose)
- Returns a `compound` score in `[-1, 1]` — perfect for intensity calculation
- No model download required; runs instantly offline

**Classification Logic:**

```
compound ≥ 0.6  + excited keywords   → 😄 Excited
compound ≥ 0.2                       → 🙂 Positive
compound ≤ -0.5 + frustrated keywords → 😤 Frustrated
compound ≤ -0.2                      → 😢 Negative
"?" ending / question words          → 🤔 Inquisitive
surprise keywords                    → 😲 Surprised
concern keywords                     → 😟 Concerned
otherwise                            → 😐 Neutral
```

**Intensity Formula:**
```python
intensity = min(1.0, abs(compound) + 0.15 * extreme_keyword_bonus)
```

A text with `compound = 0.9` and extreme keywords scores **intensity ≈ 1.0** (max modulation); a mild text scoring `compound = 0.25` scores **intensity ≈ 0.25** (subtle modulation).

---

### Vocal Parameter Modulation — `tts_engine.py`

**Engine:** [pyttsx3](https://pyttsx3.readthedocs.io/) — fully offline, no API key needed

Three vocal parameters are modulated per-emotion with intensity scaling:

| Emotion | Base Rate (wpm) | Base Pitch | Base Volume | Intensity Effect |
|---|---|---|---|---|
| Excited | 210 | 65 | 0.98 | +30 rate, +15 pitch |
| Positive | 195 | 58 | 0.90 | +30 rate, +15 pitch |
| Surprised | 205 | 68 | 0.93 | +30 rate, +15 pitch |
| Inquisitive | 175 | 55 | 0.87 | — |
| Neutral | 180 | 50 | 0.85 | — |
| Concerned | 160 | 44 | 0.82 | −25 rate, −12 pitch |
| Negative | 155 | 40 | 0.78 | −25 rate, −12 pitch |
| Frustrated | 145 | 35 | 0.75 | −25 rate, −12 pitch |

**Intensity scaling example:**  
`"This is good."` → intensity 0.3 → rate +9, pitch +4  
`"This is the BEST NEWS EVER!"` → intensity 1.0 → rate +30, pitch +15

---

## 🛠 Tech Stack

| Component | Library |
|---|---|
| Web Framework | Flask |
| Emotion Analysis | vaderSentiment |
| Text-to-Speech | pyttsx3 (offline / SAPI5 on Windows) |
| Audio Format | WAV (native pyttsx3 output) |

---

## 📋 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `GET /` | GET | Web UI |
| `POST /generate_ui` | POST (form) | Generate audio from web form |
| `POST /generate` | POST (JSON) | REST API — returns JSON + audio URL |
| `GET /health` | GET | Service health check |
| `GET /outputs/<file>` | GET | Serve generated audio file |

---

## 🔑 Environment & Requirements

No API keys required — entirely offline using pyttsx3 and VADER.

```
flask>=2.3
vaderSentiment>=3.3.2
pyttsx3>=2.90
gunicorn>=21.2
```

> **Windows note:** pyttsx3 uses the SAPI5 engine by default (built into Windows). On Linux, install `espeak`: `sudo apt install espeak`.

---

## 🎯 Challenge Compliance

| Requirement | Status |
|---|---|
| Text input (CLI / API / Web) | ✅ All three modes |
| ≥ 3 emotion categories | ✅ 8 categories |
| ≥ 2 vocal parameters modulated | ✅ Rate + Pitch + Volume (3) |
| Emotion → voice mapping | ✅ Documented above |
| Playable audio output | ✅ WAV via pyttsx3 |
| **Bonus:** Granular emotions | ✅ 8 nuanced states |
| **Bonus:** Intensity scaling | ✅ Proportional to compound score |
| **Bonus:** Web UI | ✅ Premium dark-mode UI |

---

*Built for the Empathy Engine Challenge — AI-driven expressive voice synthesis.*