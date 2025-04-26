from pydantic import BaseModel
from typing import List

# All the pydantic models required by the ComicGenFlow are defined here

# 1) Suplimentary state models - These are required by the main state models

class IngredientData(BaseModel):
  name: str
  quantity: str

class ImageObject(BaseModel):
  prompt: str
  url: str
  styled_image: str

# 2) Main state models - These models will be used by the internal state of the flow

class RecipeData(BaseModel):
  name: str
  ingredients: List[IngredientData]
  instructions: List[str]

class ImagesData(BaseModel):
  cover_page: ImageObject
  ingredient_images: List[ImageObject]
  instruction_images: List[ImageObject]

# 3) Agent/Tast models - These are required for some agents or tasks in the flow