def openai_query_agent(text, source, destination, travel_class):
    return {
        "intent": "BOOK_TICKET",
        "source": source,
        "destination": destination,
        "class": travel_class,
        "original_text": text
    }
