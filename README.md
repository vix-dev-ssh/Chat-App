# Chat-App
# Real-Time Individual Chat Application

A real-time one-to-one chat application built using Django (MVT) and Django Channels with WebSocket support.

## 🚀 Features

- Custom User Model (email-based authentication)
- User Registration, Login & Logout
- Authenticated access control
- Real-time private chat using WebSockets
- Online status indicator
- Message persistence (SQLite)
- Read receipts (✓ sent, ✓✓ read)
- Auto-scroll to latest message
- Clean MVT architecture

---

## 🛠 Tech Stack

- Python
- Django (MVT Architecture)
- Django Channels
- SQLite
- HTML, CSS, JavaScript

---

## 📦 Installation

### 1. Clone the repository

git clone https://github.com/vix-dev-ssh/Chat-App.git
cd chat_app


### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # Mac/Linux

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run migrations

python manage.py makemigrations
python manage.py migrate

### 5. Create superuser

python manage.py createsuperuser

### 6. Run server using Daphne (ASGI)

daphne chat_app.asgi:application
