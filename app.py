from flask import Flask, request, jsonify
from storageFirebase import uploadFileFirebase
from azureRead import analyze_read
from gptToExcel import convertToExcel
from openAI import chatgpt_req

app = Flask(__name__)

@app.route('/process-file', methods=['POST'])
def process_file():
    print(request.files)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the received file to a temporary location or process it directly
    # For example, you might save it temporarily and get its path
    file_path = 'temp/' + file.filename
    file.save(file_path)

    fileUrl = uploadFileFirebase(file_path)

    print("Perform the processing" + fileUrl)
    #analizedPDF = analyze_read(fileUrl)
    #gpt_response = chatgpt_req(analizedPDF)
    #convertToExcel(gpt_response)

    return jsonify({'message': 'File processed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
