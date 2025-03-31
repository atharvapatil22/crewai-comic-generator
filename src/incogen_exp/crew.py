from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, start, listen, and_, or_
from pydantic import BaseModel,Field
from typing import List 
from crewai_tools import DallETool
import json
from openai import OpenAI
from incogen_exp.helpers import add_image_details

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# @CrewBase
# class IncogenExp():
# 	"""IncogenExp crew"""

# 	# Learn more about YAML configuration files here:
# 	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
# 	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
# 	agents_config = 'config/agents.yaml'
# 	tasks_config = 'config/tasks.yaml'

# 	# If you would like to add tools to your agents, you can learn more about it here:
# 	# https://docs.crewai.com/concepts/agents#agent-tools
# 	# @agent
# 	# def researcher(self) -> Agent:
# 	# 	return Agent(
# 	# 		config=self.agents_config['researcher'],
# 	# 		verbose=True
# 	# 	)

# 	# @agent
# 	# def reporting_analyst(self) -> Agent:
# 	# 	return Agent(
# 	# 		config=self.agents_config['reporting_analyst'],
# 	# 		verbose=True
# 	# 	)
	
# 	@agent
# 	def agent_one(self) -> Agent:
# 		return Agent(
# 			config=self.agents_config['agent_one'],
# 			verbose=True
# 		)

# 	# To learn more about structured task outputs, 
# 	# task dependencies, and task callbacks, check out the documentation:
# 	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
# 	# @task
# 	# def research_task(self) -> Task:
# 	# 	return Task(
# 	# 		config=self.tasks_config['research_task'],
# 	# 	)

# 	# @task
# 	# def reporting_task(self) -> Task:
# 	# 	return Task(
# 	# 		config=self.tasks_config['reporting_task'],
# 	# 		output_file='report.md'
# 	# 	)
# 	@task
# 	def step_id_task(self) -> Task:
# 		return Task(
# 			config=self.tasks_config['step_id_task'],
# 			output_file='report.md'
# 		)

# 	@crew
# 	def crew(self) -> Crew:
# 		"""Creates the IncogenExp crew"""
# 		# To learn how to add knowledge sources to your crew, check out the documentation:
# 		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

# 		return Crew(
# 			agents=self.agents, # Automatically created by the @agent decorator
# 			tasks=self.tasks, # Automatically created by the @task decorator
# 			process=Process.sequential,
# 			verbose=True,
# 			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
# 		)

dalle_tool = DallETool(model="dall-e-3",
  size="1024x1024",
  quality="standard",
  n=1)
class IngredientData(BaseModel):
	name: str 
	quantity: str

# Define a class for a list of story scenes
class IngredientDataList(BaseModel):
	ingedient_details: List[IngredientData]
    
class IngredientImagePrompt(BaseModel):
  name: str 
  prompt: str = Field(description = "A prompt for text to image models that can be used to generate an image.")
	
    
class IngredientsFlow1(Flow):
  def __init__(self, data):
    super().__init__()
    self.state['input_text'] = data['input_text']
    self.state['ingredients'] = []
  
  @start()
  def extract_ingredients(self):        
    task_input = self.state['input_text']
    
    ingredient_extractor_agent = Agent(
      role="Ingredient Extractor",
      goal="Identify and extract ingredients along with their quantities from the given input text.",
      backstory='''You are a text-processing expert specializing in extracting structured data from unstructured text.
      Given a recipe ingredient list, you identify each ingredient and its associated quantity with high accuracy.''',
      verbose=True
    )
    
    igredient_extraction_task = Task(
      description=f'''Analyze the given input text containing a list of ingredients.
      INPUT TEXT: {task_input}
      Your job is to extract each ingredient along with its quantity. Ensure that all ingredients
      are correctly identified and formatted in a structured manner.''',
      agent=ingredient_extractor_agent,
      expected_output="A structured list of ingredients with quantities",  
      output_file="ingredients.json",  
      output_pydantic=IngredientDataList
    )
    
    crew = Crew(
      agents=[ingredient_extractor_agent],
      tasks=[igredient_extraction_task],
      verbose=True,
      process=Process.sequential
    )
    
    result = crew.kickoff()
    parsed = result.to_dict()['ingedient_details']
	
    ingredients = {}
    for obj in parsed:
      ingredients[obj['name']] = {'quantity': obj['quantity']}
    self.state['ingredients'] = ingredients

    print('\n\nSTATE UPDATED',self.state['ingredients'])
		
  @listen(extract_ingredients)
  def generate_prompts(self):  
  
    prompt_generation_agent = Agent(
      role="Image Prompt Creator",
      goal="Create image generation prompts in the style of comic art for each ingredient.",
      backstory="You are an AI-powered creator with deep knowledge of recipes and ingredients. Your task is to create a image generation prompt of a food ingredient. The prompt will be used by a image generation tool to generate a representative image for the ingredient. The images that you generate will be used in a recipe book.",
      verbose=True
    )
    
    prompt_generation_task = Task(
      description=f'''You are given an ingredient name: {'{name}'}. 
      Generate a prompt  which can be used by a text to image model to generate an image for the ingredient. The prompt should be in less than 50 words.
      You are also given the quantity ({'{quantity}'}) of the ingredient. If it is feasable, you may incorporate this in the prompt.
      The prompt should be about the ingredient with a blank or simple background''',
      agent=prompt_generation_agent,
      expected_output="A prompt for the image generation model. And the {'{name}'} of the ingredient for which prompt was generated",
      output_pydantic=IngredientImagePrompt, 
    )
    
    crew = Crew(
      agents=[prompt_generation_agent],
      tasks=[prompt_generation_task],
      verbose=True,
      process=Process.sequential
    )
    
    ingredient_inputs = [{"name": key,'quantity':value['quantity']} for key, value in self.state['ingredients'].items()]
    
    results = crew.kickoff_for_each(inputs=ingredient_inputs)

    for result in results:
      parsed = json.loads(result.raw)
      # Add each prompt to the respective ingredient dict in the state
      self.state['ingredients'][parsed['name']]['prompt'] = parsed['prompt']

    print('\n\nSTATE UPDATED',self.state['ingredients'])

  @listen(generate_prompts)
  def generate_images(self):

    client = OpenAI()

    for key, value in self.state['ingredients'].items():
      response = client.images.generate(
        model="dall-e-3",
        prompt=value['prompt'],
        n=1,
        size="1024x1024"
      )
      self.state['ingredients'][key]['dalle_image_url'] = response.data[0].url

      # Styled image will have name and quantity written over it
      styled_image = add_image_details(response.data[0].url,key,value['quantity'])
      self.state['ingredients'][key]['styled_image'] = styled_image

    print('\n\nSTATE UPDATED',self.state['ingredients'])


    
		
		
		