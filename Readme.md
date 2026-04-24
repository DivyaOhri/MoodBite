# 🍜 MoodBite — Eat What You Feel

**Smart Food Recommender with Emotion-Aware Analysis**  
Yogananda School of AI · Shoolini University · CSU2217

---

## 👥 Team
| No. | Name | Registration ID | Role |
|---|---|---|---|
| 1 | Divya Ohri | GF202453419 | Backend & GenAI Integration |
| 2 | Aishwarya Rana | Gf202453090 | RAG Pipeline & Vector Database |
| 3 | Diya | GF202460495 | Frontend / UI & Questionnaire Logic |
| 4 | Kashish | GF202462554 | Testing, Evaluation & Documentation |

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 File Structure
```
moodbite/
├── app.py              # Main Streamlit application (all pages + CSS)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🗺️ App Pages
| Page | Purpose |
|---|---|
| 🏠 Home | Welcome screen with features & stats |
| 😊 Mood Check | 4-question input form (mood, stress, energy, budget) |
| 💡 Mood Insights | Detected mood, energy/stress bars, AI explanation |
| 💰 Budget Insights | Budget utilisation, price comparison, saving tips |
| 🍽️ Food Details | Detailed food cards with descriptions, tags & science |
| 👤 Profile | Save preferences, dietary type, budget range |
| ✨ Results | Core output — top 3 food recommendations |
| 📖 About | Project info, wellness tips, team credits |

---

## 🔧 Tech Stack (Full Production)
- **Frontend**: Streamlit
- **GenAI / LLM**: Google Gemini API (`gemini-pro`)
- **Vector Database**: ChromaDB (local instance)
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **RAG Framework**: LangChain (Python)
- **Language**: Python 3.10+

> **Note**: The current `app.py` uses mock data for food results. To connect the real RAG pipeline, replace the `MOCK_RESULTS` dictionary with your ChromaDB retrieval calls and Gemini API generation.

---

## 🎨 Design
- Warm, earthy palette: creams, peaches, amber, sage
- Typography: Cormorant Garamond (display) + Outfit (body)
- Fully responsive sidebar navigation
- Smooth hover animations on all interactive elements

---

*Made with ❤️ at Yogananda School of AI, Shoolini University*