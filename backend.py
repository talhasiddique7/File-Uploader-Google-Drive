from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
import threading
import uuid
import logging

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

SCOPES = ['https://www.googleapis.com/auth/drive.file']
upload_progress = {}
progress_lock = threading.Lock()

def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(filepath, filename, upload_id):
    try:
        service = get_drive_service()
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath, resumable=True)
        request_drive = service.files().create(body=file_metadata, media_body=media)

        while True:
            status, response = request_drive.next_chunk()
            if status:
                with progress_lock:
                    upload_progress[upload_id] = int(status.progress() * 100)
            if response:
                break

        os.remove(filepath)
        with progress_lock:
            upload_progress[upload_id] = 100

    except Exception as e:
        logging.error(f"Upload failed: {e}")
        with progress_lock:
            upload_progress[upload_id] = f"error: {str(e)}"
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    if not os.path.exists("temp"):
        os.makedirs("temp")
    filepath = os.path.join("temp", filename)
    file.save(filepath)

    upload_id = str(uuid.uuid4())
    with progress_lock:
        upload_progress[upload_id] = 0

    thread = threading.Thread(target=upload_to_drive, args=(filepath, filename, upload_id))
    thread.start()

    return jsonify({"upload_id": upload_id})

@app.route('/progress/<upload_id>', methods=['GET'])
def check_progress(upload_id):
    with progress_lock:
        progress = upload_progress.get(upload_id, 0)
    return jsonify({"progress": progress})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
