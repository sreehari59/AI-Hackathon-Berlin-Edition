from crewai import Agent, Task, Crew
from tools import hotel_search_tool, flight_search_tool
from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv() 

llm=LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

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