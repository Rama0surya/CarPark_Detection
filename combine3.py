import cv2
import pickle
import numpy as np
import requests
from flask import Flask, render_template, Response
import threading
import time
from ultralytics import YOLO

# Load YOLOv8 Model
model = YOLO("best8n.pt")  # Pastikan model sudah dilatih
CONFIDENCE_THRESHOLD = 0.3

# Load parking positions dari file
try:
    with open('park_positions', 'rb') as f:
        park_positions = pickle.load(f)
except FileNotFoundError:
    print("Error: Parking positions file not found.")
    park_positions = []

print("Loaded Parking Positions:", park_positions)

# Font untuk teks di video
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Inisialisasi video capture
cap = cv2.VideoCapture(2)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from camera.")
    exit()
frame_height, frame_width, _ = frame.shape
print(f"Frame size: {frame_width}x{frame_height}")

cv2.imwrite("Demo2.jpg", cv2.resize(frame, (frame_width, frame_height)))
print("Screenshot saved as testingimage.jpg")

status_array = [0] * len(park_positions)

def is_car_in_zone(detection, zone):
    x1, y1, x2, y2 = detection
    zx, zy, zw, zh = zone
    zx2, zy2 = zx + zw, zy + zh
    return not (x2 < zx or x1 > zx2 or y2 < zy or y1 > zy2)

def process_parking_spaces(frame, detections, overlay):
    for idx, position in enumerate(park_positions):
        if len(position) == 5:
            spot_id, x, y, width, height = position
            x = int(x * frame_width / 1280)
            y = int(y * frame_height / 720)
            width = int(width * frame_width / 1280)
            height = int(height * frame_height / 720)
            
            if width <= 0 or height <= 0:
                continue
            
            zone = (x, y, width, height)
            car_detected = any(is_car_in_zone(d["box"], zone) for d in detections if d["class"] == 0)
            color = (0, 0, 255) if car_detected else (0, 255, 0)
            status_array[idx] = 1 if car_detected else 0
            cv2.rectangle(overlay, (x, y), (x + width, y + height), color, 2)
            cv2.putText(overlay, 'occupied' if car_detected else 'empty', (x + 4, y + 20), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

def update_status_array():
    url = "https://api.arifhida.my.id/update-status-cam"
    API_TOKEN = "AAAA@@!!!"  # Ganti dengan token kamu

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    while True:
        try:
            response = requests.post(url, json={"statusArray": status_array}, headers=headers)
            if response.status_code == 200:
                print("Status array successfully sent:", status_array)
            else:
                print("Failed to send status array:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending request:", e)
        time.sleep(2)


app = Flask('__name__')

def video_stream():
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        overlay = frame.copy()
        
        results = model(frame)
        detections = [
            {"box": (int(box[0]), int(box[1]), int(box[2]), int(box[3])),
             "class": int(cls), "confidence": float(conf)}
            for box, cls, conf in zip(results[0].boxes.xyxy, results[0].boxes.cls, results[0].boxes.conf)
            if conf > CONFIDENCE_THRESHOLD
        ]
        
        process_parking_spaces(frame, detections, overlay)
        ret, buffer = cv2.imencode('.jpeg', overlay)
        if not ret:
            continue
        yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    update_thread = threading.Thread(target=update_status_array)
    update_thread.daemon = True  
    update_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
