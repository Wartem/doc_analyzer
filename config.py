import os
import json

# Get the directory of the current script (config.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the config file (in the same directory as this script)
config_path = os.path.join(current_dir, 'project_config.json')

# Default configuration
default_config = {
    "UPLOAD_FOLDER": "uploads",
    "ALLOWED_EXTENSIONS": ["txt", "pdf", "png", "jpg", "jpeg", "gif"],
    "project_name": "doc_analyzer",
    "display_name": "Document Analyzer",
    "max_tokens": 12000,
}

# Try to load the configuration file, use defaults if not found
try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print(f"Warning: Configuration file not found at {config_path}. Using default configuration.")
    config = default_config

# Set configuration variables
UPLOAD_FOLDER = os.path.join(current_dir, config.get("UPLOAD_FOLDER", default_config["UPLOAD_FOLDER"]))
ALLOWED_EXTENSIONS = config.get("ALLOWED_EXTENSIONS", default_config["ALLOWED_EXTENSIONS"])
project_name = config.get("project_name", default_config["project_name"])
display_name = config.get("display_name", default_config["display_name"])
max_tokens = config.get("max_tokens", default_config["max_tokens"])

# Ensure the UPLOAD_FOLDER exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)