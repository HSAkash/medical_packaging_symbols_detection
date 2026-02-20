from pyprojroot import here # Geting root dir full path
from src.utils.commons import read_yaml
from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.entity.config_entity import (
    GenerateClassificationListConfig,
    PopulateImageConfig,
    SplittingDatasetConfig,
    GenerateTrainingYamlConfig,
    TrainingConfig,
    EvaluationConfig
)


class ConfigurationManager:
    def __init__(self, config_file_path: str=CONFIG_FILE_PATH, params_file_path: str=PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)

    def get_generate_classification_list_config(self) -> GenerateClassificationListConfig:
        config = self.config["generate_classification_list"]
        return GenerateClassificationListConfig(
            source_logo_dir=here(config.source_logo_dir),
            classification_list_file_path=here(config.classification_list_file_path)
        )

    def get_populate_image_config(self) -> PopulateImageConfig:
        config = self.config["populate_image"]
        populate_image_config = PopulateImageConfig(
            source_dataset_dir=here(config.source_dataset_dir),
            source_logo_dir=here(config.source_logo_dir),
            target_dir=here(config.target_dir),
            classification_list_file_path=here(config.classification_list_file_path),
            image_size_limit=config.image_size_limit,
            logo_size_ratio=config.logo_size_ratio
        )
        return populate_image_config
    
    def get_splitting_dataset_config(self) -> SplittingDatasetConfig:
        config = self.config["splitting_dataset"]
        splitting_dataset_config = SplittingDatasetConfig(
            source_image_dir=here(config.source_image_dir),
            source_label_dir=here(config.source_label_dir),
            yolo_dir=here(config.yolo_dir),
            train_image_dir=here(config.yolo_dir) / config.train_image_dir,
            train_label_dir=here(config.yolo_dir) / config.train_label_dir,
            val_image_dir=here(config.yolo_dir) / config.val_image_dir,
            val_label_dir=here(config.yolo_dir) / config.val_label_dir,
            train_ratio=config.train_ratio
        )
        splitting_dataset_config.train_image_dir.mkdir(parents=True, exist_ok=True)
        splitting_dataset_config.train_label_dir.mkdir(parents=True, exist_ok=True)
        splitting_dataset_config.val_image_dir.mkdir(parents=True, exist_ok=True)
        splitting_dataset_config.val_label_dir.mkdir(parents=True, exist_ok=True)
        return splitting_dataset_config

    def get_generate_training_yaml_config(self) -> GenerateTrainingYamlConfig:
        config = self.config["generate_training_yaml"]
        return GenerateTrainingYamlConfig(
            root_path=here(config.root_path),
            train=here(config.root_path) / config.train,
            test=here(config.root_path) / config.test,
            val=here(config.root_path) / config.val,
            class_file_path=here(config.class_file_path),
            train_yaml_path=here(config.root_path) / config.train_yaml_path
        )

    def get_training_config(self) -> TrainingConfig:
        config = self.config["training"]
        return TrainingConfig(
            yaml_path=here(config["yaml_path"]),
            project_path=here(config["project_path"]),
            project_name=config["project_name"],
            model=config["model"],
            model_save_path=here(config["model_save_path"]),
            resume=config["resume"],
            BATCH_SIZE=self.params["BATCH_SIZE"],
            WORKERS=self.params["WORKERS"],
            DEVICE=self.params["DEVICE"],
            IMGSZ=self.params["IMGSZ"],
            EPOCHS=self.params["EPOCHS"],
            LR=self.params["LR"],
            PATIENCE=self.params["PATIENCE"]
        )
    
    def get_evaluation_config(self) -> EvaluationConfig:
        config = self.config["evaluation"]
        return EvaluationConfig(
            model_path=here(config["model_path"]),
            yaml_path=here(config["yaml_path"]),
            project_path=here(config["project_path"]),
            project_name=config["project_name"],
            BATCH_SIZE=self.params["BATCH_SIZE"],
            WORKERS=self.params["WORKERS"],
            DEVICE=self.params["DEVICE"],
            IMGSZ=self.params["IMGSZ"]
        )