# **Mental Health Burnout Detection System**

### **Problem Statement**

**Burnout**—a state of emotional, mental, and often physical exhaustion—has become an all-too-common consequence of modern work and study environments. According to the World Health Organization, “burn-out” is an occupational phenomenon resulting from chronic workplace stress that has not been successfully managed.

Current tools for detecting burnout rely mostly on infrequent, self-reported surveys, which miss daily fluctuations and fail to provide timely, actionable insights. This gap can lead to missed opportunities for early intervention, with severe consequences for personal well-being and organizational productivity.

### **Our Solution**

The **Mental Health Burnout Detection System** is a full-stack, AI-powered platform that:

* Continuously monitors daily behavioral and physiological data (sleep, work, screen time, etc.)  
* Calculates burnout risk using evidence-based algorithms  
* Delivers personalized wellness tips using OpenAI GPT-4  
* Provides real-time feedback to users for proactive self-care

### **Key Features**

* **Intelligent Risk Assessment:** Analyzes user input with validated algorithms to categorize burnout risk as Low, Moderate, or High.  
* **AI-Powered Personalization:** Generates contextual, actionable wellness recommendations using advanced AI models.  
* **Professional User Experience:** Responsive, accessible, and visually appealing dashboard with real-time feedback.  
* **Enterprise-Grade Architecture:** Robust error handling, security, logging, and scalable microservices design.

### **System Architecture**

The system uses a modern **microservices architecture**:
* **Frontend:** Single-page web app for data entry and results display (frontend/index.html,styles.css,scripts.js)  
* **Backend:** Node.js \+ Express API for risk calculation and orchestration (backend/server.js)  
* **AI Service:** Python FastAPI microservice for generating AI-powered tips (ai-service/app.py)

### **Technology Stack**

* **Frontend:** HTML5, CSS3, Vanilla JavaScript  
* **Backend:** Node.js, Express.js, CORS, Helmet, Morgan  
* **AI Service:** Python, FastAPI, Pydantic V2, OpenAI GPT-4, Uvicorn

### **Minimalist File Structure**

mental-health-burnout-detection/  
├── frontend/  
│   └── index.html  
├── backend/  
│   ├── server.js  
│   ├── package.json  
│   └── .env  
├── ai-service/  
│   ├── app.py  
│   ├── requirements.txt  
│   └── .env  
└── README.md


### **Quick Start**

1. **Install Dependencies**  
   \# Backend  
   cd backend  
   npm install

   \# AI Service  
   cd ../ai-service  
   pip install \-r requirements.txt  
2. **Configure Environment Variables**  
   backend/.env  
   NODE\_ENV=development  
   PORT=3000  
   ML\_SERVICE\_URL=http://localhost:5001  
   LOG\_LEVEL=info  
   ai-service/.env

   OPENAI\_API\_KEY=sk-your\_openai\_api\_key\_here  
   SERVICE\_PORT=5001  
   CACHE\_DURATION=300  
   PYTHON\_ENV=development  
   LOG\_LEVEL=info  
3. **Run All Services**  
   \# Terminal 1: AI Service  
   cd ai-service  
   python app.py

   \# Terminal 2: Backend  
   cd backend  
   node server.js

   \# Terminal 3: Frontend  
   cd frontend  
   python \-m http.server 8080  
   \# Or open index.html directly in your browser

4. **Usage**  
   * Open http://localhost:8080  
   * Enter your daily data (sleep, work, screen time, etc.)  
   * Submit to see your burnout risk and personalized AI tips

### **How It Works**

* **User Input:** You enter your daily health and work data in the frontend.  
* **Backend Processing:** The backend validates your data, calculates your burnout risk, and sends it to the AI service.  
* **AI-Powered Tips:** The AI service (using GPT-4 or fallback) returns 2–3 actionable wellness recommendations.  
* **Results Display:** The frontend shows your risk score, risk category, and AI-generated tips.

### **Real-World Applications**

* **Corporate Wellness:** Proactively monitor and support employee mental health.  
* **Healthcare:** Continuous monitoring of healthcare worker or patient burnout risk.  
* **Education:** Help students and staff manage academic stress.  
* **Personal Wellness:** Individuals track their own burnout risk and receive daily advice.
