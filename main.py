import requests

url = "https://sky-flights.p.rapidapi.com/fly-anywhere"

# Define the queries for the two legs
queries = [
    {"currency": "USD", "adults": "1", "market": "US", "returnDate": "2025-07-18", "locale": "en-US", "origin": "HKT", "departureDate": "2025-07-05"},
    {"currency": "USD", "adults": "1", "market": "US", "returnDate": "2025-07-25", "locale": "en-US", "origin": "SIN", "departureDate": "2025-07-18"}
]

headers = {
    "x-rapidapi-key": "920483404emshda44bffa1a696e7p10d222jsn75c54104e428",
    "x-rapidapi-host": "sky-flights.p.rapidapi.com",
    "Accept": "application/json"
}

flights_info = []

for query in queries:
    response = requests.get(url, headers=headers, params=query)
    data = response.json()

    # Extract flight details
    for flight in data.get('flights', [])[:3]:
        price = flight.get('price', {}).get('amount', 'N/A')
        origin = flight.get('origin', {}).get('id', 'N/A')
        destination = flight.get('destination', {}).get('id', 'N/A')
        departure = flight.get('departure', 'N/A')
        arrival = flight.get('arrival', 'N/A')
        flights_info.append(f"Price: ${price}\nFrom: {origin}\nTo: {destination}\nDeparture: {departure}\nArrival: {arrival}\n\n")

# Send results to Telegram Bot
import telegram

bot_token = '7902340671:AAEfawBJ8VG-KRO_h-Ey8-pekKRssfnTYp0'
chat_id = '-4770523196'
message = "\n".join(flights_info)

bot = telegram.Bot(token=bot_token)
bot.send_message(chat_id=chat_id, text=message)
