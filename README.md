# 🧭 AI Travel Guide & Audio Companion

An intelligent, interactive AI-powered travel guide and audio narration companion that brings world wonders and historic monuments to life with generative storytelling and natural voice synthesis.

---

## ✨ Features

- **🏛️ Curated Heritage Destinations:** Explore iconic landmarks like the *Taj Mahal, Red Fort, Gateway of India, Hawa Mahal, Golden Temple, Mysore Palace*, and custom searched destinations.
- **⏱️ Flexible Guide Lengths:**
  - **Summarized (~1 min):** Concise, high-level overview focusing on significance and architectural highlights.
  - **Detailed (~3 min):** Deep, immersive storytelling covering history, culture, and interesting insights.
- **🌐 Multilingual Support:** Generate guides and audio narration in **English, Hindi, Tamil, and Telugu**.
- **🎙️ Realistic Voice Narration:** Integrated with **Murf AI (Falcon Model)** for natural Male & Female voice synthesis.
- **📜 Live Transcript Reader:** Expandable transcript section to read the full generated guide alongside audio playback.
- **📱 Responsive & Elegant UI:** Built with modern Tailwind CSS and refined typography.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, Tailwind CSS, JavaScript (ES6+ Fetch API)
- **Backend:** Python 3, Flask, Flask-CORS, Gunicorn
- **AI & APIs:**
  - **Google Gemini API (`google-genai` SDK):** Generates structured multilingual tourist guides.
  - **Murf AI Speech API:** Generates high-fidelity streaming audio narration.

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/) API Key
- A [Murf AI](https://murf.ai/) API Key

### 2. Clone Repository
```bash
git clone https://github.com/venkat842/tourist.git
cd tourist
```

### 3. Setup Environment Variables
Create a `.env` file in the `Backend/` directory (or copy from `.env.example`):
```env
MURF_API_KEY=your_murf_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5001
```

### 4. Install Dependencies
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r Backend/requirements.txt
```

### 5. Run the Application
```bash
python Backend/app.py
```
Open **[http://localhost:5001](http://localhost:5001)** in your browser!

---

## ☁️ Deployment

### Deploy on Render

1. Create a new **Web Service** on [Render](https://render.com) and connect this repository.
2. Configure settings:
   - **Root Directory:** `Backend` (or leave default `/`)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
3. Add your Environment Variables in the Render dashboard:
   - `MURF_API_KEY`
   - `GEMINI_API_KEY`
4. Deploy! Render will serve the full interactive web application directly from your live URL.

---

## 📁 Project Structure

```
tourist/
├── Backend/
│   ├── app.py              # Flask server & AI generation endpoints
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variable template
│   └── static/             # Bundled static frontend assets
├── Frontend/
│   ├── index.html          # Main UI layout
│   └── index.js            # Client-side state & API handlers
├── Procfile                # Deployment start command
├── render.yaml             # Render Blueprint configuration
├── requirements.txt        # Root requirements for cloud hosting
└── README.md               # Project documentation
```

---

## 🔒 Security Note
Never commit your `.env` file or raw API keys to version control. Keep `.env` listed inside `.gitignore` at all times.
