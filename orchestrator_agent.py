# orchestrator_agent.py

import asyncio
from openai_client import get_trip_plan

# Stub for future specialized functions:
# async def find_flight(details): ...
# async def find_hotel(details): ...
# async def recommend_things(details): ...
# async def calculate_budget(details): ...

async def orchestrate_trip(conversation: str):
    """
    This acts as the 'Orchestrator Agent'.
    It will (for now) call GPT for the plan,
    but is ready for future multi-agent calls.
    """
    # TODO: In future, parse conversation with GPT to extract intent
    # e.g., destination, dates, preferences
    # TODO: Based on parsed intent, initiate sub-agents

    # For now: Single call to GPT-4, but stub the structure.
    trip_plan = await get_trip_plan(conversation)

    return {
        "itinerary": trip_plan,
        # TODO: Add more structured outputs once specialized agents are in place
    }

