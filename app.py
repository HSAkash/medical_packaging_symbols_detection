from PIL import Image
import json
import gradio as gr
from ultralytics import YOLO
from pyprojroot import here
from src import logger
from pathlib import Path


class APP:
    def __init__(self, model_path: Path):
        self.model = YOLO(model_path)
        self.model.fuse()
        self.model.eval()
        self.class_names = [
            'breastfeeding',
            'dont_drink',
            'drowsiness',
            'external_use_only',
            'pregnant',
            'protect_from_light',
            'temperature',
        ]

    def predict(self, img):
        results = self.model.predict(img)
        boxes = results[0].boxes.xyxy.tolist()  # Extract bounding box coordinates
        class_ids = [int(id) for id in results[0].boxes.cls.tolist()]
        ploted_img = results[0].plot()  # Plot the results on the image

        json_data = []
        for cls_id, xyxy in zip(class_ids, boxes):
            json_data.append(
                {
                    'class_name': self.class_names[cls_id],
                    'position':{
                        'x1': xyxy[0],
                        'y1': xyxy[1],
                        'x2': xyxy[2],
                        'y2': xyxy[2]
                    }
                }
            )


        return ploted_img, json.dumps(json_data, indent=4)  # Return the plotted image and bounding box coordinates as JSON

    def run(self):
        gr.Interface(
            fn=self.predict,
            inputs=gr.Image(type="pil", label="Upload Image"),
            outputs=[
                gr.Image(type="pil"),
                gr.Textbox()
            ]
        ).launch()

if __name__ == "__main__":
    logger.info("Starting the Gradio app...")
    app = APP(model_path=here("models/logo_detection.pt"))
    app.run()
