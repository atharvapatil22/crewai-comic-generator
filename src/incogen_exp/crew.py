from crewai import Agent, Crew, Process, Task
from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel,Field
from typing import List 
from crewai_tools import DallETool
import json
from openai import OpenAI
from incogen_exp.helpers import add_image_details
from PIL import Image, ImageOps

# This variable cotrols the limit of ingredients. To ensure that the Image Generation API is not abused
INGREDIENTS_LIMIT = 24

dalle_tool = DallETool(model="dall-e-2",
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
	
    
class ComicGenFlow(Flow):
  def __init__(self, data):
    super().__init__()
    self.state['input_text'] = data['input_text']
    self.state['ingredients'] = []
  
  # THE COMMENTED PART WILL BE TAKEN OVER BY PREPROCESSING FLOW

  # (1) Extract Ingredients from input text
  # @start()
  # def extract_ingredients(self):        
  #   task_input = self.state['input_text']
    
  #   ingredient_extractor_agent = Agent(
  #     role="Ingredient Extractor",
  #     goal="Identify and extract ingredients along with their quantities from the given input text.",
  #     backstory='''You are a text-processing expert specializing in extracting structured data from unstructured text.
  #     Given a recipe ingredient list, you identify each ingredient and its associated quantity with high accuracy.''',
  #     verbose=True
  #   )
    
  #   igredient_extraction_task = Task(
  #     description=f'''Analyze the given input text containing a list of ingredients.
  #     INPUT TEXT: {task_input}
  #     Your job is to extract each ingredient along with its quantity. Ensure that all ingredients
  #     are correctly identified and formatted in a structured manner.''',
  #     agent=ingredient_extractor_agent,
  #     expected_output="A structured list of ingredients with quantities",  
  #     output_file="ingredients.json",  
  #     output_pydantic=IngredientDataList
  #   )
    
  #   crew = Crew(
  #     agents=[ingredient_extractor_agent],
  #     tasks=[igredient_extraction_task],
  #     verbose=True,
  #     process=Process.sequential
  #   )
    
  #   result = crew.kickoff()
  #   parsed = result.to_dict()['ingedient_details']
	
  #   ingredients = {}
  #   for obj in parsed:
  #     ingredients[obj['name']] = {'quantity': obj['quantity']}
  #   self.state['ingredients'] = ingredients

  #   print('\n\nSTATE UPDATED',self.state['ingredients'])

  # # (1b) Check Ingredients LIMIT
  # @router(extract_ingredients)
  # def ingredient_limit_check(self):
      
  #   # Handle Ingredients LIMIT CHECK
  #   if len(self.state['ingredients']) > 24:
  #     return "FAIL"
  #   else:
  #     return "PASS"
      
  # @listen("FAIL")
  # def exit_flow(self):
  #   return "LIMIT_EXCEEDED"
		
  # (1) Generate image prompts for (i)Cover page, (ii) List of ingredients and (iii) List of instructions
  @start
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

  # (2) Generate DallE images using all the prompts
  @listen(generate_prompts)
  def generate_images(self):

    client = OpenAI()
    idx = 1

    for key, value in self.state['ingredients'].items():
      response = client.images.generate(
        model="dall-e-2",
        prompt=value['prompt'],
        n=1,
        size="512x512"
      )
      self.state['ingredients'][key]['dalle_image_url'] = response.data[0].url

      print(f'\n\nIngredient image generated ({idx})\n',response.data[0].url)
      idx+=1

      # Styled image will have name and quantity written over it
      styled_image = add_image_details(response.data[0].url,key,value['quantity'])
      self.state['ingredients'][key]['styled_image'] = styled_image

    print('\n\nSTATE UPDATED',self.state['ingredients'])


  # (3) Merge all the images to create comic pages
  @listen(generate_images)
  def merge_images(self):

    rows, cols = 4, 3  # Grid layout
    images_per_page = rows * cols  # 12 images per page
    img_size = 1024  # Each original image is 1024x1024
    border_size = 5
    margin = 20  # Space between images

    # Compute new size per image including borders
    img_with_border_size = img_size + 2 * border_size

    # Compute final image dimensions
    total_width = cols * img_with_border_size + (cols + 1) * margin
    total_height = rows * img_with_border_size + (rows + 1) * margin

    ingredient_images = [value['styled_image'] for value in self.state['ingredients'].values()]
    total_images = len(ingredient_images)
    num_pages = (total_images + images_per_page - 1) // images_per_page  # Round up

    pages = []  # List to store all generated pages

    for page in range(num_pages):
      # Create a blank image for this page
      page_image = Image.new("RGB", (total_width, total_height), "white")

      # Get the images for this page
      start_idx = page * images_per_page
      end_idx = min(start_idx + images_per_page, total_images)
      current_batch = ingredient_images[start_idx:end_idx]

      for idx, img in enumerate(current_batch):
        row, col = divmod(idx, cols)

        # Add black border
        img_with_border = ImageOps.expand(img, border=border_size, fill="black")

        # Compute position including margin
        x_offset = margin + col * (img_with_border_size + margin)
        y_offset = margin + row * (img_with_border_size + margin)

        # Paste into the current page
        page_image.paste(img_with_border, (x_offset, y_offset))

      # page_image.show()
      pages.append(page_image)  # Store this page

    return pages

    
		
		
		