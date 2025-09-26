Got it 👍 You want your **README.md** to include the project architecture tree.
Here’s a polished version of the README with the **folder structure** integrated:

```markdown
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


# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Check status
git status

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
# Create Procfile
echo "web: uvicorn app.main:app --host=0.0.0.0 --port=\$PORT" > Procfile

heroku create your-app-name
git push heroku main
```

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

## 📌 License

MIT License

```

---

👉 Do you want me to also **fill your README with API examples (sample requests/responses for movies, bookings, theaters)** so it becomes developer-ready?
```
