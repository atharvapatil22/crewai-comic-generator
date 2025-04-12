from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import io
import base64
import os


def capitalize_first_letter(string):
  for i, char in enumerate(string):
    if char.isalpha():  # Check if the character is a letter
      # Replace the first letter with uppercase and keep the rest the same
      string = string[:i] + char.upper() + string[i + 1:]
      break
  return string

# Function will dynamically set font for dev and prod environments
def get_font(size=40):
  flask_env = os.environ.get("FLASK_ENV", "production")
  if flask_env == "development":
    return ImageFont.truetype("comic.ttf", size=size)  
  else:
    return ImageFont.truetype("DejaVuSans-Bold.ttf" , size=size)

def add_image_details(image_url,name,quantity):
  """Function to modify Ingredient Image to add name and quantity"""

  response = requests.get(image_url)
  img = Image.open(BytesIO(response.content))

  # Get the image dimensions (assume the original is 1024x1024)
  width, height = img.size

  # Format the text correctly to capitalize the first letter:

  # Name text
  text1 = capitalize_first_letter(name)
  # Quantity Text
  text2 = capitalize_first_letter(quantity)
  
  bg_color = (135, 206, 235)  # Sky Blue 
  border_color = (0, 0, 0)  # Black border color

  # Load font 
  font = get_font(size=40) 
  draw = ImageDraw.Draw(img)

  # Get the size of the text using textbbox (bounding box)
  text1_bbox = draw.textbbox((0, 0), text1, font=font)
  text1_width, text1_height = text1_bbox[2] - text1_bbox[0], text1_bbox[3] - text1_bbox[1]

  text2_bbox = draw.textbbox((0, 0), text2, font=font)
  text2_width, text2_height = text2_bbox[2] - text2_bbox[0], text2_bbox[3] - text2_bbox[1]

  # Define extra padding for the background rectangles
  padding = 50  

  # Increase the height of the background rectangles
  text1_bg_height = text1_height + padding
  text2_bg_height = text2_height + padding

  # Ensure that the total height of the image doesn't exceed 1024px
  total_text_height = text1_bg_height + text2_bg_height
  if total_text_height > height:
      # Calculate the new height for cropping
      excess_height = total_text_height - height
      img = img.crop((0, excess_height, width, height))  # Crop the top excess height
      height = img.size[1]  # Update height after cropping

  # Create a new image with the same size (1024x1024) but add text at the top and bottom
  new_image = Image.new('RGB', (width, height), (255, 255, 255))

  # Paste the original image onto the new image
  new_image.paste(img, (0, 0))

  # Create drawing context for new image
  draw = ImageDraw.Draw(new_image)

  # Add the sky blue background and text for Text 1 at the top
  draw.rectangle([0, 0, width, text1_bg_height], fill=bg_color)

  # Center the text vertically in the top rectangle
  text1_y = (text1_bg_height - text1_height) // 2
  draw.text(((width - text1_width) // 2, text1_y), text1, fill=(0, 0, 0), font=font)

  # Add a black border to the bottom of the top rectangle
  draw.line([0, text1_bg_height, width, text1_bg_height], fill=border_color, width=3)

  # Add the sky blue background and text for Text 2 at the bottom
  draw.rectangle([0, height - text2_bg_height, width, height], fill=bg_color)

  # Center the text vertically in the bottom rectangle
  text2_y = height - text2_bg_height + (text2_bg_height - text2_height) // 2
  draw.text(((width - text2_width) // 2, text2_y), text2, fill=(0, 0, 0), font=font)

  # Add a black border to the top of the bottom rectangle
  draw.line([0, height - text2_bg_height, width, height - text2_bg_height], fill=border_color, width=3)

  return new_image

def image_to_base64(image):
  """Converts a PIL Image to a base64 string."""
  buffered = io.BytesIO()
  image.save(buffered, format="JPEG")  
  img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
  return img_str