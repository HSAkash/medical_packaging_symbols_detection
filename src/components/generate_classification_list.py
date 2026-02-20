from src.entity.config_entity import GenerateClassificationListConfig

class GenerateClassificationList:
    """
    Generates a text file for logo classification.
    How many logo in logo folder based on that it create classes.txt file.
    """
    def __init__(self, config: GenerateClassificationListConfig):
        self.config = config

    def generate(self):
        # Get all logo files path
        logo_files = self.config.source_logo_dir.glob("*")
        logo_files = sorted(logo_files)
        # Get all logo file names without extensions and write to classification list file
        with open(self.config.classification_list_file_path, "w") as f:
            for logo_file in logo_files:
                class_name = logo_file.stem
                f.write(f"{class_name}\n")


if __name__ == "__main__":
    from src.config.configuration import ConfigurationManager
    from src import logger

    config_manager = ConfigurationManager()
    generate_classification_list_config = config_manager.get_generate_classification_list_config()
    generate_classification_list = GenerateClassificationList(generate_classification_list_config)
    generate_classification_list.generate()
    logger.info(f"Classification list generation completed. {generate_classification_list_config.classification_list_file_path} created.")
