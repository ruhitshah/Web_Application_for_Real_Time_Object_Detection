# detector.py
import cv2
import os
from ultralytics import YOLO

class YoloV8Detector:
    def __init__(self, weights_path: str = "models/yolov8n.pt", imgsz: int = 640, device: str | None = None):
        """
        weights_path: path to .pt weights (e.g., models/yolov8n.pt)
        imgsz: inference size (square)
        device: 'cpu', 'cuda', or None (auto). Ultralytics auto-selects if None.
        """
        self.weights_path = weights_path          # <<< store it so your apps can compare
        self.model = YOLO(weights_path)
        self.imgsz = imgsz

    def predict_result(self, frame, conf: float = 0.25, iou: float = 0.45):
        results = self.model.predict(
            source=frame, conf=conf, iou=iou, imgsz=self.imgsz, verbose=False
        )
        return results[0]

    def draw(self, frame, conf: float = 0.25, iou: float = 0.45, labels: bool = True):
        res = self.predict_result(frame, conf=conf, iou=iou)
        # Ultralytics Result.plot supports labels= (newer versions). Fall back if missing.
        try:
            annotated = res.plot(labels=labels)
        except TypeError:
            annotated = res.plot()
        return annotated

def open_video_source(source: str | int = 0):
    if isinstance(source, str) and source.isdigit():
        source = int(source)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")
    return cap

def mjpeg_generator(detector: YoloV8Detector, source=0, conf=0.25, iou=0.45, labels=True, save=False):
    """
    Yields an MJPEG stream with annotated frames.
    """
    cap = open_video_source(source)
    frame_id = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            annotated = detector.draw(frame, conf=conf, iou=iou, labels=labels)

            if save:
                os.makedirs("saved_frames", exist_ok=True)
                cv2.imwrite(f"saved_frames/frame_{frame_id:06d}.jpg", annotated)
                frame_id += 1

            ok, buffer = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not ok:
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )
    finally:
        cap.release()
