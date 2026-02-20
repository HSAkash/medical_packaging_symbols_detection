from src.config.configuration import ConfigurationManager
from src.components.splitting_dataset import SplittingDataset


class SplittingDatasetPipeline:
    def __init__(self):
        pass

    def run(self):
        config = ConfigurationManager().get_splitting_dataset_config()
        splitting_dataset = SplittingDataset(config=config)
        splitting_dataset.split()


if __name__ == "__main__":
    from src import logger
    STAGE_NAME = "Splitting Dataset"
    splitting_dataset_pipeline = SplittingDatasetPipeline()
    logger.info(f">>> stage {STAGE_NAME} started")
    splitting_dataset_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")