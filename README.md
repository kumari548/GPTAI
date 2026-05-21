# FitnessGPT AI

FitnessGPT AI is a Generative AI based fitness assistant developed using Flask, Groq API, HTML, CSS, and JavaScript.

The application works similar to ChatGPT but focuses only on fitness-related conversations such as workouts, diet plans, weight loss, bodybuilding, and healthy lifestyle guidance.

---

# Features

- AI-powered fitness assistant
- Groq Llama 3.3 integration
- Prompt engineering based responses
- Modern ChatGPT-like interface
- Multiple chat history support
- Voice input support
- New chat functionality
- Dynamic sidebar chat names
- Custom background image support
- Responsive UI design

---

# Technologies Used

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Python Flask

## AI Integration
- Groq API
- Llama 3.3 70B Versatile Model

---

# 📁 Project Structure

fitnessgpt/
│
├── app.py
├── requirements.txt
├── .env
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── images/
│       └── gym.jpg
│
└── README.md

---

# ⚙️ Installation

## 1. Create Virtual Environment


python -m venv venv

## 2. Activate Virtual Environment

### Windows

venv\Scripts\activate

---

# 📦 Install Required Packages

pip install -r requirements.txt

---

# 🔑 Setup API Key

Create .env file:

GROQ_API_KEY=YOUR_GROQ_API_KEY

Get Groq API Key from:

https://console.groq.com/keys

---

# ▶️ Run Project

python app.py
