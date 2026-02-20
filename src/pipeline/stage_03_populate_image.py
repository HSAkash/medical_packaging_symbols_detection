from src.config.configuration import ConfigurationManager
from src.components.populate_image import PopulateImage

class PopulateImagesPipeline:
    def __init__(self):
        pass

    def run(self):
        config = ConfigurationManager().get_populate_image_config()
        populate_image = PopulateImage(config=config)
        populate_image.populate()



if __name__ == "__main__":
    from src import logger
    STAGE_NAME = "Populate Images"
    populate_images_pipeline = PopulateImagesPipeline()
    logger.info(f">>> stage {STAGE_NAME} started")
    populate_images_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")