import cv2
import numpy as np
import pyttsx3
import os

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speech speed

# Load currency images (pre-captured dataset)
CURRENCY_PATH = "images"
currency_images = {}
currency_labels = {}

for file in os.listdir(CURRENCY_PATH):
    if file.endswith(".jpg") or file.endswith(".png"):
        label = file.split(".")[0]  # Extract currency name from filename
        image = cv2.imread(os.path.join(CURRENCY_PATH, file), 0) 
        currency_images[label] = image
        currency_labels[label] = label

# ORB Feature Detector
orb = cv2.ORB_create(nfeatures=500) 
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

def detect_currency(frame):
    """Detects currency by matching features with stored images."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    best_match = None
    max_good_matches = 0

    # Compute keypoints and descriptors for input frame
    kp1, des1 = orb.detectAndCompute(gray_frame, None)
    
    if des1 is None:
        return None  # No features detected in the frame

    for label, image in currency_images.items():
        # Compute keypoints and descriptors for stored currency image
        kp2, des2 = orb.detectAndCompute(image, None)
        
        if des2 is None:
            continue

        matches = bf.match(des1, des2)

        # Sort matches by distance (lower is better)
        matches = sorted(matches, key=lambda x: x.distance)

        # Count good matches (lower distance means better match)
        good_matches = [m for m in matches if m.distance < 50]  # 50 is a good threshold
        
        # If this currency has more good matches than previous best, update
        if len(good_matches) > max_good_matches:
            max_good_matches = len(good_matches)
            best_match = label

    # Only consider as detected if good matches exceed a threshold
    return best_match if max_good_matches > 20 else None  # Increased threshold for better accuracy

def speak_currency(currency_name):
    """Speaks the detected currency."""
    engine.say(f"The detected Indian currency is {currency_name}")
    engine.runAndWait()

previous_detection = None  # To avoid repeated speech

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    detected_currency = detect_currency(frame)

    if detected_currency and detected_currency != previous_detection:
        print(f"Detected: {detected_currency}")
        cv2.putText(frame, f"Currency: {detected_currency}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        speak_currency(detected_currency)
        previous_detection = detected_currency  # Avoid repeating the same speech

    elif not detected_currency:
        previous_detection = None  # Reset if no currency detected

    cv2.imshow("Currency Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()