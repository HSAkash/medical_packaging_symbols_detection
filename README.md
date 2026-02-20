# Warning Symbol Detection on Medicine Packaging (WSDF)

🎥 **Demo Video (UI Walkthrough)**

> **Place your recorded UI demo video here (right after the title).**
> Example: GitHub supports video links or embedded preview via attachments.

---

## 1. Introduction

This repository implements the **Warning Symbol Detection Framework (WSDF)** for detecting standardized **pharmaceutical warning symbols** on medicine packaging.

The framework combines:

* **SAM3** for package/panel localization (mask extraction)
* **Synthetic dataset generation** by inserting symbols into valid panel regions
* **YOLOv12n** (lightweight detector) for final symbol detection
* **Gradio UI** for interactive inference

This project supports **7 warning symbol classes** and provides training + evaluation + inference + UI.

---

## 2. Supported Warning Symbols (7 Classes)

The system detects the following warning symbols:

1. **breastfeeding**
2. **dont_drink**
3. **drowsiness**
4. **external_use_only**
5. **pregnant**
6. **protect_from_light**
7. **temperature**

## Supported Warning Symbols

<div align="center">

<table>
<tr>
<td align="center">
<img src="assets/detection/breastfeeding.webp" width="150"/><br/>
<b>Breastfeeding</b>
</td>

<td align="center">
<img src="assets/detection/dont_drink.webp" width="150"/><br/>
<b>Do Not Drink</b>
</td>

<td align="center">
<img src="assets/detection/drowsiness.webp" width="150"/><br/>
<b>Drowsiness</b>
</td>
</tr>

<tr>
<td align="center">
<img src="assets/detection/external_use_only.webp" width="150"/><br/>
<b>External Use Only</b>
</td>

<td align="center">
<img src="assets/detection/pregnant.webp" width="150"/><br/>
<b>Pregnant</b>
</td>

<td align="center">
<img src="assets/detection/protect_from_light.webp" width="150"/><br/>
<b>Protect From Light</b>
</td>
</tr>

<tr>
<td align="center" colspan="3">
<img src="assets/detection/temperature.webp" width="150"/><br/>
<b>Temperature</b>
</td>
</tr>

</table>

</div>

---

## 3. Synthetic Logo Placement on Medicine Packages (SAM3 → Mask → Placement)

Since real annotated warning-symbol datasets are limited, this project generates a synthetic dataset by placing warning logos on real medicine package images.

### 3.1 Step-by-step Process

1. **Input:** Raw medicine package image
2. **SAM3 Segmentation:** Detect package/panel mask
3. **Mask Extraction:** Extract package region (panel position)
4. **Valid Placement Region Selection:** Choose flat/clean area inside panel
5. **Overlay Warning Logo:** Place symbol + auto-generate bounding box label

📌 **Add image here:** Full process example (4-step visual)

> `images/synthetic_pipeline_example.png`

📌 **Add images here (if you want separate steps):**

* Raw package image: `images/raw_package.jpg`
* SAM3 mask: `images/sam3_mask.png`
* Panel/ROI highlighted: `images/panel_roi.png`
* Final logo overlay result: `images/logo_overlay.png`

### 3.2 SAM3 Repo Used

This implementation uses **SAM3** for mask-based package localization:

* [https://github.com/facebookresearch/sam3](https://github.com/facebookresearch/sam3)

---

## 4. Installation

### 4.1 Clone the Repository

```bash
git clone git@github.com:HSAkash/medical_packaging_symbols_detection.git
cd medical_packaging_symbols_detection
```

### 4.2 Create Virtual Environment

```bash
python -m venv env
```

Activate:

**Windows**

```bash
env\Scripts\activate
```

**Linux / Mac**

```bash
source env/bin/activate
```

### 4.3 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. How to Run

### 5.1 Run Template

```bash
python template.py
```

### 5.2 Run Using Python

```bash
python main.py
```

### 5.3 Run Using DVC (Reproducible Pipeline)

Initialize DVC:

```bash
dvc init
```

Run pipeline:

```bash
dvc run
```

Reproduce pipeline:

```bash
dvc repro
```

### 5.4 Run the UI (Gradio)

```bash
python app.py
```

Then open the URL shown in the terminal.

📌 **Add image here:** UI screenshot (optional, since you will use video)

> `images/ui.png`

---

## 6. Training (YOLOv12n)

The synthetic dataset is used to train a **YOLOv12n** lightweight detector.

Training includes:

* multi-class detection (7 classes)
* rotation augmentation (0°, 90°, 180°, 270°)
* automatic bounding-box annotation from logo placement

📌 **Add image here:** Training pipeline / dataset generation figure (optional)

> `images/training_pipeline.png`

---

## 7. Training Results

This repository includes training curves and evaluation outputs.

📌 **Add image here:** Training/validation curves (`results.png`)

> `images/results.png`

### 7.1 Curves

📌 Add images here:

* F1–Confidence curve: `images/BoxF1_curve.png`
* Precision–Confidence curve: `images/BoxP_curve.png`
* Precision–Recall curve: `images/BoxPR_curve.png`
* Recall–Confidence curve: `images/BoxR_curve.png`

### 7.2 Confusion Matrix

📌 Add images here:

* Confusion Matrix (raw): `images/confusion_matrix.png`
* Confusion Matrix (normalized): `images/confusion_matrix_normalized.png`

### 7.3 Dataset Distribution

📌 Add image here:

* Dataset distribution (labels): `images/labels.jpeg`

---

## 8. Prediction / Detection Results (After Training)

Below are example detections for all 7 warning symbols after training.

📌 **Add images here:**

* `images/detect_breastfeeding.webp`
* `images/detect_dont_drink.webp`
* `images/detect_drowsiness.webp`
* `images/detect_external_use_only.webp`
* `images/detect_pregnant.webp`
* `images/detect_protect_from_light.webp`
* `images/detect_temperature.webp`

---

## 9. Output Format (Example)

The system returns both:

1. **Image output** with bounding box + label + confidence
2. **JSON output** with class name and bounding-box coordinates

Example format:

```json
{
  "class_name": "pregnant",
  "position": {
    "x1": 228.49,
    "y1": 379.87,
    "x2": 273.29,
    "y2": 425.29
  }
}
```

---

## 10. Reference Paper

All methodology details are based on the paper you provided:

**Detection of Warning Symbols on Medicine Packaging Using a Synthetic Dataset and Lightweight YOLO Model**

---

## 11. License

Add your license here (MIT / Apache 2.0 / etc.)

---

## 12. Author

**HSAkash**
Medical Packaging Warning Symbol Detection (WSDF)
