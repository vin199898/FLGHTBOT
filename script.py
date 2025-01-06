import requests

# Telegram bot details
telegram_token = "7902340671:AAEfawBJ8VG-KRO_h-Ey8-pekKRssfnTYp0"  # Replace with your bot's API token
chat_id = "-4770523196"  # Replace with your Telegram chat ID


# Function to send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  # Optional: Use Markdown formatting
    }
    response = requests.get(url, params=params)
    return response

# API details
url = "https://sky-scanner3.p.rapidapi.com/flights/search-multi-city"

# Payload for multi-city search
payload = {
    "market": "TH",  # Singapore market
    "locale": "en-US",
    "currency": "THB",  # Currency in SGD
    "adults": 1,
    "children": 0,
    "infants": 0,
    "cabinClass": "economy",
    "stops": ["direct"],  # Allowing direct and 1-stop flights
    "sort": "cheapest_first",     # Sort by cheapest first
    "flights": [
        {
            "fromEntityId": "HKT",  # Outbound: HKT → SIN
            "toEntityId": "SIN",
            "departDate": "2025-03-29"  # Outbound date
        },
        {
            "fromEntityId": "SIN",  # Return: SIN → BKK
            "toEntityId": "BKK",
            "departDate": "2025-04-03"  # Return date
        }
    ]
}

headers = {
    "x-rapidapi-key": "920483404emshda44bffa1a696e7p10d222jsn75c54104e428",
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Get response from API
response = requests.post(url, json=payload, headers=headers)
data = response.json()

# Extract flight details
flights_info = []
for flight in data.get('data', {}).get('itineraries', [])[:3]:  # Top 3 results
    price = flight.get('price', {}).get('raw', None)
    if price:
        # First leg: HKT → SIN
        leg1 = flight['legs'][0]
        leg1_depart = leg1.get('departure', 'N/A')
        leg1_arrive = leg1.get('arrival', 'N/A')
        leg1_carrier = leg1['carriers']['marketing'][0].get('name', 'N/A')
        leg1_origin = leg1['origin']['displayCode']
        leg1_dest = leg1['destination']['displayCode']

        # Second leg: SIN → BKK
        leg2 = flight['legs'][1]
        leg2_depart = leg2.get('departure', 'N/A')
        leg2_arrive = leg2.get('arrival', 'N/A')
        leg2_carrier = leg2['carriers']['marketing'][0].get('name', 'N/A')
        leg2_origin = leg2['origin']['displayCode']
        leg2_dest = leg2['destination']['displayCode']

        flights_info.append({
            'price': price,
            'leg1_depart': leg1_depart,
            'leg1_arrive': leg1_arrive,
            'leg1_carrier': leg1_carrier,
            'leg1_origin': leg1_origin,
            'leg1_dest': leg1_dest,
            'leg2_depart': leg2_depart,
            'leg2_arrive': leg2_arrive,
            'leg2_carrier': leg2_carrier,
            'leg2_origin': leg2_origin,
            'leg2_dest': leg2_dest
        })

# Format message for Telegram
message = "Top 3 Multi-City Flights (HKT → SIN → BKK):\n\n"
for flight in flights_info:
    message += f"*Price:* THB {flight['price']}\n\n"

    message += "*Leg 1: HKT → SIN*\n"
    message += f"  Departure: {flight['leg1_depart']} ({flight['leg1_origin']})\n"
    message += f"  Arrival: {flight['leg1_arrive']} ({flight['leg1_dest']})\n"
    message += f"  Carrier: {flight['leg1_carrier']}\n\n"

    message += "*Leg 2: SIN → BKK*\n"
    message += f"  Departure: {flight['leg2_depart']} ({flight['leg2_origin']})\n"
    message += f"  Arrival: {flight['leg2_arrive']} ({flight['leg2_dest']})\n"
    message += f"  Carrier: {flight['leg2_carrier']}\n"
    message += "-" * 40 + "\n"

# Send message to Telegram
send_telegram_message(message)






































