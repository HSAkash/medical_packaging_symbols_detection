from src.config.configuration import ConfigurationManager
from src.components.generate_train_yaml import GenerateTrainingYaml

class GenerateTrainYamlPipeline:
    def __init__(self):
        pass

    def run(self):
        config_manager = ConfigurationManager()
        generate_training_yaml_config = config_manager.get_generate_training_yaml_config()
        generate_training_yaml = GenerateTrainingYaml(generate_training_yaml_config)
        generate_training_yaml.generate_yaml()


if __name__ == "__main__":
    from src import logger
    STAGE_NAME = "Generate Training YAML"
    logger.info(f"Starting {STAGE_NAME}...")
    pipeline = GenerateTrainYamlPipeline()
    pipeline.run()
    logger.info(f"Completed {STAGE_NAME}.")