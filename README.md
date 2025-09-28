# 🎬 Movie Booking System - Algo Bharat Assignment

A complete backend API for movie ticket booking built with **FastAPI**, **SQLAlchemy**, and **SQLite/PostgreSQL**. Deployed on **Render** for demo.

---

## 🚀 Features Implemented (Algo Bharat Requirements)

✅ **CRUD APIs** for movies, theaters, shows, bookings  
✅ **Theater hall layout** with flexible seating (6+ seats per row)  
✅ **Group booking** with seat validation  
✅ **Alternative show suggestions** when seats not available together  
✅ **Concurrent booking prevention** with database transactions  
✅ **Analytics APIs** with GMV tracking  
✅ **Render deployment** with public URL  

---

## 📂 Project Architecture

```
movie_booking/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py      # SQLAlchemy models (Movie, Theater, Show, Booking, Seat)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── movie.py         # Pydantic schemas for movies
│   │   ├── theater.py       # Pydantic schemas for theaters
│   │   └── booking.py       # Pydantic schemas for bookings
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── movies.py        # Movie CRUD endpoints
│   │   ├── theaters.py      # Theater and hall management
│   │   ├── shows.py         # Show timing management
│   │   ├── bookings.py      # Booking and seat selection
│   │   └── analytics.py     # Analytics and reporting
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── movie.py         # Movie database operations
│   │   ├── theater.py       # Theater database operations
│   │   ├── show.py          # Show database operations
│   │   └── booking.py       # Booking database operations
│   └── utils/
│       ├── __init__.py
│       └── database.py      # Database connection and session management
├── tests/
│   └── test_complete_system.py  # Comprehensive system tests
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment configuration
├── main.py                 # Root-level main for Render deployment
└── README.md
```

---

## 🌐 Live Deployment

**Live API URL:** `https://movie-booking-system-11.onrender.com`

**API Documentation:** `https://movie-booking-system-11.onrender.com/docs`

**Health Check:** `https://movie-booking-system-11.onrender.com/health`

---

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/rajeshchauhan97/movie-booking-system.git
cd movie-booking-system

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
python test_complete_system.py
```

---

## ☁️ Render Deployment

### Automatic Deployment
- Connected to GitHub repository
- Auto-deploys on every push to `main` branch
- Free tier with public URL

### Manual Setup
1. Go to [Render.com](https://render.com)
2. Connect GitHub account
3. Create new **Web Service**
4. Connect `movie-booking-system` repository
5. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - **Environment Variables:**
     - `DATABASE_URL`: `sqlite:///./movie_booking.db`

---

## 📚 API Endpoints

### Core Endpoints
- `GET /` - API information and requirements
- `GET /health` - Health check and database status
- `GET /docs` - Interactive API documentation

### Movie Management
- `GET /api/movies` - List all movies
- `POST /api/movies` - Create new movie
- `GET /api/movies/{id}` - Get movie details

### Theater Management
- `GET /api/theaters` - List all theaters
- `POST /api/theaters` - Create new theater
- `POST /api/theaters/halls` - Create theater hall with seating layout

### Booking System
- `POST /api/bookings/book` - Book tickets for a show
- `POST /api/bookings/book-together` - Group booking with alternative suggestions

### Analytics
- `GET /api/analytics/movie/{id}` - Movie booking analytics
- `GET /api/analytics/theater/{id}` - Theater revenue analytics

---

## 🧪 Testing the System

```python
# Run comprehensive test
python test_complete_system.py

# Test specific features:
python test_algo_bharat_requirements.py
```

Test includes:
- Movie and theater creation
- Hall layout with 6+ seats per row
- Group booking with seat validation
- Alternative show suggestions
- Concurrent booking prevention
- Analytics reporting

---

## 🔧 Technology Stack

- **Backend Framework:** FastAPI
- **Database:** SQLAlchemy ORM with SQLite/PostgreSQL
- **Validation:** Pydantic
- **Deployment:** Render
- **Testing:** Python unittest
- **Version Control:** Git & GitHub

---

## 📄 License

MIT License - Algo Bharat Assignment Submission

---

## 👨‍💻 Developer

**Rajesh Chauhan**  
*Algo Bharat Internship Assignment*  
GitHub: [rajeshchauhan97](https://github.com/rajeshchauhan97)

```