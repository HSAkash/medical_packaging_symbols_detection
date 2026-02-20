from src.config.configuration import ConfigurationManager
from src.components.evaluation import Evaluation

class EvaluationPipeline:
    def __init__(self):
        pass

    def run(self):
        config_manager = ConfigurationManager()
        evaluation_config = config_manager.get_evaluation_config()
        evaluation = Evaluation(evaluation_config)
        evaluation.evaluate()

if __name__ == "__main__":
    from src import logger
    STAGE_NAME = "Evaluation"
    logger.info(f">>> stage {STAGE_NAME} started")
    pipeline = EvaluationPipeline()
    pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")