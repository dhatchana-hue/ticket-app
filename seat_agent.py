import random

def seat_availability_agent(trains):
    return trains[trains["seat_available"] > 0].copy()

def generate_seat_map(total_seats=24):
    seats = []
    for i in range(1, total_seats + 1):
        seat_type = "Lower" if i % 2 == 1 else "Upper"
        seats.append({
            "seat_no": i,
            "seat_type": seat_type,
            "status": "Available"
        })
    return seats

def mark_booked_seats(seats, booked_count=6):
    booked = random.sample([s["seat_no"] for s in seats], booked_count)
    for s in seats:
        if s["seat_no"] in booked:
            s["status"] = "Booked"
    return seats
