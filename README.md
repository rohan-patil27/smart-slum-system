# 🌟 Smart Slum Resource & Job Matching System

AI-powered platform for underprivileged urban communities to access jobs, government schemes, NGOs, and resume tools.

---

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install streamlit pandas
```

### 2. Run the App
```bash
cd smart_slum_system
streamlit run app.py
```

### 3. Open in Browser
```
http://localhost:8501
```

---

## 🔐 Demo Login Credentials

| Role  | Mobile     | Password  |
|-------|------------|-----------|
| Admin | 9999999999 | admin123  |
| User  | 9876543210 | pass123   |

---

## 📁 Project Structure

```
smart_slum_system/
├── app.py                    ← Main entry point
├── requirements.txt
├── slum_system.db            ← Auto-created SQLite database
└── modules/
    ├── __init__.py
    ├── database.py           ← DB init + sample data seeding
    ├── styles.py             ← Dark theme CSS
    ├── language.py           ← English / Hindi / Marathi translations
    ├── auth.py               ← Login & Register
    ├── job_matching.py       ← AI skill-based job matching
    ├── schemes.py            ← Government scheme eligibility checker
    ├── emergency.py          ← NGOs, hospitals, helplines
    ├── resume.py             ← HTML/PDF resume generator
    └── admin.py              ← Admin dashboard & analytics
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 AI Job Matching | Skill overlap scoring (Jaccard similarity) |
| 🏛️ Scheme Finder | Age, income, gender, caste-based eligibility |
| 📄 Resume Generator | Preview + downloadable HTML→PDF |
| 🆘 Emergency Help | NGOs, hospitals, national helplines |
| 🌐 3 Languages | English, Hindi, Marathi |
| 🎤 Voice Input | Via mobile keyboard mic support |
| ⚙️ Admin Dashboard | Analytics: skills, users, districts, jobs |
| 📊 Visual Charts | Bar charts for skills, districts, gender, caste |

---

## 💡 What You Can Add Next

1. **Google Maps integration** — Show NGO/hospital map
2. **SMS notifications** — Twilio API for job alerts
3. **Aadhaar/e-KYC verification** — DigiLocker API
4. **WhatsApp Bot** — Twilio WhatsApp for low-literacy access
5. **AI Chatbot** — Gemini/Claude API for Q&A
6. **Mobile App** — Convert to Android using Kivy or Flutter

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Database:** SQLite via sqlite3
- **Matching:** Python string matching (Jaccard)
- **Styling:** Custom CSS (dark theme, Google Fonts)
- **Languages:** Python 3.8+
