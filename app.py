import pandas as pd
import random
import streamlit as st

# =====================================
# DATASET GENERATION (Simulated)
# =====================================
def generate_dataset(n=5000):
    data = []
    sources = ["Chennai", "Bangalore", "Hyderabad", "Coimbatore"]
    destinations = ["Bangalore", "Chennai", "Delhi", "Mumbai"]
    classes = ["Sleeper", "3A", "2A"]
    preferences = ["Lower", "Upper", "Any"]

    for _ in range(n):
        total_seats = random.randint(50, 100)
        booked_seats = random.randint(0, total_seats)

        data.append({
            "train_id": random.randint(10000, 99999),
            "train_name": "Express_" + str(random.randint(1, 200)),
            "source": random.choice(sources),
            "destination": random.choice(destinations),
            "travel_date": "2025-12-10",
            "class": random.choice(classes),
            "total_seats": total_seats,
            "booked_seats": booked_seats,
            "seat_available": total_seats - booked_seats,
            "passenger_age": random.randint(18, 70),
            "preference": random.choice(preferences)
        })

    return pd.DataFrame(data)

# Create dataset once
df = generate_dataset()

# =====================================
# OpenAI QUERY UNDERSTANDING AGENT (SIMULATED)
# =====================================
def openai_query_agent(user_text, source, destination, travel_class):
    return {
        "intent": "Book Ticket",
        "source": source,
        "destination": destination,
        "class": travel_class,
        "original_text": user_text
    }

# =====================================
# AGENTS
# =====================================
def train_search_agent(query):
    return df[
        (df["source"] == query["source"]) &
        (df["destination"] == query["destination"]) &
        (df["class"] == query["class"])
    ].copy()

def seat_availability_agent(trains):
    return trains[trains["seat_available"] > 0].copy()

def notification_agent(result):
    if result is None:
        return "❌ Booking Failed: No seats available. Please try another train or class."
    return (
        "✅ Booking Confirmed!\n"
        f"Train Name : {result['train_name']}\n"
        f"Train ID   : {result['train_id']}\n"
        f"Seat No    : {result['seat_number']}\n"
        f"Status     : {result['status']}"
    )

# =====================================
# SEAT MAP (USER SELECTION)
# =====================================
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
    booked_count = min(booked_count, len(seats))
    booked = random.sample([s["seat_no"] for s in seats], booked_count)
    for s in seats:
        if s["seat_no"] in booked:
            s["status"] = "Booked"
    return seats

# =====================================
# STREAMLIT UI
# =====================================
st.set_page_config(page_title="Agentic AI Train Booking", layout="centered")

st.title("🚆 Agentic AI Train Ticket Booking System")
st.caption("CN7050 – Intelligent Systems Coursework (Agentic AI)")

st.markdown("### 🔁 Agents Used")
st.write("""
- OpenAI Query Understanding Agent (Simulated)
- Train Search Agent
- Seat Availability Agent
- User Seat Selection (UI)
- Notification Agent
""")

st.markdown("### 🧾 User Input")
user_text = st.text_input("Natural Language Request", "Chennai to Bangalore sleeper ticket venum")
source = st.selectbox("Source", ["Chennai", "Bangalore", "Hyderabad", "Coimbatore"])
destination = st.selectbox("Destination", ["Bangalore", "Chennai", "Delhi", "Mumbai"])
travel_class = st.selectbox("Class", ["Sleeper", "3A", "2A"])

# Keep state for train selection + booking
if "selected_train" not in st.session_state:
    st.session_state.selected_train = None

if st.button("🔎 Search Trains"):
    st.session_state.selected_train = None  # reset selection each search

    st.markdown("## ⚙️ Agent Execution Evidence")

    # Agent 0 – OpenAI
    query = openai_query_agent(user_text, source, destination, travel_class)
    st.success("OpenAI Query Understanding Agent ✔")
    st.json(query)

    # Agent 1 – Train Search
    trains = train_search_agent(query)
    st.info(f"Train Search Agent ✔ | Trains Found: {len(trains)}")

    if len(trains) > 0:
        st.dataframe(
            trains[["train_id", "train_name", "source", "destination", "class", "seat_available"]].head(10),
            use_container_width=True
        )

    # Agent 2 – Seat Availability
    available = seat_availability_agent(trains)
    st.info(f"Seat Availability Agent ✔ | Available Trains: {len(available)}")

    if len(available) == 0:
        st.error("❌ No seats available for this route/class.")
    else:
        # Let user pick a train (like real apps)
        st.markdown("## 🚉 Select Train to Book")

        available = available.head(10).copy()
        available["display"] = available.apply(
            lambda r: f"{r.train_name} | ID:{r.train_id} | Seats:{int(r.seat_available)}",
            axis=1
        )

        chosen = st.radio("Choose a train", available["display"].tolist())
        st.session_state.selected_train = available[available["display"] == chosen].iloc[0].to_dict()

        st.success("Train Selected ✔")
        st.write(st.session_state.selected_train)

# Seat selection section appears only if a train is selected
if st.session_state.selected_train is not None:
    st.markdown("---")
    st.header("🪑 Seat Selection (User selects seat like RedBus)")

    # Create seat map each run (demo). You can persist if needed.
    seat_map = generate_seat_map(total_seats=24)
    seat_map = mark_booked_seats(seat_map, booked_count=6)

    # Show available seats only
    available_seats = [
        f"Seat {s['seat_no']} ({s['seat_type']})"
        for s in seat_map if s["status"] == "Available"
    ]

    selected_seat = st.selectbox("Select an available seat", available_seats)

    if st.button("✅ Confirm Seat Booking"):
        seat_no = selected_seat.split()[1]  # "Seat 7 (Lower)" -> "7"

        result = {
            "train_id": int(st.session_state.selected_train["train_id"]),
            "train_name": st.session_state.selected_train["train_name"],
            "seat_number": seat_no,
            "status": "Confirmed"
        }

        final_message = notification_agent(result)
        st.markdown("## 📩 Final Output")
        st.success(final_message)
