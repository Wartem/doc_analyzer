import pdfplumber
import docx
from bs4 import BeautifulSoup
import csv
import json

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def extract_text_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return '\n'.join([' '.join(row) for row in reader])

def extract_text_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return json.dumps(data, indent=4)

def extract_text(file_path, file_extension):
    extractors = {
        'txt': extract_text_from_txt,
        'docx': extract_text_from_docx,
        'pdf': extract_text_from_pdf,
        'html': extract_text_from_html,
        'csv': extract_text_from_csv,
        'json': extract_text_from_json
    }
    
    extractor = extractors.get(file_extension.lower())
    if not extractor:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    try:
        return extractor(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {str(e)}")
        return None