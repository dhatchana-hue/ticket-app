def notification_agent(result):
    return (
        "✅ Booking Confirmed!\n"
        f"Train Name : {result['train_name']}\n"
        f"Train ID   : {result['train_id']}\n"
        f"Seat No    : {result['seat_number']}\n"
        f"Status     : {result['status']}"
    )
