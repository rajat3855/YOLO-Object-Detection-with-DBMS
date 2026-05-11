import cv2
import numpy as np
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        # This will auto-download yolov8n.pt the first time (~6MB)
        self.model = YOLO("yolov8n.pt")

    def detect(self, image_bytes: bytes):
        # Convert uploaded image bytes into something OpenCV can read
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Run YOLO detection
        results = self.model(img)[0]
        labels = []

        # Draw boxes on the image for each detected object
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = self.model.names[int(box.cls[0])]
            conf = round(float(box.conf[0]), 2)
            labels.append({"label": label, "confidence": conf})

            # Draw rectangle and label text
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{label} {conf}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert back to image bytes to send as response
        _, encoded = cv2.imencode(".jpg", img)
        return encoded.tobytes(), labels
