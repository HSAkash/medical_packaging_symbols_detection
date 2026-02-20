from src import logger
from src.pipeline import (
    stage_01_generate_classification_list,
    stage_02_splitting_dataset,
    stage_03_populate_image,
    stage_04_generate_train_yaml,
    stage_05_training,
    stage_06_evaluation
)

if __name__ == "__main__":
    # Stage 1: Generate Classification List file
    STAGE_NAME = "Generate Classification List file"
    logger.info(f">>> stage {STAGE_NAME} started")
    generate_classification_list_pipeline = stage_01_generate_classification_list.GenerateClassificationListPipeline()
    generate_classification_list_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")

    # Stage 2: Splitting Dataset
    STAGE_NAME = "Splitting Dataset"
    logger.info(f">>> stage {STAGE_NAME} started")
    splitting_dataset_pipeline = stage_02_splitting_dataset.SplittingDatasetPipeline()
    splitting_dataset_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")

    # Stage 3: Generate Population Images
    STAGE_NAME = "Generate Population Images"
    logger.info(f">>> stage {STAGE_NAME} started")
    generate_population_images_pipeline = stage_03_populate_image.PopulateImagesPipeline()
    generate_population_images_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")

    # Stage 4: Generate Training YAML
    STAGE_NAME = "Generate Training YAML"
    logger.info(f">>> stage {STAGE_NAME} started")
    generate_training_yaml_pipeline = stage_04_generate_train_yaml.GenerateTrainYamlPipeline()
    generate_training_yaml_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")

    # Stage 5: Training
    STAGE_NAME = "Training"
    logger.info(f">>> stage {STAGE_NAME} started")
    training_pipeline = stage_05_training.TrainingPipeline()
    training_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")

    # Stage 6: Evaluation
    STAGE_NAME = "Evaluation"
    logger.info(f">>> stage {STAGE_NAME} started")
    evaluation_pipeline = stage_06_evaluation.EvaluationPipeline()
    evaluation_pipeline.run()
    logger.info(f">>> stage {STAGE_NAME} completed")