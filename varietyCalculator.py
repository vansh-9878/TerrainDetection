import cv2
import numpy as np


def detect_roughness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = np.sqrt(np.square(sobel_x) + np.square(sobel_y))
    mean = np.mean(gradient_magnitude)
    std = np.std(gradient_magnitude)
    roughness_index = std / mean
    return roughness_level(roughness_index), roughness_index

def slipperiness_percentage(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    variance = np.var(gray)
    threshold_value = 5000  # Adjust this threshold based on testing

    if variance > threshold_value:
        percentage = 0  # Not slippery
    else:
        percentage = ((threshold_value - variance) / threshold_value) * 100

    return slipperiness_level(percentage)

def roughness_level(roughness_index):
    high_threshold = 1.5
    low_threshold = 0.3

    if roughness_index > high_threshold:
        return 5
    elif roughness_index < low_threshold:
        return 1  
    elif roughness_index>=0.3 and roughness_index<=0.6:
        return 2
    elif roughness_index>0.6 and roughness_index<0.9:
        return 3
    else:
        return 4

def slipperiness_level(slipperiness_percentage):
    high_threshold = 80
    low_threshold = 16

    if slipperiness_percentage > high_threshold:
        return 3  
    elif slipperiness_percentage < low_threshold:
        return 1  
    elif slipperiness_percentage>=16 and slipperiness_percentage<=32:
        return 2
    elif slipperiness_percentage>32 and slipperiness_percentage<=48:
        return 3
    else:
        return 4 

