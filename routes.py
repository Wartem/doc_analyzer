import os
import sys
import importlib
import json
from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from .config import project_name, display_name

print("Python path in routes.py:", sys.path)

# Dynamic imports
def import_module(module_name):
    with temporary_sys_path(project_dir):
        try:
            return importlib.import_module(f'.{module_name}', package='projects.doc_analyzer')
        except ImportError:
            try:
                return importlib.import_module(f'projects.doc_analyzer.{module_name}')
            except ImportError:
                return importlib.import_module(module_name)

import contextlib

@contextlib.contextmanager
def temporary_sys_path(path):
    original_sys_path = sys.path.copy()
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path = original_sys_path
        

project_dir = os.path.dirname(__file__)
project_name = os.path.basename(project_dir)

# Read display_name from project_config.json
config_path = os.path.join(project_dir, 'project_config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    display_name = config.get('display_name', project_name)

bp = Blueprint(project_name, __name__, template_folder='templates')
# bp = Blueprint(project_name, __name__, template_folder=f'{project_name}_templates')
 #bp = Blueprint(project_name, __name__, template_folder=os.path.join(project_dir, 'templates'))


@bp.route('/')
def index():
    # Check if we're running as an individual project
    if current_app.name == project_name:
        # If running individually, redirect to the project page
        return redirect(url_for(f'{project_name}.start_project'))
    # If running as part of main_app, show the index page
    return render_template('doc_index.html', project_name=project_name, display_name=display_name)

@bp.route('/project', methods=['GET', 'POST'])
def start_project():
    with temporary_sys_path(project_dir):
        project_main = import_module('project_main')
        files_handlers = import_module('utils.files_handlers')
        text_extraction = import_module('utils.text_extraction')
        api_client = import_module('utils.api_client')
        
    if request.method == 'POST':
        extracted_text = ""
        file_path = None

        # Handle file upload
        if 'file' in request.files:
            file_path, message = files_handlers.process_file_upload(request.files['file'])
            flash(message[0], message[1])

        # Handle URL
        file_url = request.form.get('file_url')
        if file_url:
            file_path, message = files_handlers.process_file_url(file_url)
            flash(message[0], message[1])

        # Extract text if we have a valid file_path
        if file_path:
            filename = os.path.basename(file_path)
            file_extension = filename.rsplit('.', 1)[1].lower()
            try:
                extracted_text = text_extraction.extract_text(file_path, file_extension)
            except ValueError as e:
                flash(str(e), 'danger')
                extracted_text = str(e)

        if not extracted_text:
            flash("No text was extracted from the document. Please ensure the document contains readable text.", 'warning')
            return render_template('doc_project.html', project_name=project_name, display_name=display_name)

        # Get criteria from the form
        user_prompt = request.form.get('prompt', '')
        
        # Construct the prompt
        full_prompt = f"{user_prompt}\n\nExtracted Text:\n{extracted_text}"
        
        # Analyze with LM Studio / OpenAI
        analysis_result = api_client.analyze_document_with_openai(full_prompt)
        
        # Render results
        return render_template('doc_project.html', analysis_result=analysis_result, project_name=project_name, display_name=display_name)
    
    # GET request
    result = project_main.start()
    result['project_name'] = project_name
    result['display_name'] = display_name
    return render_template('doc_project.html', **result)