# 🎬 Movie Booking Application

A backend service for managing movies, theaters, and ticket bookings, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  

---

## 🚀 Features
- Manage Movies (CRUD operations)
- Manage Theaters & Shows
- Book Tickets
- Analytics for bookings
- API Documentation via Swagger & ReDoc
- Docker & Heroku Deployment support

---

## 📂 Project Structure

```

movie_booking/
├── app/
│   ├── **init**.py
│   ├── main.py
│   ├── models/
│   │   ├── **init**.py
│   │   ├── database.py
│   │   ├── movie.py
│   │   ├── theater.py
│   │   └── booking.py
│   ├── schemas/
│   │   ├── **init**.py
│   │   ├── movie.py
│   │   ├── theater.py
│   │   └── booking.py
│   ├── crud/
│   │   ├── **init**.py
│   │   ├── movie.py
│   │   ├── theater.py
│   │   └── booking.py
│   ├── routers/
│   │   ├── **init**.py
│   │   ├── movies.py
│   │   ├── theaters.py
│   │   ├── bookings.py
│   │   └── analytics.py
│   └── utils/
│       ├── **init**.py
│       ├── database.py
│       └── security.py
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md

````

---

## 🛠️ Local Development

```bash
git clone <repository-url>
cd movie_booking
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
````
python test_complete_system.py
---

##  @Complete Git Setup

# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Check status
git 

# Set your git configuration
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# Or if you want to set it only for this repository (remove --global)
git config user.email "raju@sabhavath.com"
git config user.name "Raju Sabhavath"

# 4. Make initial commit
git commit -m "feat: Complete Movie Booking System with all features

- CRUD APIs for movies, theaters, shows
- Group booking with seat validation  
- Alternative show suggestions
- Concurrency control for seat booking
- Flexible seating layouts (min 6 seats/row)
- Analytics and revenue reporting
- Ready for deployment"

# 5. Check log
git log --oneline

## ☁️ Deploy to Heroku

```bash
# Check if Heroku CLI is installed
heroku --version

# If not installed, you can deploy without it using GitHub
# First, let's try Heroku deployment:

# Create Heroku app
heroku create movie-booking-system-algo

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev

# Deploy to Heroku
git push heroku master

# If 'master' doesn't work, try:
git push heroku main

---

## 🐳 Deploy with Docker

```bash
docker build -t movie-booking .
docker run -p 8000:8000 movie-booking
```

---

## 📖 API Documentation

Once deployed, access:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing

```bash
pytest
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and set your configuration:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/moviedb
SECRET_KEY=your-secret-key
```

---


---

👉 Do you want me to also **fill your README with API examples (sample requests/responses for movies, bookings, theaters)** so it becomes developer-ready?
```

