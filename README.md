# NAHB Flask + Django  
Interactive Story Builder & Reader

This project is a simple choose‑your‑own‑adventure system where users can create stories with pages and choices, and other users can play through them.  
It uses *Flask* for the API and *Django* for the frontend and user system.

The goal of the project is to show how two frameworks can work together and how to build a small interactive fiction platform.

---

## 📌 Features

### 👤 User System
- Login / Logout
- Signup
- Author role (can create stories)
- Normal users (can read/play stories)
- Admin panel (Django admin)

### ✍️ Author Tools
- Create stories
- Edit stories (title, description, status)
- Create pages
- Edit pages (text, ending, label)
- Add choices between pages
- Delete pages
- Preview story
- Autosave progress for readers
- Story stats (admin only)

### 📖 Reader Features
- Play stories from start to finish
- Resume where you left off
- Clean UI for choices
- Ending screen with label

### 🎨 Frontend
- Fully redesigned UI  
- Yellow theme  
- Modern cards, buttons, layout  
- Responsive design  
- Simple and clean for students

---

## 🏗️ Project Architecture

The project is split into two main parts:

### *1. Flask API (Backend Logic)*
Handles:
- Story data
- Pages
- Choices
- JSON endpoints
- Autosave progress

Runs on its own port (default: 5000).

### *2. Django App (Frontend + Auth)*
Handles:
- Templates
- User accounts
- Author tools
- Admin panel
- Story reader UI

Runs on its own port (default: 8000).

Django communicates with Flask using HTTP requests.

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/njfred5/nahb-flask-django
cd nahb-flask-django