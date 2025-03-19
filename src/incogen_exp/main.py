#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from incogen_exp.crew import IngredientsFlow1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    data = {
        "input_text": '''For the Pasta:

    12 oz (340g) pasta (penne or fettuccine works well)
    2 tbsp olive oil or butter

For the Protein (Optional):

    1 lb (450g) chicken breast or shrimp, sliced
    1 tsp Cajun seasoning (for seasoning the protein)

For the Sauce:

    2 tbsp butter
    3 cloves garlic, minced
    1 bell pepper (red, yellow, or green), sliced
    ½ onion, sliced
    1 cup heavy cream
    1 cup chicken broth (or vegetable broth)
    ½ cup Parmesan cheese, grated
    1 tbsp Cajun seasoning (adjust to taste)
    ½ tsp smoked paprika (optional for extra smokiness)
    Salt and black pepper to taste
    ½ tsp red pepper flakes (optional for extra spice)
''',
        "current_year": str(datetime.now().year)
    }
    
    try:
        ing_flow = IngredientsFlow1(data=data)
        # ing_flow.plot()  # for visualize the flow
        ing_flow.kickoff()
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
