# Terrain Detection Project

## 🚀 Overview
This project utilizes deep learning models to classify terrain types in real-time from a webcam feed. A YOLOv8 model first determines if the terrain is water or not. If it is not water, a custom Convolutional Neural Network (CNN) classifies it into one of the following categories:
- 🌿 Grassy
- 🌊 Marshy
- 🪨 Rocky
- 🏖️ Sandy
- ❓ Other

Additionally, the system estimates roughness and slipperiness levels of the terrain.

## 🎯 Features
- 🔍 **Real-time terrain classification** using a YOLOv8 model and a CNN.
- 🎥 **Webcam feed processing** for continuous terrain detection.
- 🌐 **Flask-based web interface** for live visualization.
- 📊 **Roughness and slipperiness detection** for enhanced terrain analysis.

## 🛠 Installation
### Prerequisites
Ensure you have the following dependencies installed:
```bash
pip install flask opencv-python numpy joblib ultralytics
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/terrain-detection.git
cd terrain-detection
```

## ▶️ Running the Application
Start the Flask server:
```bash
python app.py
```

Access the web interface at:
```
http://localhost:8080/
```

## 🔗 API Endpoints
### 1️⃣ Live Video Feed
```
GET /video_feed
```
- Returns: Live webcam feed with terrain classification

### 2️⃣ Current Prediction
```
GET /current_prediction
```

## 🚧 Future Improvements
- 🔄 Extend classification to additional terrain types.
- 🎯 Improve model accuracy with more diverse datasets.
- 📱 Implement mobile compatibility for real-time detection.

## 📜 License
This project is licensed under the GNU License.

---
**👨‍💻 Author:** Vansh Arora
**🐙 GitHub:** [Github](https://github.com/vansh-9878)

