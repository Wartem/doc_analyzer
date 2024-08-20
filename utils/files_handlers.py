import os
import requests
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return file_path, ('File successfully uploaded', 'success')
    else:
        return None, ('Invalid file type', 'danger')

def process_file_url(file_url):
    try:
        response = requests.get(file_url)
        if allowed_file(file_url.split('.')[-1]):
            filename = secure_filename(file_url.split('/')[-1])
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path, ('File successfully downloaded from URL', 'success')
        else:
            return None, ('URL does not point to a supported document type', 'danger')
    except requests.exceptions.RequestException as e:
        return None, (f'Error downloading document: {e}', 'danger')