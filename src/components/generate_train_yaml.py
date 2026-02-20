from src.entity.config_entity import GenerateTrainingYamlConfig
from src.utils.commons import save_yaml

class GenerateTrainingYaml:
    def __init__(self, config: GenerateTrainingYamlConfig):
        self.config = config

    def get_class_info(self):
        # Get class names from the class file classes.txt
        with open(self.config.class_file_path, 'r') as file:
            class_info = file.readlines()
        return sorted([x.strip() for x in class_info if x.strip()])

    def generate_yaml(self):
        self.class_names = self.get_class_info()
        number_of_classes = len(self.class_names)
        data = {
            'path': self.config.root_path.__str__(), # root path where yolo data will be
            'train': self.config.train.__str__(), # train images & label path
            'test': self.config.test.__str__(), # train images & label path
            'val': self.config.val.__str__(), # validation images & label path
            'nc': number_of_classes, # number of classes
            'names': self.class_names # class names
        }
        # Save the YAML file
        save_yaml(self.config.train_yaml_path, data, sort_keys=False)


if __name__ == "__main__":
    from src import logger
    from src.config.configuration import ConfigurationManager
    config_manager = ConfigurationManager()
    generate_training_yaml_config = config_manager.get_generate_training_yaml_config()
    generate_training_yaml = GenerateTrainingYaml(generate_training_yaml_config)
    generate_training_yaml.generate_yaml()
    logger.info("YAML file generation completed.")