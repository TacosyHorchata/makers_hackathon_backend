import time

import json
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)

#worker connection
q = Queue(connection=conn)

@app.route('/', methods=['GET'])
def salute():
    return jsonify({'message': 'Hello world'})

@app.route('/scrape-data-processing', methods=['POST'])
def scrapeDataAndProcessing():
    try:
        return jsonify({'job_id': 'Hey'})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
