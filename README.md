# Web Application for Real-Time Object Detection

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.70+-teal.svg)](https://fastapi.tiangolo.com/)  
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange.svg)](https://opencv.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  

This project provides a web-based interface for performing **real-time object detection** using deep learning models. It includes two implementations: one with **Flask** and another with **FastAPI**, allowing you to serve object detection results via a browser. Users can upload images or use their webcam to detect objects in real time.

---

## ✨ Features
- Real-time object detection using pre-trained deep learning models.
- Web interface with options for image upload or live camera feed.
- Two backend implementations: **Flask** and **FastAPI**.
- Organized structure with `static` (CSS/JS) and `templates` (HTML) directories.
- Easily extendable for new models or detection pipelines.

---

## 📂 Project Structure

```text
Web_Application_for_Real_Time_Object_Detection/
│
├── app_flask.py        # Flask implementation
├── app_fastapi.py      # FastAPI implementation
├── detector.py         # Core object detection logic
├── requirements.txt    # Required Python packages
├── README.md           # Project documentation
│
├── static/             # Static assets (CSS, JS, images)
├── templates/          # HTML templates
└── __pycache__/        # detector.cpython-313.pyc

```

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ruhitshah/Web_Application_for_Real_Time_Object_Detection.git
   cd Web_Application_for_Real_Time_Object_Detection
### Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
#Install dependencies
pip install -r requirements.txt
## 🚀 Usage
### Run with Flask
python app_flask.py
Open browser and navigate to: http://127.0.0.1:5000

### Run with FastAPI
uvicorn app_fastapi:app --reload
Open browser and navigate to: http://127.0.0.1:8000

## 🖼️ Web Interface
Upload an image for detection.

View detection results with bounding boxes and class labels.

Option to extend for live video stream (webcam integration).

## 📦 Requirements
Main dependencies (full list in requirements.txt):

Python 3.7+

Flask

FastAPI

Uvicorn

OpenCV

NumPy

TensorFlow / PyTorch (depending on model used)

## 🔧 Customization
Update detector.py to integrate your own trained detection model.

Modify templates/ to change the UI.

Add CSS/JS under static/ for design customization.

## 📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

## 👨‍💻 Author
Ruhit Shah
