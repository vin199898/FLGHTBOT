import requests

# Telegram bot details
telegram_token = "7902340671:AAEfawBJ8VG-KRO_h-Ey8-pekKRssfnTYp0"  # Replace with your bot's API token
chat_id = "-4770523196"  

# Function to send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  # Optional: Use Markdown formatting
    }
    requests.get(url, params=params)

# API details
url = "https://sky-flights.p.rapidapi.com/fly-to-country"
headers = {
    "x-rapidapi-key": "920483404emshda44bffa1a696e7p10d222jsn75c54104e428",
    "x-rapidapi-host": "sky-flights.p.rapidapi.com",
    "Accept": "application/json"
}

# Define multiple routes
routes = [
    {
        "route_name": "HKT → SIN → BKK",  # First route
        "queries": [
            {"adults": "1", "locale": "en-US", "currency": "SGD", "market": "SG",
             "origin": "HKT", "destination": "SIN", "departureDate": "2025-01-21", "returnDate": ""},
            {"adults": "1", "locale": "en-US", "currency": "SGD", "market": "SG",
             "origin": "SIN", "destination": "BKK", "departureDate": "2025-01-28", "returnDate": ""}
        ]
    },
    {
        "route_name": "SIN → HKG → TPE",  # Second route
        "queries": [
            {"adults": "1", "locale": "en-US", "currency": "SGD", "market": "SG",
             "origin": "SIN", "destination": "HKG", "departureDate": "2025-02-05", "returnDate": ""},
            {"adults": "1", "locale": "en-US", "currency": "SGD", "market": "SG",
             "origin": "HKG", "destination": "TPE", "departureDate": "2025-02-10", "returnDate": ""}
        ]
    }
]

# Process each route
final_message = ""
for route in routes:
    final_message += f"*{route['route_name']}*\n\n"
    
    for query in route['queries']:
        response = requests.get(url, headers=headers, params=query)
        data = response.json()

        # Extract flight details
        flights_info = []
        for flight in data.get('data', {}).get('itineraries', [])[:3]:  # Top 3 results
            price = flight.get('price', {}).get('raw', None)
            if price:
                departure = flight['legs'][0].get('departure', 'N/A')
                arrival = flight['legs'][0].get('arrival', 'N/A')
                carrier = flight['legs'][0]['carriers']['marketing'][0].get('name', 'N/A')
                origin = flight['legs'][0]['origin']['displayCode']
                dest = flight['legs'][0]['destination']['displayCode']

                flights_info.append(f"*Price:* ${price}\n"
                                    f"*{origin} → {dest}*\n"
                                    f"Departure: {departure}\n"
                                    f"Arrival: {arrival}\n"
                                    f"Carrier: {carrier}\n"
                                    + "-" * 40)

        final_message += "\n".join(flights_info) + "\n\n"

# Send message to Telegram
send_telegram_message(final_message)
