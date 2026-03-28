
# STYL — Style Trend Your Look 👗✨

> AI-powered personal stylist that analyzes your outfit photos and finds real shoppable products from Myntra, Amazon, and more — in seconds.

https://github.com/user-attachments/assets/d5f07723-4932-4338-b36d-34c6131884bc

🌐 **Live Demo:** [styl-style-trend-your-look-frontend.onrender.com](https://styl-style-trend-your-look-frontend.onrender.com)

---

## 🎬 Demo

<!-- Add your demo video/gif here -->

---

## 🧠 What is STYL?

STYL is a multimodal AI fashion assistant with two core features:

- **Complete My Fit** — Upload a photo of your shirt and/or pants, pick an occasion, and STYL analyzes your outfit using Gemini Vision AI and recommends real shoppable shoes, tops, or bottoms that complete your look.
- **Occasion Stylist** — Tell STYL your occasion, style preference, gender, and budget — it builds a complete outfit from scratch and finds real products within your budget from Indian shopping platforms.

No generic suggestions. Real products. Real you.

---

## 🚀 Features

- 📸 **Multimodal Vision Analysis** — Gemini 2.5 Flash sees your actual clothing items and extracts color, style, fit, and vibe
- 🤖 **Multi-step Agent Pipeline** — LangChain agents reason across vision output, style matching, and product search
- 🛍️ **Real Product Search** — SerpApi Google Shopping returns live products from Myntra, Amazon, Flipkart, Snitch, and more
- 💰 **Budget-aware Curation** — Occasion Stylist splits your budget smartly across items and filters products by price
- 👗 **Fashion Intelligence** — Color harmony rules, occasion-appropriate footwear, gender-specific styling baked into every recommendation
- ⚡ **Fast API Backend** — Async FastAPI with modular agent architecture
- 🎨 **Editorial UI** — Clean, fashion-forward frontend with cream/terracotta palette

---

## 🏗️ Architecture

```
User Input (Image / Text)
        ↓
FastAPI Backend
        ↓
┌─────────────────────────────────┐
│         Agent Pipeline          │
│                                 │
│  Vision Agent (Gemini Vision)   │
│         ↓                       │
│  Style Agent (LangChain LLM)    │
│         ↓                       │
│  Search Agent (SerpApi)         │
└─────────────────────────────────┘
        ↓
Real Products + Recommendations
        ↓
HTML/Tailwind Frontend
```

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Frontend | HTML, Tailwind CSS, Vanilla JS |
| Backend | FastAPI, Python |
| Vision AI | Google Gemini 2.5 Flash |
| LLM Orchestration | LangChain |
| Product Search | SerpApi Google Shopping |
| Deployment | Render |

---

## 📁 Project Structure

```
STYL/
├── backend/
│   ├── main.py                  # FastAPI routes
│   ├── agents/
│   │   ├── vision_agent.py      # Gemini Vision analysis
│   │   ├── style_agent.py       # Style recommendations
│   │   ├── occasion_agent.py    # Occasion outfit planning
│   │   └── search_agent.py      # SerpApi product search
│   ├── utils/
│   │   └── image_utils.py       # Base64 image helpers
│   └── requirements.txt
├── frontend/
│   ├── index.html               # Landing page
│   ├── complete-fit.html        # Mode 1 — Complete My Fit
│   └── occasion.html            # Mode 2 — Occasion Stylist
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/krishpatel2-prog/STYL.git
cd STYL
```

### 2. Set up backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Add environment variables
Create a `.env` file inside `backend/`:
```
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_API_KEY=your_serpapi_key
```

### 4. Run backend
```bash
uvicorn main:app --reload --port 8000
```

### 5. Run frontend
```bash
cd ../frontend
python -m http.server 3000
```

Open `http://localhost:3000` in your browser.

---

## 🔌 API Endpoints

### `POST /analyze` — Complete My Fit
| Field | Type | Description |
|---|---|---|
| `shirt` | File (optional) | Shirt image |
| `pants` | File (optional) | Pants image |
| `occasion` | String | e.g. Date, Party, Office |
| `gender` | String | masculine / feminine / neutral |

**Response:** Vision analysis + occasion match score + stylist verdict + real product recommendations

---

### `POST /occasion` — Occasion Stylist
| Field | Type | Description |
|---|---|---|
| `occasion` | String | e.g. Date, Wedding |
| `style` | String | e.g. Classic, GenZ, Streetwear |
| `gender` | String | masculine / feminine / neutral |
| `budget_min` | Int | Minimum budget in INR |
| `budget_max` | Int | Maximum budget in INR |

**Response:** Complete outfit plan + real products within budget

---

## 🌐 Deployment

Both services deployed on **Render**:
- Backend — Render Web Service (Python)
- Frontend — Render Static Site

---

## 🙌 Built By

**Krish Patel** — 2nd year B.Tech AI & Data Science, KJ Somaiya Institute of Technology

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/krishpatel2-prog)

---

*Powered by Gemini AI · Built with ❤️ and FastAPI*
