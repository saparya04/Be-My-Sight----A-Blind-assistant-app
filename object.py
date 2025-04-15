import cv2
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Load pre-trained model and config files
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

# Class labels for the MobileNet SSD model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

last_spoken = ""
while True:
    ret, frame = cap.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    spoken_labels = set()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]
            box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the box and label
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            label_text = f"{label}: {confidence:.2f}"
            cv2.putText(frame, label_text, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Speak the object name if not already spoken recently
            if label != last_spoken:
                spoken_labels.add(label)

    # Speak all detected labels once per frame (non-repeating)
    for label in spoken_labels:
        engine.say(f"{label} detected")
        engine.runAndWait()
        last_spoken = label

    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
