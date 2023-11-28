import os
from openai import OpenAI
import json
import re
import time

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

def strict_output(system_prompt, user_prompt, output_format, default_category = "", output_value_only = False,
                  model = 'gpt-3.5-turbo-16k', temperature = 0, num_tries = 2, verbose = False):
    
    ''' Ensures that OpenAI will always adhere to the desired output json format. 
    Uses rule-based iterative feedback to ask GPT to self-correct.
    Keeps trying up to num_tries it it does not. Returns empty json if unable to after num_tries iterations.
    If output field is a list, will treat as a classification problem and output best classification category.
    Text enclosed within < > will generated by GPT accordingly'''

    # if the user input is in a list, we also process the output as a list of json
    list_input = isinstance(user_prompt, list)
    # if the output format contains dynamic elements of < or >, then add to the prompt to handle dynamic elements
    dynamic_elements = '<' in str(output_format)
    # if the output format contains list elements of [ or ], then we add to the prompt to handle lists
    list_output = '[' in str(output_format)
    
    # start off with no error message
    error_msg = ''
    
    for i in range(num_tries):
        
        output_format_prompt = f'''\nUse the following json format: \n\n {output_format} '''
        
        if list_output:
            output_format_prompt += '''\nIf user ask for a list, display it as ["{item_1-property_1}&\&\{item_1-property_2}","{item_2-property_1}&\&\{item_2-property_2}"]'''
        
        # if output_format contains dynamic elements, process it accordingly
        if dynamic_elements: 
            output_format_prompt += f'''
                                    Any text enclosed by < and > indicates you must generate content to replace it. Example input: Go to <location>, Example output: Go to the garden
                                    Any output key containing < and > indicates you must generate the key name to replace it. Example input: {{'<location>': 'description of location'}}, Example output: {{school: a place for education}}'''

        # if input is in a list format, ask it to generate json in a list
        if list_input:
            output_format_prompt += '''\nIf user ask for a list, display it as ["{item_1-property_1}&\&\{item_1-property_2}","{item_2-property_1}&\&\{item_2-property_2}"]'''
            
        # Use OpenAI to get a response
        response = client.chat.completions.create(
          temperature = temperature,
          max_tokens=5200,
          model=model,
          messages=[
            {"role": "system", "content": system_prompt + output_format_prompt + error_msg},
            {"role": "user", "content": str(user_prompt)}
          ]
        )
        res = response.choices[0].message.content.replace('\'', '"')
        print('hey')
        
        # ensure that we don't replace away aprostophes in text 
        res = re.sub(r"(\w)\"(\w)", r"\1'\2", res)

        if verbose:
            print('System prompt:', system_prompt + output_format_prompt + error_msg)
            print('\nUser prompt:', str(user_prompt))
            print('\nGPT response:', res)
        
        # try-catch block to ensure output format is adhered to
        try:
            output = json.loads(res)
            if isinstance(user_prompt, list):
                if not isinstance(output, list): raise Exception("Output format not in a list of json")
            else:
                output = [output]
                
            # check for each element in the output_list, the format is correctly adhered to
            for index in range(len(output)):
                for key in output_format.keys():
                    # unable to ensure accuracy of dynamic output header, so skip it
                    if '<' in key or '>' in key: continue
                    # if output field missing, raise an error
                    if key not in output[index]: raise Exception(f"{key} not in json output")
                    # si una de los campos pedidos por el usuario es un array
                    if isinstance(output_format[key], list):
                        choices = output_format[key]
                        # ensure output is not a list
                        if isinstance(output[index][key], list):
                            output[index][key] = output[index][key][0]
                        # output the default category (if any) if GPT is unable to identify the category
                        if output[index][key] not in choices and default_category:
                            output[index][key] = default_category
                        # if the output is a description format, get only the label
                        if ':' in output[index][key]:
                            output[index][key] = output[index][key].split(':')[0]
                            
                # if we just want the values for the outputs
                if output_value_only:
                    output[index] = [value for value in output[index].values()]
                    # just output without the list if there is only one element
                    if len(output[index]) == 1:
                        output[index] = output[index][0]
                    
            return output if list_input else output[0]

        except Exception as e:
            error_msg = f"\n\nResult: {res}\n\nError message: {str(e)}"
            print("An exception occurred:", str(e))
            print("Current invalid json format:", res)
         
    return {}

def gpt_request(pdfConvertedToText, jsonData):

    text = pdfConvertedToText
    
    res = strict_output(system_prompt = '''You are a assistant meant to extract data from a text pdf, separated by chunks of text. Every time a chunk is passed, copy the previous json and add the new data.''', 
              user_prompt = text,
              output_format = jsonData,
              default_category = "null")

    return (res)

def test():
    time.sleep(7)
    return 'lol'
