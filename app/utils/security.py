# app/utils/sample_data.py
from sqlalchemy.orm import Session
from app.models import Movie, Theater, TheaterHall, Show, Seat
from datetime import datetime, timedelta

def create_sample_data(db: Session):
    # Create sample movies
    movie1 = Movie(
        title="Avengers: Endgame",
        description="The epic conclusion to the Infinity Saga",
        duration_minutes=181,
        genre="Action, Adventure",
        language="English",
        release_date=datetime(2019, 4, 26)
    )
    
    movie2 = Movie(
        title="The Dark Knight",
        description="Batman faces the Joker in Gotham City",
        duration_minutes=152,
        genre="Action, Crime",
        language="English",
        release_date=datetime(2008, 7, 18)
    )
    
    db.add_all([movie1, movie2])
    db.commit()
    
    # Create sample theater
    theater = Theater(
        name="City Cinema",
        address="123 Main Street",
        city="Metropolis",
        state="State",
        zip_code="12345"
    )
    db.add(theater)
    db.commit()
    
    # Create theater hall with layout
    hall = TheaterHall(
        theater_id=theater.id,
        name="Hall A",
        total_seats=50,
        layout_json='[{"row_number": 1, "total_seats": 7}, {"row_number": 2, "total_seats": 8}, {"row_number": 3, "total_seats": 7}, {"row_number": 4, "total_seats": 8}, {"row_number": 5, "total_seats": 7}, {"row_number": 6, "total_seats": 7}, {"row_number": 7, "total_seats": 6}]'
    )
    db.add(hall)
    db.commit()
    
    # Create seats
    seats = []
    for row_num in range(1, 8):
        seat_count = 7 if row_num % 2 == 1 else 8
        if row_num == 7:
            seat_count = 6
        for seat_num in range(1, seat_count + 1):
            seat = Seat(
                hall_id=hall.id,
                row_number=row_num,
                seat_number=seat_num,
                seat_type="regular"
            )
            seats.append(seat)
    
    db.add_all(seats)
    db.commit()
    
    # Create sample shows
    show1 = Show(
        movie_id=movie1.id,
        hall_id=hall.id,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=5),
        price=12.50
    )
    
    show2 = Show(
        movie_id=movie2.id,
        hall_id=hall.id,
        start_time=datetime.now() + timedelta(hours=6),
        end_time=datetime.now() + timedelta(hours=8, minutes=32),
        price=10.00
    )
    
    db.add_all([show1, show2])
    db.commit()
    
    print("Sample data created successfully!")