import shutil
from src import logger
from src.entity.config_entity import TrainingConfig
from ultralytics import YOLO


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.resume = config.resume
        self.weights_dir = self.config.project_path / self.config.project_name / "weights" # during training where model will be saved
        self.last_model_path = self.weights_dir / "last.pt" # during training, last version of model path
        self.best_model_path = self.weights_dir / "best.pt" # during training, best version of the model
        # Check if the last model exists and if we should resume training
        if self.last_model_path.exists() and self.resume:
            logger.info(f"Loading weights from {self.last_model_path}")
            self.model = YOLO(self.last_model_path)
            self.resume = True
        else:
            # load new model
            self.model = YOLO(self.config.model)
            self.resume = False

    def train(self):
        if self.resume:
            self.model.train(resume=self.resume)
        else:
            self.model.train(
                data=self.config.yaml_path, # training yaml file path
                epochs=self.config.EPOCHS,
                batch=self.config.BATCH_SIZE,
                imgsz=self.config.IMGSZ,
                device=self.config.DEVICE,
                workers=self.config.WORKERS,
                project=self.config.project_path, # root dir, where training results will be saved
                name=self.config.project_name, # inner project: root dir all fill will be saved in name folder
                exist_ok=True,
                pretrained=False,
                optimizer="Adam",
                lr0=self.config.LR,
                patience=self.config.PATIENCE,
                resume=self.resume
            )
        # Save the model
        if self.best_model_path.exists():
            self.config.model_save_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.best_model_path, self.config.model_save_path)
            logger.info(f"Model saved to {self.config.model_save_path}")


if __name__ == "__main__":
    from src.config.configuration import ConfigurationManager
    logger.info("Training started")
    config_manager = ConfigurationManager()
    training_config = config_manager.get_training_config()
    training = Training(training_config)
    training.train()
    logger.info("Training completed")