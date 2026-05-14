from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from detector import ObjectDetector
from database import init_db, save_detection, get_history

app = FastAPI(title="YOLO Object Detection API")

# Load the detector once when server starts
detector = ObjectDetector()
init_db()

@app.get("/")
def root():
    return {"message": "YOLO Object Detection API is running!"}

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    image_bytes = await file.read()
    annotated_image, labels = detector.detect(image_bytes)
    save_detection(file.filename, labels)
    # Return the annotated image directly
    return Response(content=annotated_image, media_type="image/jpeg")

@app.get("/history")
def detection_history():
    rows = get_history()
    return [
        {"id": r[0], "filename": r[1], "labels": r[2], "time": r[3]}
        for r in rows
    ]
