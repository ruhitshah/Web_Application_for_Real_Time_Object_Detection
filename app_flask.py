from flask import Flask, render_template, Response, request, send_from_directory
from detector import YoloV8Detector, mjpeg_generator

app = Flask(__name__, static_folder="static", template_folder="templates")
DETECTOR = YoloV8Detector(weights_path="models/yolov8n.pt", imgsz=640)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    conf = float(request.args.get("conf", 0.25))
    iou  = float(request.args.get("iou", 0.45))
    source = request.args.get("source", "0")
    labels = request.args.get("labels", "true") == "true"
    save   = request.args.get("save", "false") == "true"
    model  = request.args.get("model", "yolov8n.pt")

    global DETECTOR
    if model != DETECTOR.weights_path:
        DETECTOR = YoloV8Detector(weights_path=f"models/{model}", imgsz=640)

    gen = mjpeg_generator(DETECTOR, source=source, conf=conf, iou=iou, labels=labels, save=save)
    return Response(gen, mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
