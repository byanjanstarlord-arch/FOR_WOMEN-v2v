# HerSakhi – AI Career Companion

HerSakhi is an AI-powered career development platform designed to help women plan, grow, and achieve their professional goals through personalized guidance, intelligent analysis, and modern user experience.

## ✨ Key Features
- AI-powered career roadmap generation
- Resume analysis and improvement suggestions
- Skill gap detection and learning recommendations
- AI mentorship and career guidance
- Modern premium UI built with Three.js, GSAP, and glassmorphism
- Django backend with REST APIs
- Modular AI service layer with OpenRouter integration

## 🛠 Tech Stack
- Backend: Django, Django REST Framework
- Frontend: HTML, CSS, JavaScript, Three.js, GSAP
- AI: OpenRouter
- Database: SQLite/PostgreSQL

## 🚀 Getting Started
```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
Open http://localhost:8000.

## 📁 Project Structure
- `templates/` – HTML templates
- `static/` – CSS, JS, images, assets
- `ai/` – AI service modules
- `manage.py` – Django entry point

## 🔐 Environment
Configure required variables in `.env`, including `DATABASE_URL` and `OPENROUTER_API_KEY`.

## 📄 License
This project is intended for educational, research, and hackathon purposes unless otherwise specified.