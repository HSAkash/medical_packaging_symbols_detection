from dataclasses import dataclass
from pathlib import Path



@dataclass
class GenerateClassificationListConfig:
    source_logo_dir:                        Path
    classification_list_file_path:          Path


@dataclass
class PopulateImageConfig:
    source_dataset_dir:                       Path
    source_logo_dir:                        Path
    target_dir:                             Path
    classification_list_file_path:          Path
    image_size_limit:                       int
    logo_size_ratio:                        float


@dataclass
class SplittingDatasetConfig:
    source_image_dir:                       Path
    source_label_dir:                       Path
    yolo_dir:                               Path
    train_image_dir:                        Path
    train_label_dir:                        Path
    val_image_dir:                          Path
    val_label_dir:                          Path
    train_ratio:                            float


@dataclass(frozen=True)
class GenerateTrainingYamlConfig:
    root_path:                              Path
    train:                                  Path
    test:                                   Path
    val:                                    Path
    class_file_path:                        Path
    train_yaml_path:                        Path


@dataclass(frozen=True)
class TrainingConfig:
    yaml_path:                              Path
    project_path:                           Path
    project_name:                           Path
    model:                                  Path
    model_save_path:                        Path
    resume:                                 bool
    BATCH_SIZE:                             int
    WORKERS:                                int
    DEVICE:                                 str
    IMGSZ:                                  int
    EPOCHS:                                 int
    LR:                                     float
    PATIENCE:                               int


@dataclass(frozen=True)
class EvaluationConfig:
    model_path:                             Path
    yaml_path:                              Path
    project_path:                           Path
    project_name:                           Path
    BATCH_SIZE:                             int
    WORKERS:                                int
    DEVICE:                                 str
    IMGSZ:                                  int