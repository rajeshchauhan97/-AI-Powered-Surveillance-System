# 🎬 Movie Booking Application

A backend service for managing movies, theaters, and ticket bookings, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  

---

## 🚀 Features
- Manage Movies (CRUD operations)
- Manage Theaters & Shows
- Book Tickets (single & group)
- Suggest alternative shows if seats unavailable
- Analytics for bookings and revenue
- API Documentation via Swagger & ReDoc
- Docker & Railway Deployment support

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
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
````

Test the application endpoints:

```bash
python test_fix.py
```

---

## @Complete Git Setup

```bash
git init
git add .
git commit -m "feat: Complete Movie Booking System with all features"
git log --oneline
```

Set your git config:

```bash
git config user.email "raju@sabhavath.com"
git config user.name "Raju Sabhavath"
```

---

## ☁️ Deploy to Railway

1. **Install Railway CLI** (optional): [https://railway.app/install](https://railway.app/install)

2. **Login to Railway**:

```bash
railway login
```

3. **Initialize project**:

```bash
railway init
```

4. **Connect PostgreSQL plugin** (or any database service):

```bash
railway add postgresql
```

5. **Deploy your application**:

```bash
railway up
```

6. **Open deployed app**:

```bash
railway open
```

> Railway will automatically detect your Python app and run `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

---

## 🐳 Deploy with Docker

```bash
docker build -t movie-booking .
docker run -p 8000:8000 movie-booking
```

---

## 📖 API Documentation

Once running locally or on Railway, access:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing

Run all tests using:

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
