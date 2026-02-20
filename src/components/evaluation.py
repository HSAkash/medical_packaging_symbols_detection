from src.entity.config_entity import EvaluationConfig
from ultralytics import YOLO
from src import logger


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.model = YOLO(self.config.model_path)
        self.model.fuse() # fuse model layers for better performance
        self.model.eval() # set model to evaluation mode

    def evaluate(self):
        try:
            results = self.model.val(
                data=self.config.yaml_path, # validation yaml file path
                imgsz=self.config.IMGSZ,
                device=self.config.DEVICE,
                batch=self.config.BATCH_SIZE,
                workers=self.config.WORKERS,
                project=self.config.project_path, # root dir, where evaluation results will be saved
                name=self.config.project_name, # inner project: root dir all fill will be saved in name folder
                exist_ok=True,
                verbose=True,
                save_json=True, # save JSON results
                save_conf=True,
            )

            evaluation_doc = "Evaluation results:\n"

            # Guard against missing or failed metrics.box
            if hasattr(results, "box") and results.box is not None:
                evaluation_doc += f"mAP@50: {getattr(results.box, 'map50', 'N/A'):.4f}\n" if results.box.map50 is not None else "mAP@50: N/A\n"
                evaluation_doc += f"mAP@50:95: {getattr(results.box, 'map', 'N/A'):.4f}\n" if results.box.map is not None else "mAP@50:95: N/A\n"
            else:
                evaluation_doc += "Warning: No bounding box evaluation results available.\n"

            # Speed
            if hasattr(results, "speed"):
                for key, value in results.speed.items():
                    evaluation_doc += f"    {key}: {value}\n"

            # Other metrics
            if hasattr(results, "results_dict"):
                for key, value in results.results_dict.items():
                    evaluation_doc += f"    {key}: {value}\n"

            logger.info(evaluation_doc)
            logger.info("Evaluation completed")

        except Exception as e:
            logger.error(f"Evaluation failed with error: {str(e)}")

if __name__ == "__main__":
    from src.config.configuration import ConfigurationManager
    config_manager = ConfigurationManager()
    evaluation_config = config_manager.get_evaluation_config()
    evaluation = Evaluation(evaluation_config)
    evaluation.evaluate()
    logger.info("Evaluation completed")