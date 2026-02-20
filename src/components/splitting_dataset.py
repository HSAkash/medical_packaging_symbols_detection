import shutil
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from src.entity.config_entity import SplittingDatasetConfig


class SplittingDataset:
    def __init__(self, config: SplittingDatasetConfig):
        self.config = config

    def split(self):
        image_paths = self.config.source_image_dir.glob("*")
        image_paths = list(image_paths)

        # Spliting the training test paths
        train_paths, val_paths = train_test_split(
            image_paths,
            train_size=self.config.train_ratio,
            random_state=42,
            shuffle=True
        )

        for img_path in tqdm(train_paths, desc="Copying training images"):
            # Copy training images and corresponding labels
            shutil.copy(img_path, self.config.train_image_dir / img_path.name)
            # image path with .txt extension and change the logo dir
            label_path = self.config.source_label_dir / img_path.with_suffix('.txt').name
            shutil.copy(label_path, self.config.train_label_dir / label_path.name)

        # Copy validation images and labels
        for img_path in tqdm(val_paths, desc="Copying validation images"):
            shutil.copy(img_path, self.config.val_image_dir / img_path.name)
            label_path = self.config.source_label_dir / img_path.with_suffix('.txt').name
            shutil.copy(label_path, self.config.val_label_dir / label_path.name)


if __name__ == "__main__":
    from src.config.configuration import ConfigurationManager
    from src import logger

    STAGE_NAME = "Splitting Dataset"
    logger.info(f">>> stage {STAGE_NAME} started")
    config = ConfigurationManager().get_splitting_dataset_config()
    splitter = SplittingDataset(config=config)
    splitter.split()
    logger.info(f">>> stage {STAGE_NAME} completed")