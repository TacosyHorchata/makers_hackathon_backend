from openai import OpenAI
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI()    

desiredOutputTest = [
        {
            "type": "function",
            "function": {
                "name": "get_data",
                "description": "Extract relevant data of a document and convert it to json",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fecha": {
                            "description": "The date in the invoice",
                        },
                        "id_invoice": {
                            "description": "The invoice id",
                        },
                        "lista_productos": { 
                            "description": "Lista de productos"
                        },
                    },
                    "required": [],
                },
            },
        },
    ]
extractedPdfTest = ''' '''
desiredOutputTest2 = { "fecha":"The date in the invoice",
                      "id_invoice":  "The invoice id",
                      "lista_productos": "Lista de productos"
                    },


def gpt_request_completions(extractedPdf, desiredOutput):

    nullExample = {"fecha":  "null", "direccion de destino": "null"}

    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "system", "content": f"You are an assistant meant to extract relevant data from a text to json, is very important that you stick to structure of the desired json, only parse the fields in the desired json. \n If the json includes a list, such as a 'products list', return an array of very short objects with the most important properties of each product/service/item. \n \n The desired json is: \n {desiredOutput} \n\n if there is any missing value, return 'null'. Example: \n {nullExample}"},{"role": "user", "content":f"This is the text to be converted:\n{extractedPdf}"} ]
    #tools = desiredOutput
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        response_format={ "type": "json_object" }
        #tools=tools,
        #tool_choice={"type": "function", "function": {"name": "get_data"}},  # auto is default, but we'll be explicit
    )
    res = response.choices[0].message.content.replace('\'', '"')
    res = re.sub(r"(\w)\"(\w)", r"\1'\2", res)

    return res