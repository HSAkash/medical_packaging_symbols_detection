from src.config.configuration import ConfigurationManager
from src.components.training import Training

class TrainingPipeline:
    def __init__(self):
        pass

    def run(self):
        config_manager = ConfigurationManager()
        training_config = config_manager.get_training_config()
        training = Training(training_config)
        training.train()

if __name__ == "__main__":
    from src import logger
    STAGE_NAME = "Training"
    logger.info(f">>> stage {STAGE_NAME} started")
    pipeline = TrainingPipeline()
    pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")