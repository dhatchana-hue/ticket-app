import pandas as pd
import random

def generate_dataset(n=5000):
    data = []
    sources = ["Chennai", "Bangalore", "Hyderabad", "Coimbatore"]
    destinations = ["Bangalore", "Chennai", "Delhi", "Mumbai"]
    classes = ["Sleeper", "3A", "2A"]

    for _ in range(n):
        total = random.randint(50, 100)
        booked = random.randint(0, total)

        data.append({
            "train_id": random.randint(10000, 99999),
            "train_name": "Express_" + str(random.randint(1, 200)),
            "source": random.choice(sources),
            "destination": random.choice(destinations),
            "class": random.choice(classes),
            "total_seats": total,
            "booked_seats": booked,
            "seat_available": total - booked
        })

    return pd.DataFrame(data)
