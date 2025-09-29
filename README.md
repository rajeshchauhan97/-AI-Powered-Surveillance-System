# 🎬 Movie Booking System - Algo Bharat Assignment

A complete backend API for **movie ticket booking** built with **FastAPI**, **SQLAlchemy**, and **SQLite/PostgreSQL**. Deployed on **Render** for demo.

---

## 🚀 Features Implemented

✅ **CRUD APIs** for movies, theaters, halls, shows, and bookings  
✅ **Theater hall layout** with flexible seating (6+ seats per row)  
✅ **Group booking** with seat validation  
✅ **Alternative show suggestions** when seats are not available together  
✅ **Concurrent booking prevention** with database transactions  
✅ **Analytics APIs** with GMV tracking  
✅ **Render deployment** with public URL for demo  

---

## 📂 Project Architecture

```

movie_booking/
├── app/
│   ├── **init**.py
│   ├── main.py
│   ├── models/
│   │   ├── **init**.py
│   │   └── database.py
│   ├── schemas/
│   │   ├── **init**.py
│   │   ├── movie.py
│   │   ├── theater.py
│   │   └── booking.py
│   ├── routers/
│   ├── crud/
│   └── utils/
│       └── database.py
├── tests/
│   └── test_complete_system.py
├── requirements.txt
├── render.yaml
├── main.py
├── .env
├── Dockerfile
└── README.md

````

---

## 🛠️ Local Development Setup

```bash
# Clone repository
git clone https://github.com/rajeshchauhan97/movie-booking-system.git
cd movie-booking-system

# Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Access Swagger docs
# http://127.0.0.1:8000/docs

# Run tests
python tests/test_complete_system.py
````

---

## ⚙️ Environment Variables

Create a `.env` file:

```ini
DATABASE_URL=sqlite:///./movie_booking.db
SECRET_KEY=your_secret_key
```

In `app/config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
```

---

## 🧪 API Testing Examples

**1. Create Movie**

```bash
curl -X POST "http://127.0.0.1:8000/movies" \
-H "Content-Type: application/json" \
-d '{"title": "Inception", "duration": 148, "genre": "Sci-Fi", "rating": 8.8}'
```

**2. Create Theater**

```bash
curl -X POST "http://127.0.0.1:8000/theaters" \
-H "Content-Type: application/json" \
-d '{"name":"IMAX Cinema","location":"Downtown Mall"}'
```

**3. Create Hall**

```bash
curl -X POST "http://127.0.0.1:8000/halls" \
-H "Content-Type: application/json" \
-d '{"theater_id":1,"hall_number":1,"seats_per_row":{"A":8,"B":7,"C":9,"D":6,"E":10}}'
```

**4. Create Show**

```bash
curl -X POST "http://127.0.0.1:8000/shows" \
-H "Content-Type: application/json" \
-d '{"movie_id":1,"theater_id":1,"hall_id":1,"show_time":"2025-09-29T20:00:00","price":12.50}'
```

**5. Group Booking**

```bash
curl -X POST "http://127.0.0.1:8000/bookings/group" \
-H "Content-Type: application/json" \
-d '{"show_id":1,"user_ids":[1,2,3,4],"seats":["A1","A2","A3","A4"]}'
```

---

## ☁️ Render Deployment Guide

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Configure Render

1. Go to [Render.com](https://render.com) → Sign up/Login
2. Click **New Web Service** → Connect your GitHub repo
3. Configure service:

   * **Name:** `movie-booking-system`
   * **Branch:** `main`
   * **Runtime:** Python 3.x
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

Update `main.py` for Render port:

```python
import os
import uvicorn
from app.main import app

port = int(os.environ.get("PORT", 10000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Step 3: Optional `render.yaml`

```yaml
services:
  - type: web
    name: movie-booking-system
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    autoDeploy: true
```

### Step 4: Verify Deployment

```bash
curl https://movie-booking-system.onrender.com/health
```

Access API Docs:
`https://movie-booking-system.onrender.com/docs`

---

## 🐳 Optional – Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build & run:

```bash
docker build -t movie-booking .
docker run -p 8000:8000 movie-booking
```

---

## 📚 API Endpoints

* `GET /` → API info

* `GET /health` → Health check

* `GET /docs` → Swagger UI

* `GET /movies` → List all movies

* `POST /movies` → Create movie

* `GET /movies/{id}` → Movie details

* `GET /theaters` → List theaters

* `POST /theaters` → Create theater

* `POST /halls` → Create hall

* `POST /bookings/book` → Book tickets

* `POST /bookings/group` → Group booking

* `GET /analytics/movie/{id}` → Movie analytics

* `GET /analytics/theater/{id}` → Theater revenue

---

## 🔧 Technology Stack

* **Backend:** FastAPI
* **Database:** SQLAlchemy ORM (SQLite/PostgreSQL)
* **Validation:** Pydantic
* **Deployment:** Render (Free Tier)
* **Testing:** Python unittest
* **Version Control:** Git & GitHub

---

## 👨‍💻 Developer

**Raju sabhavath**
*Algo Bharat Internship Assignment*
GitHub: [rajeshchauhan97](https://github.com/rajeshchauhan97)

