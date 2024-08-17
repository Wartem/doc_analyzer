import os
import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

import openai
import pdfplumber
import docx
from bs4 import BeautifulSoup
import csv

# max 33 kB txt size

from openai.error import OpenAIError, APIConnectionError, RateLimitError

project_dir = os.path.dirname(__file__)
project_name = os.path.basename(project_dir)

# Read display_name from project_config.json
config_path = os.path.join(project_dir, 'project_config.json')
max_tokens = 12000
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    display_name = config.get('display_name', project_name)

bp = Blueprint(project_name, __name__, template_folder='templates')

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = os.path.join(project_dir, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'html', 'csv', 'json'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file using python-docx."""
    doc = docx.Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using pdfplumber."""
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_text_from_html(file_path):
    """Extract text from an HTML file using BeautifulSoup."""
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def extract_text_from_csv(file_path):
    """Extract text from a CSV file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return '\n'.join([' '.join(row) for row in reader])

def extract_text_from_json(file_path):
    """Extract text from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return json.dumps(data, indent=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path, file_extension):
    """Extract text based on file extension."""
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == 'txt':
        return extract_text_from_txt(file_path)
    elif file_extension == 'docx':
        return extract_text_from_docx(file_path)
    elif file_extension == 'html':
        return extract_text_from_html(file_path)
    elif file_extension == 'csv':
        return extract_text_from_csv(file_path)
    elif file_extension == 'json':
        return extract_text_from_json(file_path)
    else:
        raise ValueError("Unsupported file type")

def get_llm_server_info():
    # Example: Replace with actual logic to query your LLM server
    # This function should return a dictionary with server info
    return {
        "context_length": max_tokens  # Example value
    }

def analyze_document_with_openai(prompt):
    """Send a prompt to the LM Studio API and return the result."""
    try:
        base_url = "http://localhost:1234/v1"
        headers = {
            "Authorization": "Bearer lm-studio",  # Use if LM Studio requires an API key
            "Content-Type": "application/json"
        }
        payload = {
            "model": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        
        response = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"LM Studio API error: {str(e)}"

@bp.route('/')
def index():
    return render_template('index.html', project_name=project_name, display_name=display_name)

@bp.route('/project', methods=['GET', 'POST'])
def start_project():
    if request.method == 'POST':
        extracted_text = ""
        file_path = None

        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                flash('File successfully uploaded', 'success')
            else:
                flash('Invalid file type', 'danger')
                extracted_text = "Invalid file type"
        
        # Handle URL
        file_url = request.form.get('file_url')
        if file_url:
            try:
                response = requests.get(file_url)
                if allowed_file(file_url.split('.')[-1]):
                    filename = secure_filename(file_url.split('/')[-1])
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    flash('File successfully downloaded from URL', 'success')
                else:
                    flash('URL does not point to a supported document type', 'danger')
                    file_path = None
            except requests.exceptions.RequestException as e:
                flash(f'Error downloading document: {e}', 'danger')
                file_path = None
        
        # Extract text if we have a valid file_path
        if file_path:
            file_extension = filename.rsplit('.', 1)[1].lower()
            try:
                extracted_text = extract_text(file_path, file_extension)
            except ValueError as e:
                flash(str(e), 'danger')
                extracted_text = str(e)
        elif not extracted_text:  # If we haven't set it to an error message already
            extracted_text = "No file or URL provided"

        # Check if extracted_text is empty
        if not extracted_text.strip():
            flash("No text was extracted from the document. Please ensure the document contains readable text.", 'warning')
            return render_template('project.html', project_name=project_name, display_name=display_name)

        # Get criteria from the form
        user_prompt = request.form.get('prompt', '')
        
        # Construct the prompt
        full_prompt = f"{user_prompt}\n\nExtracted Text:\n{extracted_text}"
        
        # Analyze with LM Studio / OpenAI
        analysis_result = analyze_document_with_openai(full_prompt)
        
        # Render results
        return render_template('project.html', analysis_result=analysis_result, project_name=project_name, display_name=display_name)
    
    return render_template('project.html', project_name=project_name, display_name=display_name)