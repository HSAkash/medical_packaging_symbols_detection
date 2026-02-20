import cv2
import random
import numpy as np
from tqdm import tqdm
from pathlib import Path
from src.entity.config_entity import PopulateImageConfig


class PopulateImage:
    def __init__(self, config: PopulateImageConfig):
        self.config = config
        self.class_map = self.load_classes(self.config.classification_list_file_path)

    def load_classes(self, classes_file_path: Path):
        classes = []
        with open(classes_file_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        return {name: idx for idx, name in enumerate(classes)}

    def load_image(self, image_path: Path, is_logo: bool = False):
        if is_logo:
            # load image which has 4 chanel, logos background are transparent
            return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # (4, h, w)
        img = cv2.imread(image_path)  # (3, H, W)
        mask_path = (image_path.parent.parent / 'masks' / f"{image_path.stem}_mask").with_suffix('.npy')
        mask = np.load(mask_path).astype(np.uint8)
        return img, mask
    
    def resize_image_and_mask(self, img, mask, image_size_limit=640):
        """
        Resize image and mask so that max(height, width) >= image_size_limit
        while keeping aspect ratio unchanged.
        """

        h, w = img.shape[:2]
        max_side = max(h, w)

        # If already large enough, return as-is
        if max_side <= image_size_limit:
            return img, mask

        # Compute scale ratio
        scale = image_size_limit / max_side

        new_w = int(round(w * scale))
        new_h = int(round(h * scale))

        # Resize image (bilinear)
        img_resized = cv2.resize(
            img,
            (new_w, new_h),
            interpolation=cv2.INTER_LINEAR
        )

        # Resize mask (NEAREST to preserve labels)
        mask_resized = cv2.resize(
            mask,
            (new_w, new_h),
            interpolation=cv2.INTER_NEAREST
        )

        return img_resized, mask_resized
    
    def rotate_keep_size(self, img, angle):
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(
            img, M, (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0)
        )
    

        
    def add_logo_to_image(self, img, logo, mask, label, out_prefix:Path, rotation=False):
        mask_uint8 = mask.astype(np.uint8) * 255

        # -----------------------------
        # Prepare logo variants (optional 0/90/180/270)
        # -----------------------------
        logos = [logo]
        if rotation:
            logos = [
                logo,
                self.rotate_keep_size(logo, 90),
                self.rotate_keep_size(logo, 180),
                self.rotate_keep_size(logo, 270),
            ]

        # -----------------------------
        # Find package contour
        # -----------------------------
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)

        # -----------------------------
        # Package orientation & size
        # -----------------------------
        (_, _), (pkg_w, pkg_h), angle = cv2.minAreaRect(cnt)
        if pkg_w < pkg_h:
            angle += 90
            pkg_w, pkg_h = pkg_h, pkg_w

        # -----------------------------
        # Logo size rule
        # (10% of max side, but not bigger than min side)
        # -----------------------------
        max_side = max(pkg_w, pkg_h)
        min_side = min(pkg_w, pkg_h)

        logo_target_size = int(self.config.logo_size_ratio * max_side)
        logo_target_size = min(logo_target_size, int(min_side))

        # Distance transform once
        dist = cv2.distanceTransform(mask_uint8, cv2.DIST_L2, 5)

        # -----------------------------
        # Place each logo variant
        # -----------------------------
        for i, lg in enumerate(logos):
            out = img.copy()

            for temp_ratio in [1.0, 0.9, 0.8, 0.7,0.5]:
                # Resize logo (keep aspect ratio)
                logo_target_size = logo_target_size*temp_ratio
                lh, lw = lg.shape[:2]
                scale = logo_target_size / max(lw, lh)
                new_w = max(1, int(lw * scale))
                new_h = max(1, int(lh * scale))

                lg_resized = cv2.resize(lg, (new_w, new_h), interpolation=cv2.INTER_AREA)

                # Rotate resized logo to follow package angle (KEEP SIZE = new_h,new_w)
                lg_rot = self.rotate_keep_size(lg_resized, angle)

                # Recompute new_h,new_w (still same, but safe)
                new_h, new_w = lg_rot.shape[:2]

                # Safe placement radius
                half_diag = int(np.sqrt(new_w**2 + new_h**2) / 2)

                valid_positions = np.where(dist >= half_diag)
                if len(valid_positions[0]) == 0:
                    # return
                    # raise ValueError(f"Logo too large to fit inside mask (even with constraints). \npath:{out_prefix} \nlabel:{label}")
                    continue
                break

            if len(valid_positions[0]) == 0:
                    # return
                    raise ValueError(f"Logo too large to fit inside mask (even with constraints). \npath:{out_prefix} \nlabel:{label}")
            

            # Random safe center
            idx = random.randint(0, len(valid_positions[0]) - 1)
            cy = int(valid_positions[0][idx])
            cx = int(valid_positions[1][idx])

            x1 = cx - new_w // 2
            y1 = cy - new_h // 2

            # Clip to image boundaries
            H, W = out.shape[:2]
            x1 = max(0, min(x1, W - new_w))
            y1 = max(0, min(y1, H - new_h))

            # Mask check (must be fully inside object)
            roi_mask = mask_uint8[y1:y1 + new_h, x1:x1 + new_w]
            if roi_mask.shape[:2] != (new_h, new_w):
                continue  # edge case
            if not np.all(roi_mask == 255):
                # try a few times to find another random safe spot
                ok = False
                for _ in range(50):
                    idx = random.randint(0, len(valid_positions[0]) - 1)
                    cy = int(valid_positions[0][idx])
                    cx = int(valid_positions[1][idx])
                    x1 = max(0, min(cx - new_w // 2, W - new_w))
                    y1 = max(0, min(cy - new_h // 2, H - new_h))
                    roi_mask = mask_uint8[y1:y1 + new_h, x1:x1 + new_w]
                    if np.all(roi_mask == 255):
                        ok = True
                        break
                if not ok:
                    raise ValueError(f"Could not find a fully-inside placement after multiple tries.  \npath:{out_prefix} \nlabel:{label}")
                    return

            # Alpha handling
            if lg_rot.shape[2] == 4:
                alpha = lg_rot[:, :, 3].astype(np.float32) / 255.0
                logo_rgb = lg_rot[:, :, :3].astype(np.float32)
            else:
                alpha = np.ones((new_h, new_w), dtype=np.float32)
                logo_rgb = lg_rot.astype(np.float32)

            # Blend
            roi = out[y1:y1 + new_h, x1:x1 + new_w, :].astype(np.float32)
            for c in range(3):
                roi[:, :, c] = alpha * logo_rgb[:, :, c] + (1 - alpha) * roi[:, :, c]
            out[y1:y1 + new_h, x1:x1 + new_w, :] = roi.astype(np.uint8)

            image_save_path = (out_prefix.parent / f"{out_prefix.stem}_{label:02d}_{i*90:03d}").with_suffix('.jpg')
            cv2.imwrite(image_save_path, out)
            img_h, img_w, _ = out.shape
            bbox = [cx/img_w, cy/img_h, new_w/img_w, new_h/img_h]
            label_data = f"{label} {' '.join(map(str, bbox))}\n"
            label_path = (image_save_path.parent.with_stem('labels') / image_save_path.stem).with_suffix('.txt')
            label_path.write_text(label_data)


    def populate(self):
        logo_paths = self.config.source_logo_dir.glob("*")
        logo_paths = sorted(logo_paths)
        image_paths = self.config.source_dataset_dir.glob("*/images/*.jpg")
        image_paths = sorted(image_paths)

        logos = {}
        # load all the logo initially
        for logo_file in logo_paths:
            class_name = logo_file.stem
            logos[self.class_map[class_name]] = self.load_image(logo_file, is_logo=True)

        # iterate all images and add logos
        # index = 0
        n_classes = len(logos)
        for image_path in tqdm(image_paths, desc="Populating images: "):
            dest_dir = self.config.target_dir / image_path.parent.parent.stem
            dest_image_path = dest_dir / 'images' / image_path.name
            dest_label_path = (dest_dir / 'labels' / f"{image_path.stem}_{n_classes-1:02d}_{270}").with_suffix('.txt')

            dest_image_path.parent.mkdir(parents=True, exist_ok=True)
            dest_label_path.parent.mkdir(parents=True, exist_ok=True)

            if dest_label_path.exists():
                continue
            
            original_img, mask = self.load_image(image_path)
            original_img, mask = self.resize_image_and_mask(original_img, mask, self.config.image_size_limit)

            for logo_class in sorted(logos.keys()):
                logo_img = logos[logo_class]
                self.add_logo_to_image(
                    original_img,
                    logo_img,
                    mask,
                    logo_class,
                    dest_image_path,
                    rotation=True
                )
            # index += 1



if __name__ == "__main__":
    from src.config.configuration import ConfigurationManager
    from src import logger

    config = ConfigurationManager().get_populate_image_config()
    logger.info("Starting image population...")
    populate_image = PopulateImage(config)
    populate_image.populate()
    logger.info("Image population completed.")