import time

from ai_engine.models.model_loader import ModelLoader


loader = ModelLoader()

start = time.time()

loader.load_yolo_model(
    "yolov8n.pt"
)

end = time.time()

print(end - start)