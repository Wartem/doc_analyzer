import json
import os
import importlib
import sys

# Read the project name from the config file
config_path = os.path.join(os.path.dirname(__file__), 'project_config.json')

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Read the project name from the config file
config_path = os.path.join(current_dir, 'project_config.json')

try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        project_name = config.get('project_name')    

    if not project_name:
        raise ValueError("Project name not found in config file")
    
    '''
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Attempting to import module: {project_name}")
    module = importlib.import_module(project_name)
    print(f"Module imported successfully: {module}")
    print(f"Attempting to get create_app function")
    create_app = getattr(module, 'create_app')
    print(f"create_app function retrieved: {create_app}")
    '''
    
    # Dynamic import using importlib
    module = importlib.import_module(project_name)
    create_app = getattr(module, 'create_app')

    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)

except FileNotFoundError:
    print(f"Error: Config file not found at {config_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in config file at {config_path}")
    sys.exit(1)
except ValueError as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
except ImportError:
    print(f"Error: Could not import module '{project_name}'. Make sure it exists and is in the correct location.")
    sys.exit(1)
except AttributeError:
    print(f"Error: Module '{project_name}' does not have a 'create_app' function.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
    sys.exit(1)