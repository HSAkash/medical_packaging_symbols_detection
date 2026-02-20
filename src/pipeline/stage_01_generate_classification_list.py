from src.config.configuration import ConfigurationManager
from src.components.generate_classification_list import GenerateClassificationList



STAGE_NAME = "Generate Classification List File"

class GenerateClassificationListPipeline:
    def __init__(self):
        pass

    def run(self):
        config = ConfigurationManager().get_generate_classification_list_config()
        yolo_label = GenerateClassificationList(config=config)
        yolo_label.generate()



if __name__ == "__main__":
    from src import logger
    generate_classification_list_pipeline = GenerateClassificationListPipeline()
    logger.info(f">>> stage {STAGE_NAME} started")
    generate_classification_list_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")