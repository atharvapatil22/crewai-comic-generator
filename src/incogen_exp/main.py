#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

# from incogen_exp.crew import ComicGenFlow
from src.incogen_exp.crew import ComicGenFlow

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(input_text):
    """
    Run the crew.
    """
    data = {
        "input_text": input_text,
        "current_year": str(datetime.now().year)
    }

    mock_flow_input = {
        "cleaned_recipe_data" : {
            "name": "Salted Onion",
            "ingredients": [{"name":"onion","quantity":"2 diced"}, {"name":"salt","quantity":"1 tbsp"}],
            "instructions" : ["step1","step2"]
        }
    }

    try:
        comic_gen_flow = ComicGenFlow(flow_input=mock_flow_input)
        # comic_gen_flow.plot()  # for visualize the flow
        flow_output = comic_gen_flow.kickoff()
        return flow_output
    

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         IncogenExp().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         IncogenExp().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         IncogenExp().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
