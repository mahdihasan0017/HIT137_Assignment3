# models/image_model.py
from transformers import pipeline

class ImageModel:
    def __init__(self):
        self.model_name = "DETR Object Detector"
        self.category = "Image (Computer Vision - Object Detection)"
        self.description = "Detects objects and their bounding boxes in images."

        self.model = pipeline(
            "object-detection",  # changed task
            model="facebook/detr-resnet-50"  # changed model
        )

    def run(self, image_path: str):
        try:
            result = self.model(image_path)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
