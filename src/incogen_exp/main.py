#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from incogen_exp.crew import StoryCrew,ArtistCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    # Creating hypothesis or generating questions using QuestCrew
    inputs = {
        'number_of_scenes': int(4),
        'story_text': "Once upon a time, there lived a mighty lion named Bhasuraka, who terrorized the jungle. The animals, tired of his tyranny, decided to send him a prey every day. One day, it was a clever rabbit’s turn, and he devised a plan to rid the jungle of the lion. He led Bhasuraka to a deep well, convincing him that another lion lived there. Bhasuraka, seeing his reflection in the water, roared in anger and jumped into the well, never to return.",
    }

    scenes_list = StoryCrew().crew().kickoff(inputs=inputs)


    if scenes_list is not None:        
        print(f"Raw result from script writing: {scenes_list.raw}")

    slist = scenes_list.pydantic
    story_summary = slist.summary
    for scene in slist.scenes:
        print(f"Scene: {scene.narration}") 

    scene_input = [{ "story_summary": story_summary,
        'scene_description': scene.narration} for i, scene in enumerate(slist.scenes)]


    # Run the agent
    result_images = ArtistCrew().crew().kickoff_for_each(inputs = scene_input)

    print("result_images : {result_images.raw}")