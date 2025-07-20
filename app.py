import os
from crewai import Agent, Task, Crew
from crewai import Process
from crewai.tools import tool
from crewai import LLM
import os
from dotenv import load_dotenv
from datetime import datetime
from serpapi import GoogleSearch
import Flask
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
load_dotenv() 

app = Flask(__name__)
CORS(app)

llm=LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

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


hotel_agent = Agent(
    role="Hotel Agent",
    goal="Perform a hotel search, get hotel pricing, hotel reservation based on the user requirement.",  
    allow_delegation=False, # Allow agents to delegate task to other agents
    verbose=True,
    llm=llm, # Language model that powers the agent
    backstory=(
        """
        The Hotel Agent is skilled in helping the user with any information related to hotel.
        From hotel searching, hotel reservation to hotel booking
        """
    ), # Providing context and personality to the agent
    tools=[hotel_search_tool]
)

flight_agent = Agent(
    role="Flight Agent",
    goal="Perform a flight search, get flight pricing, flight booking based on the user requirement.",  
    allow_delegation=False, 
    verbose=True,
    llm=llm,
    backstory=(
        """
        The flight Agent is skilled in helping the user with any information related to flight.
        From flight searching, flight booking
        """
    ),
    tools=[flight_search_tool]
)

summarizing_agent = Agent(
    role="Summarizing Agent",
    goal="Give a Summary based on the what the user actaully wants. To the point",  
    allow_delegation=False, 
    verbose=True,
    llm=llm,
    backstory=(
        """
        The summarizing agent is skilled in helping the user summarizing the result
        It would give the answer only what is required
        """
    )
)

    # A list of relevant hotels as dictionaries with the following keys:
    # - name: str
    # - rating: float
    # - price: str
    # - amenities: list of str


hotel_task = Task(
    description=(
    """
    Understand the user query: '{user_question}'.
    Extract the following information from the user query:
    - query (the hotel search query or destination)
    - check_in_date (in YYYY-MM-DD format)
    - check_out_date (in YYYY-MM-DD format)
    - number of adults (as a number)

    If all four parameters are found, call the Hotel Search Tool with those values and provide a 
    a relevant answer that directly addresses the user's question.
    If any value is missing or ambiguous, do not call the tool and instead respond with: "Can you please once again share the
    location, check in date, check out date and number of adults information". Then return control to the manager.
    """
    ),
    expected_output="""
    A relevant answer that directly addresses the user's question.

    Example:
    [
        {
            "final_answer": "A relevant answer that directly addresses the user's question."
        },
        {
            "name": "Holiday Inn Express & Suites Potsdam by IHG",
            "rating": 4.2,
            "price": "$128",
            "amenities": ["Pet-friendly", "Child-friendly", "Restaurant", "Bar", "Free breakfast", "Air conditioning"]
        }
    ]

    If data is missing:
    'Missing information: check_in_date, number of adults'
    """,
    tools=[hotel_search_tool],
    agent=hotel_agent,
)


flight_task = Task(
    description=(
    """
    Understand the user query: '{user_question}'.
    
    # Extract the following information from the user query:
    # - query (the hotel search query or destination)
    # - check_in_date (in YYYY-MM-DD format)
    # - check_out_date (in YYYY-MM-DD format)
    # - number of adults (as a number)

    If all four parameters are found, call the Hotel Search Tool with those values.
    Provide a structured list of hotel results formatted as dictionaries.
    If any value is missing or ambiguous, do not call the tool and instead respond with: "Can you please once again share the
    location, check in date, chek out date and number of adults information". Then return control to the manager.
    """
    ),
    expected_output="""
    A relevant answer that directly addresses the user's question.
    A list of relevant hotels as dictionaries with the following keys:
    - name: str
    - rating: float
    - price: str
    - amenities: list of str

    Example:
    [
        {
            "final_answer": "A relevant answer that directly addresses the user's question."
        }
        {
            "name": "Holiday Inn Express & Suites Potsdam by IHG",
            "rating": 4.2,
            "price": "$128",
            "amenities": ["Pet-friendly", "Child-friendly", "Restaurant", "Bar", "Free breakfast", "Air conditioning"]
        },
        ...
    ]
    """,
    tools=[flight_search_tool],
    agent=flight_agent,
)
 
 
summarizing_task = Task(
    description=(
    """
    Understand the user query: '{user_question}'.
    You would also get the response from the either flight or hotel agent.

    Based on this information, interpret the user's intent and provide a concise, relevant, and direct 
    response that addresses their original question.
    """
    ),
    expected_output="""
    A brief and relevant answer that directly addresses the user's question.

    Example1:
    {
        "output": "Here are some hotel options in Berlin for your stay from August 1st to August 3rd."
    }
    
    OR
    
    Example2:
    {
        "output": "The best hotel in Berlin is Hyatt "
    }
        
    """,
    tools=[],
    agent=summarizing_agent,
)


manager_agent = Agent(
    role="Master Agent",
    goal="""understand the user question, based on the understanding delegate the task to:
        1. hotel_agent if it anything related to hotel
        2. flight_agent if it is anything related to flight

        Finally give a brief and relevant answer that directly addresses the user's question.
    """,
    backstory="""
    As the Master Agent, you are the central coordinator of a smart travel concierge system. 
    You have a deep understanding of user intent and are highly skilled at analyzing natural language queries.

    Your primary role is to interpret each user request accurately and determine the appropriate course of action. 
    You are calm, efficient, and precise—like a world-class travel planner. 
    You dont answer questions directly; instead, you route the request to the best-suited specialist agent:

    - If the query is related to hotel bookings, room availability, or amenities, you delegate it to the hotel_agent.
    - If the query is about flights, schedules, or air travel arrangements, you delegate it to the flight_agent.
    
    If any essential information is missing for the task to proceed (such as travel dates, destinations, or number of travelers), 
    you ensure the appropriate agent prompts the user for clarification or follow-up.

    You are trusted to manage the flow of tasks intelligently, ensuring users get fast, relevant, and well-organized help.
    Finally give a brief and relevant answer that directly addresses the user's question.
    """,
    allow_delegation=False,
    max_retry_limit=1,
    cache=True,
    verbose=True,
    llm=llm,
)

# 3. summarizing agent is the agent which gets the final response from either hotel or flight agent
# - If the output or response is from flight_agent ot hotel_agent then delegate to summarizing_agent

hierarchical_crew = Crew(
    agents=[hotel_agent, flight_agent],
    tasks=[hotel_task, flight_task],
    manager_agent=manager_agent,
    process=Process.hierarchical,
    chat_llm = "gpt-4o"
)


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_question = data["question"]
    user_question = user_question + f"Note: For reference today is {datetime.now()}"
    hierarchical_flow_output = hierarchical_crew.kickoff(
        inputs={"user_question": user_question}
    )

    return jsonify(hierarchical_flow_output.raw), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")