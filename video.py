import cv2
from ultralytics import YOLO

def predictWater(frame):
    model = YOLO("YOLO_water_detection.pt")  # Update with your saved model path

    result = model.predict(frame,device="cpu")
    # print(result)

    probs = result[0].probs  # Get probability object
    predicted_class_index = probs.top1  # Index of the highest probability
    predicted_class_name = result[0].names[predicted_class_index]  # Class name
    confidence = probs.data[predicted_class_index].item()  # Confidence score
    # print(probs.top1conf>0.85)
    if(predicted_class_name=='Water' and probs.top1conf>0.90):
        return 1
    else:
        return 0

# cap=cv2.VideoCapture(0)
# while True:
#     ret,frame=cap.read()
#     if(not ret):
#         break
    
#     print(predictWater(frame))
    
#     cv2.imshow('frame',frame)
#     key=cv2.waitKey(1)
#     if key==27:
#         break
    
# cv2.destroyAllWindows()