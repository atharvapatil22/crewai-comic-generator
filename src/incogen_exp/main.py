#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from incogen_exp.crew import IncogenExp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'input_text': '''How to Prepare a Butterflied Spatchcocked Chicken

    Remove backbone: To prepare chicken turn the chicken breast side down on a cutting board. Cut spine from chicken using heavy duty kitchen shears, trim down both sides of the backbone from end to end to it remove completely (reserve in fridge for chicken stock if desired).

Whole chicken with spine cut out.

    Butterfly the chicken open.
    Optional tip: Optionally for ease in flattening chicken in the next step you can make a small cut down the upper center of it (the sternum) before turning the chicken. Trim excess visible fat from the chicken, season inside the chicken with salt and pepper.

Butterflied whole chicken.

Turn and flatten chicken: Turn chicken to opposite side, use the heel of your hand forcefully press between the center of the chicken breasts to flatten the chicken (if needed use a second hand over the first for extra added pressure).Breaking bone for spatchcock chicken.
Make herb butter: In a mixing bowl using a spatula stir together butter, 1 1/2 tsp each garlic, thyme and rosemary. Season with salt and pepper to taste (I use about 3/4 tsp salt and 1/4 tsp pepper).

Rub butter under chicken skin: Using the back of a spatula or your finger separate the skin from the chicken to create a pocket for the butter (start at the neck and run down near the opposite end but not all the way through or butter will melt out). Also do this for the thighs.

Dab over the chicken skin to dry with paper towels.

Butter garlic herb mixture for roast chicken.
How to Cook Spatchcock Chicken on a Sheet Pan

Prepare oven and baking pan: Preheat oven to 425 degrees. Spray an 18 by 13 inch baking sheet with non-stick cooking spray or line with parchment paper.

Place spatchcock chicken on pan, season: Transfer the chicken to prepared baking sheet breast side up, turn and tuck the wings tips under the chicken. Season the chicken evenly with paprika, salt and pepper to taste.

Season vegetables, spread around chicken: In a large mixing bowl toss together potatoes, carrots, remaining garlic, rosemary and thyme, salt and pepper to taste and olive oil.

Spread vegetables around chicken (you can use space under neck area and under wingtips if needed).

Spatchcock chicken and vegetables on a baking sheet shown before roasting.

How long to bake: Roast in oven until chicken breasts are 160 to 165 in center on an instant read food thermometer (thighs should be at least 165 degrees, but it’s okay if thighs are hotter. The chicken breasts you don’t want past that temperature or they’ll dry out), about 50 to 60 minutes.

Vegetable tip: If needed you can toss the vegetables around 30 minutes if they are beginning to brown.

Let rest and slice: Tent with foil and let chicken rest 10 minutes before carving (for juicier chicken). Garnish everything with parsley and serve with lemon wedges for spritzing over chicken and vegetables.

Spatchcock chicken and veggies on baking sheet shown after roasting.
How to Store

    Any leftover chicken and vegetables can be stored in the fridge for up to 3 days.
    Rewarm individual servings in the microwave on 50% power until warmed through, or warm in a skillet with a little oil.
    It is not recommended to freeze this recipe as the potatoes will become mushy. You can however freeze leftover roasted spatchcock chicken for up to 3 months.
    I recommend using leftover chicken carcass and the backbone for homemade chicken stock.
''',
        'current_year': str(datetime.now().year)
    }
    
    try:
        IncogenExp().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        IncogenExp().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        IncogenExp().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        IncogenExp().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
