import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import os
import uuid
from datetime import datetime, timedelta

script_directory = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(script_directory, 'serviceAccountKey.json')

cred = credentials.Certificate(json_file_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'data-magnet-98e0f.appspot.com',
    'databaseURL': 'https://data-magnet-98e0f-default-rtdb.firebaseio.com/'
})

bucket = storage.bucket()
destination_directory = 'Pdfs/'

def uploadFileFirebase (path_file):

    file_name, file_extension = os.path.splitext(os.path.basename(path_file))

    file_name = file_name.replace(" ","_")

    # Generate a unique ID (e.g., timestamp-based)
    unique_id = str(uuid.uuid4())

    # Create the new file name with the unique ID in the middle
    unique_file_name = f"{file_name}_{unique_id}{file_extension}"

    # Create the destination path in Firebase Storage
    destination_path = os.path.join(destination_directory, unique_file_name)

    # Upload the file to Firebase Storage
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(path_file)

    expiration_time = datetime.now() + timedelta(days=1)
            # URL of the uploaded file
    file_url = blob.generate_signed_url(expiration=expiration_time)

    return(file_url)

def save_object_to_firebase(obj):
    ref = db.reference('requests')  # Reference to the 'response' directory in the database
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")  # Get current timestamp
    ref.child(timestamp).set(obj)  # Set the object under a timestamp as a child

def save_errors_to_firebase(obj):
    ref = db.reference('errors')  # Reference to the 'response' directory in the database
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")  # Get current timestamp
    ref.child(timestamp).set(obj)  # Set the object under a timestamp as a child


"""
def upload_file_to_firebase_storage(file_path, destination_path):
    try:
        # Initialize Firebase Storage
        bucket = storage.bucket()

        # Upload the file to Firebase Storage
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(file_path)

        # URL of the uploaded file
        file_url = blob.public_url

        return file_url

    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return None

# Example usage:
file_path = 'path/to/your/local/file.txt'  # Replace with the path to your local file
destination_path = 'uploads/file.txt'  # Replace with the desired destination path in Firebase Storage

file_url = upload_file_to_firebase_storage(file_path, destination_path)
if file_url:
    print(f"File uploaded successfully. URL: {file_url}")"""
