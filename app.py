import cv2
import numpy as np
import joblib
from flask import Flask, Response, render_template_string, jsonify
import varietyCalculator
import threading
import video

# Load model
model = joblib.load('modelV7.pkl')
# model = joblib.load('waterModel.pkl')
print("Model loaded successfully.")

# Define class names
class_names = {
    0: "Grassy",
    1: "Marshy",
    2: "Other",
    3: "Rocky",
    4: "Sandy",
}

# Initialize Flask app
app = Flask(__name__)

# Capture video feed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
else:
    print("Webcam opened successfully.")

current_prediction = "Loading..."
roughness="..."
slippery="..."
# Function to process video frames
def process_frame(frame):
    global current_prediction, roughness, slippery
    # Resize and normalize frame
    resized_frame = cv2.resize(frame, (255, 255))
    img_array = np.array(resized_frame, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Make predictions
    # start_time=time.time()
    waterPrediction=video.predictWater(frame)
    # end_time=time.time()
    # print(f'Time taken : {end_time-start_time}')
    if(waterPrediction==1):
        current_prediction='Water'
    else:
        print(img_array.shape)
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=-1)
        current_prediction = class_names.get(predicted_class[0], "Unknown")
        
    #roughness
    roughness=varietyCalculator.detect_roughness(frame)
    slippery=varietyCalculator.slipperiness_percentage(frame)
    # print(f" rough : {roughness[0]} ")

frame = []

from time import sleep

def predict_process_frames():
    global frame
    while True:
        if len(frame) == 0:
            print("Frame not available yet")
            sleep(2)
            continue
        process_frame(frame)
        print("frame processed!!!")
        
        

def generate_frames():
    global frame
    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error: Could not read frame.")
            break
        # print(ret)
        # frame = cv2.GaussianBlur(frame, (5, 5), 0)
        _, buffer = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_prediction')
def current_prediction_endpoint():
    return jsonify({"prediction": current_prediction,"roughness":roughness,"slippery":slippery})

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terrain Detection</title>
    <style>
        body {
            margin: 0;
            font-family: 'Arial', sans-serif;
            background-color: #121212;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            text-align: center;
            background: #1e1e1e;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        .header {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 20px;
            color: #76c7c0;
        }
        .video-container img {
            border-radius: 10px;
            border: 3px solid #76c7c0;
            width: 720px;
            height: auto;
        }
        .prediction-container {
            margin-top: 20px;
            display: flex;
            justify-content: space-around;
        }
        .prediction-box {
            background: #252525;
            padding: 15px 25px;
            border-radius: 10px;
            font-size: 1.5em;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            min-width: 150px;
        }
        .highlight {
            color: #76c7c0;
        }
    </style>
    <script>
        async function fetchPrediction() {
            try {
                const response = await fetch('/current_prediction');
                const data = await response.json();
                document.getElementById('prediction').innerText = data.prediction;
                document.getElementById('roughness').innerText = "Roughness Level " + data.roughness[0];
                document.getElementById('slipperyness').innerText = "Slippery Level " + data.slippery;
            } catch (error) {
                console.error('Error fetching prediction:', error);
            }
        }
        setInterval(fetchPrediction, 500);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">Terrain Detection Live Feed</div>
        <div class="video-container">
            <img src="{{ url_for('video_feed') }}" alt="Terrain Live Feed">
        </div>
        <div class="prediction-container">
            <div id="prediction" class="prediction-box highlight">Loading...</div>
            <div id="roughness" class="prediction-box">Loading...</div>
            <div id="slipperyness" class="prediction-box">Loading...</div>
        </div>
    </div>
</body>
</html>
    """)

if __name__ == '__main__':
    thread = threading.Thread(target=predict_process_frames)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
