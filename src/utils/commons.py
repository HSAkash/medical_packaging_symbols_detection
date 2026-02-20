import yaml
from src import logger
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
from typing import Any

def read_yaml(file_path: Path) -> ConfigBox:
    try:
        with open(file_path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except FileNotFoundError as e:
        logger.error(f"File not found: {file_path}")
        raise e
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file: {file_path}")
        raise e
    except BoxValueError as e:
        logger.error(f"Error converting YAML to ConfigBox: {file_path}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise e
    
def save_yaml(file_path: Path, data: dict[str, Any], sort_keys=False):
    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file, sort_keys=sort_keys)
            logger.info(f"YAML file saved at: {file_path}")
    except Exception as e:
        logger.exception(f"Exception: {e}")
        raise Exception(f"Error saving YAML file: {file_path}") from e