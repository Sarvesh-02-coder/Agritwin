# AgriTwin – A Smart Farming Companion

AgriTwin is a project built by **Team We Bare Bugs** for **CodeWave 25**.  
It is designed as a guide app for farmers, especially in rural areas, to help them make informed agricultural decisions with the power of AI, data, and simulations.  

---

## Features  

### What-If Simulator  
Simulates yield production based on conditions like seed delay or irrigation delays, helping farmers understand the impact of their decisions before they occur.  

### Crop Recommendation & Pest Alerts  
- Provides crop recommendations tailored to upcoming weather and soil health.  
- Displays pest alerts on the same page to warn farmers in advance.  

### Smart Irrigation  
- Recommends how much water should be given and when to irrigate.  
- Includes a weekly water analysis to optimize irrigation schedules.  

### Risk Forecast  
- Forecasts expected yield and expected income based on market prices.  
- Highlights risk factors (like pests, weather, or delays) that could impact productivity.  

### AgriTwin Coach (AI Chatbot)  
- An AI-powered chatbot that answers farmers’ questions in real-time.  
- Provides agricultural suggestions, tips, and acts as a virtual guide.  
- Uses a JSON-based model along with Gemini API key for responses.  

### Farmer Profile  
- Stores only essential details like farm area, pincode, phone number, and name.  
- All other information is fetched dynamically from backend datasets and APIs.  

---

## Data Sources & APIs  

- Weather Data: NASA POWER API  
- Soil Health Data: ISRIC Soil API  
- Market Prices: Agmarknet  
- Pests: Hardcoded dataset for MVP stage  
- Extra Services: Fertilizers and more (planned for future versions)  

---

## Machine Learning  

We developed a Yield Prediction ML Model trained on a dataset of ~3,00,000 entries.  
- Model framework: CatBoost (chosen for higher accuracy compared to XGBoost).  
- Provides yield forecasts that connect directly with the risk forecast and what-if simulator.  

---

## Tech Stack  

- Frontend: React + Vite  
- Backend: Python (FastAPI-based)  
- ML Model: CatBoost, Python-based training  
- Databases & Services: APIs + in-house backend datasets  
- Chatbot: JSON model + Gemini API key  

---

## Installation & Usage  

### 1. Clone the Repository  
```bash
git clone https://github.com/Sarvesh-02-coder/AgriTwin.git
cd AgriTwin
```

### 2. Setup Backend  
Navigate to backend folder:  
```bash
cd backend
```

Create and activate virtual environment:  
```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
source .venv/bin/activate  # On Mac/Linux
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

Run backend server:  
```bash
python -m uvicorn app.main:app --reload
```

### 3. Setup Frontend  
Navigate to frontend folder:  
```bash
cd frontend
```

Install dependencies:  
```bash
npm install
```

Run frontend:  
```bash
npm run dev
```

### 4. Setup Chatbot  
Navigate to chatbot folder:  
```bash
cd chatbot
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

Make sure to set up your Gemini API Key in the chatbot config/environment before running.  

---

## Requirements  

- `requirements.txt` (backend): Contains all dependencies required for backend + ML model.  
- `chatbot/requirements.txt`: Separate list of dependencies for chatbot services.  

---

## Team – We Bare Bugs  

- Sarvesh Sapkal – Backend Developer  
- Shalvi Maheshwari – ML Model & Chatbot Developer  
- Laukika Shinde – Frontend Developer  

---

## Hackathon Spirit  

This project was built with passion and dedication for CodeWave 25.  
We pushed ourselves to integrate real-world APIs, AI models, and smart simulations into a single farmer-friendly platform.  

While we encountered challenges (multi-lingual backend bug, offline SMS integration), we worked tirelessly to debug and enhance our system. Every bug taught us something new — and that’s the true hackathon spirit.  

---

## Conclusion  

AgriTwin is more than an app — it’s a vision for smarter, data-driven agriculture. By combining AI, real-time APIs, and farmer-friendly features, it aims to empower rural farmers with actionable insights, reduce risks, and increase productivity.  
