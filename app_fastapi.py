from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from detector import YoloV8Detector, mjpeg_generator

app = FastAPI(title="YOLOv8 Realtime (FastAPI)")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DETECTOR = YoloV8Detector(weights_path="models/yolov8n.pt", imgsz=640)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/video_feed")
def video_feed(
    conf: float = 0.25,
    iou: float = 0.45,
    source: str = "0",
    labels: bool = True,
    save: bool = False,
    model: str = "yolov8n.pt"
):
    global DETECTOR
    # Only reload when model actually changes
    if model != DETECTOR.weights_path:
        DETECTOR = YoloV8Detector(weights_path=f"models/{model}", imgsz=640)

    gen = mjpeg_generator(DETECTOR, source=source, conf=conf, iou=iou, labels=labels, save=save)
    return StreamingResponse(gen, media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/health")
def health():
    return {"status": "ok"}
