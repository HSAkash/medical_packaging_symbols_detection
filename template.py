import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "medical_packaging_symbols_detection"


# List of files to be created
list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/__init__.py",
    f"src/components/__init__.py",
    f"src/utils/__init__.py",
    f"src/config/__init__.py",
    f"src/config/configuration.py",
    f"src/pipeline/__init__.py",
    f"src/entity/__init__.py",
    f"src/constants/__init__.py",
    'main.py',
    
    # MLflow files
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    
    # setup files
    "requirements.txt",
    "setup.py",
    "README.md",

    # Jupyter Notebook files
    "notebook/",

    # Data files
    "dataset/images/",
    "dataset/logos/",
    "dataset/classes.txt",
]

# Function to create directories and files
def create_directories_and_files(project_name, list_of_files):
    for file_path in list_of_files:
        file_path = Path(file_path)
        # Create directories if they don't exist
        if file_path.suffix == "":
            if not os.path.exists(file_path):
                os.makedirs(file_path, exist_ok=True)
                logging.info(f"Created directory: {file_path}")
        else:
            # Create files if they don't exist
            if not os.path.exists(file_path):
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w') as f:
                    pass
                logging.info(f"Created file: {file_path}")


if __name__ == "__main__":
    # Create directories and files
    create_directories_and_files(project_name, list_of_files)
    logging.info(f"Project structure for '{project_name}' created successfully.")