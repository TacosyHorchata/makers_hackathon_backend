from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "give the html and css to replicate the following layout"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://i.ibb.co/WcRRYFR/final.png",
          },
        },
      ],
    }
  ],
  max_tokens=2000,
)

print(response)