import requests

# API URL
url = "https://sky-flights.p.rapidapi.com/fly-anywhere"

# Query parameters for the first leg: HKT to SIN
querystring1 = {
    "currency": "USD",
    "adults": "1",
    "market": "US",
    "returnDate": "2025-01-22",
    "locale": "en-US",
    "origin": "HKT",
    "departureDate": "2025-01-21"
}

# Query parameters for the second leg: SIN to BKK
querystring2 = {
    "currency": "USD",
    "adults": "1",
    "market": "US",
    "returnDate": "2025-01-29",
    "locale": "en-US",
    "origin": "SIN",
    "departureDate": "2025-01-28"
}

# Headers with API key and host
headers = {
    "x-rapidapi-key": "920483404emshda44bffa1a696e7p10d222jsn75c54104e428",
    "x-rapidapi-host": "sky-flights.p.rapidapi.com",
    "Accept": "application/json"
}

# Function to fetch flight data
def fetch_flights(querystring):
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    flights_info = []

    # Extract relevant flight information
    if 'data' in data and 'results' in data['data']:
        for flight in data['data']['results'][:3]:  # Get the first 3 flights
            price = flight.get('price', {}).get('amount', 'N/A')
            currency = flight.get('price', {}).get('currency', 'USD')
            origin = flight.get('legs', [{}])[0].get('origin', {}).get('name', 'N/A')
            destination = flight.get('legs', [{}])[0].get('destination', {}).get('name', 'N/A')
            departure = flight.get('legs', [{}])[0].get('departure', 'N/A')
            arrival = flight.get('legs', [{}])[0].get('arrival', 'N/A')

            # Append flight info
            flights_info.append({
                'price': f"{currency} {price}",
                'origin': origin,
                'destination': destination,
                'departure': departure,
                'arrival': arrival
            })
    return flights_info

# Fetch flights for both legs
flights_leg1 = fetch_flights(querystring1)
flights_leg2 = fetch_flights(querystring2)

# Print details for leg 1: HKT to SIN
print("Leg 1: HKT to SIN")
for flight in flights_leg1:
    print(f"Price: {flight['price']}")
    print(f"Origin: {flight['origin']}")
    print(f"Destination: {flight['destination']}")
    print(f"Departure: {flight['departure']}")
    print(f"Arrival: {flight['arrival']}")
    print("-" * 40)

# Print details for leg 2: SIN to BKK
print("Leg 2: SIN to BKK")
for flight in flights_leg2:
    print(f"Price: {flight['price']}")
    print(f"Origin: {flight['origin']}")
    print(f"Destination: {flight['destination']}")
    print(f"Departure: {flight['departure']}")
    print(f"Arrival: {flight['arrival']}")
    print("-" * 40)
