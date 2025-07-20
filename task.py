from crewai import Task
from agents import hotel_agent, flight_agent
from tools import hotel_search_tool, flight_search_tool

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