import os
from crewai import Crew
from crewai import Process
import os
from dotenv import load_dotenv
from datetime import datetime
import flask
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from agents import hotel_agent, flight_agent, manager_agent
from task import hotel_task, flight_task
from utils import transcribe, stt
load_dotenv() 

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    questions = transcribe("media/audio1.mp3")
    # user_question = data["question"]
    user_question = questions
    user_question = user_question + f"Note: For reference today is {datetime.now()}"


    hierarchical_crew = Crew(
    agents=[hotel_agent, flight_agent],
    tasks=[hotel_task, flight_task],
    manager_agent=manager_agent,
    process=Process.hierarchical,
        chat_llm = "gpt-4o"
    )
    
    hierarchical_flow_output = hierarchical_crew.kickoff(
        inputs={"user_question": user_question}
    )

    stt(hierarchical_flow_output.raw)

    return jsonify(hierarchical_flow_output.raw), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")