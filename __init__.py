# doc_analyzer initialization
from flask import Flask
import os
import json

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Load configuration from project_config.json
    config_path = os.path.join(os.path.dirname(__file__), 'project_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            app.config.update(config)

    # Ensure project_name and display_name are set
    if 'project_name' not in app.config:
        app.config['project_name'] = os.path.basename(os.path.dirname(__file__))
    if 'display_name' not in app.config:
        app.config['display_name'] = app.config['project_name']

    # ... other configurations ...

    from . import routes
    bp = routes.bp
    bp.name = app.config['project_name']  # Dynamically set the blueprint name
    app.register_blueprint(bp)

    return app