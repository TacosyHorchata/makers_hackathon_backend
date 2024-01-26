from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

import json
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)

client = OpenAI()

def gpt_request_completions(flight_data):
    try:

        messages = [{"role": "system", "content": f"Summarize the following flight details and suggest the best options:\n\n{flight_data}"} ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        res = response.choices[0].message.content.replace('\'', "''")
        res = re.sub(r"(\w)\"(\w)", r"\1'\2", res)
        
        print(res)
        return {'response': res}

    except Exception as e:
        return {'error': str(e)}


@app.route('/', methods=['GET'])
def salute():
    return jsonify({'message': 'Hello world'})

@app.route('/scrape-data-processing', methods=['POST'])
def scrapeDataAndProcessing():
    try:

        data = request.get_json()
        departure_city = data['departure_city']
        destination_city = data['destination_city']
        departure_date = data['departure_date']
        return_date = data['return_date']


        url_search_results = f'https://www.kiwi.com/co/search/results/{departure_city}/{destination_city}/{departure_date}/{return_date}'


        response = requests.get(url_search_results)


        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            

            page_title = soup.title.text

            result = gpt_request_completions(page_title)
            return jsonify(result)
        
        else:
            return jsonify({'error': f"Error while making the request. Status code: {response.status_code}"})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':

    app.run(debug=True)


