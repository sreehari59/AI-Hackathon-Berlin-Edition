from crewai.tools import tool
from serpapi import GoogleSearch

@tool("Flight Search Tool")
def flight_search_tool(query:str, departure_id, arrival_id, outbound_date, return_date):
    """Search flight given the query."""
    params = {
        "engine": "google_flights",
        "departure_id": "PEK",
        "arrival_id": "AUS",
        "outbound_date": "2025-07-19",
        "return_date": "2025-07-25",
        "currency": "USD",
        "hl": "en",
        "api_key": "secret_api_key"
        }
    search = GoogleSearch(params)
    results = search.get_dict()
    flight_details = []
    
    for flight_group in j.get("best_flights"):
        for flight in flight_group.get("flights"):
            airline_name = flight.get("airline")
            duration = flight.get("duration")
            airplane = flight.get("airplane")
            travel_class = flight.get("travel_class")

            flight_details.append((duration, airplane, airline_name, travel_class))
    return flight_details

@tool("Hotel Search Tool")
def hotel_search_tool(query: str, check_in_date: str,
                    check_out_date: str, adults:str) -> list:
    """Search hotels given the query, check_in_date, check_out_date, adults."""

    missing = []
    if not query:
        missing.append("query")
    if not check_in_date:
        missing.append("check_in_date")
    if not check_out_date:
        missing.append("check_out_date")
    if not adults:
        missing.append("adults")
    if missing:
        return f"Missing information: {', '.join(missing)}"

    else:
        params = {
            "engine": "google_hotels",
            "q": query,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": adults,
            "currency": "USD",
            "gl": "us",
            "hl": "en",
            "api_key": os.getenv("SERP_API")
            }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        hotel_details = [(hotel["name"], hotel["overall_rating"],
                    hotel["price"], hotel["amenities"]) for hotel in results["ads"]]
        return hotel_details