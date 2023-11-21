from flask import Flask, request, jsonify
from storageFirebase import uploadFileFirebase, save_object_to_firebase, save_errors_to_firebase
from azureRead import analyze_read
from gptToExcel import convertToExcel
from openAI import chatgpt_req
from dataMagnet import gpt_request

from PyPDF2 import PdfReader
import os

#imports for worker
from rq import Queue
from worker import conn
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

@app.route('/process-file', methods=['POST'])
def process_file():
    try:
        #cargando el json que incluye el schema
        posted_data = json.loads(request.form.get('output_json'))

        #revisando que exista el archivo en la peticion
        if 'file' not in request.files:
            save_errors_to_firebase({'error': 'No file'})
            return jsonify({'error': 'No file'})
        
        file = request.files['file']
        
        if file.filename == '':
            save_errors_to_firebase({'error': 'File missing'})
            return jsonify({'error': 'File missing'})

        #revisar si es pdf
        file_extension = os.path.splitext(file.filename)[1]
        if file_extension.lower() != '.pdf':
            save_errors_to_firebase({'error': 'File extension is not a pdf', 'file-name': file.filename, "requested-data": posted_data})
            return jsonify({'error': 'File extension is not pdf'})

        #guardando el archivo temporal
        file_path = 'temp/' + file.filename
        file.save(file_path)

        print({"File name":file.filename, "Output JSON": posted_data})
        #revisando que el archivo no tenga mas de 5 paginas
        with open(file_path, 'rb') as f:
            pdf = PdfReader(f)
            num_pages = len(pdf.pages)

        if num_pages > 5:
            save_errors_to_firebase({'error': 'File has too many pages', 'file-name': file.filename, "requested-data": posted_data})
            return jsonify({'error': 'File has too many pages'})
        
        #si todo salio bien, se sube a firebase
        fileUrl = uploadFileFirebase(file_path)
        print({"File URL":fileUrl})
        #se analiza el texto en el pdf
        analyzedPDF = analyze_read(fileUrl)
        print({"length from Analized PDF":len(analyzedPDF)})

        #revisando que el archivo no tenga mas de 10000 caracteres o lo que serian 2000 palabras
        if len(analyzedPDF) > 10000:  
            save_errors_to_firebase({'error': 'File has too much words', 'file-name': file.filename, "file-url": fileUrl, "requested-data": posted_data})
            return jsonify({'error': 'File has too much words'})
        
        #se guarda lo analizado en 'temp/analyzed_text.txt'
        txt_file_path = 'temp/analyzed_text.txt'
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(analyzedPDF)

        #se le pasa el texto a la funcion del LLM
        job = q.enqueue(gpt_request, analyzedPDF, posted_data)

        while True:
            status = job.get_status()
            if status == 'SUCCESSFUL':
                # Job is successfully completed
                dataExtracted = job.return_value
                print({"Data Extracted": dataExtracted})
                break  
            elif status == 'FAILED' or status == 'STOPPED':
                # Job encountered an error or stopped
                print("Job failed or stopped.")
                break  
            else:
                print('looping', status)
                # Job is still in progress, wait for some time before checking again
                time.sleep(2)

        # Wait for the job to finish and get the result
        dataExtracted = dataExtracted = job.return_value
        print({"Data Extracted":dataExtracted})

        #guardar la peticion y sus datos en Firebase
        reqAndResponseData = {
            "filename": file.filename,
            "file-url": fileUrl,
            "requested-data": posted_data,
            "lenght-of-document": len(analyzedPDF),
            "extracted-data": json.dumps(dataExtracted),
        }

        save_object_to_firebase(reqAndResponseData)
        #convertToExcel(gpt_response)

        return (dataExtracted)

    except Exception as e:
        error_data = {
            'error': str(e),
            'file-name': file.filename if 'file' in locals() else 'Unknown',
            'file-url': fileUrl if 'fileUrl' in locals() else 'Unknown',
            'requested-data': posted_data if 'posted_data' in locals() else 'Unknown'
        }
        save_errors_to_firebase(error_data)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
