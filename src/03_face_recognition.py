import cv2
import numpy as np
from attendance_logic import mark_attendance

# Load trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read("models/face_model.yml")

# Load labels dictionary
labels = np.load("models/labels.npy", allow_pickle=True).item()

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

print("Starting Face Recognition... Press Q to exit.")
marked_people = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y : y + h, x : x + w]
        face = cv2.resize(face, (200, 200))

        label, confidence = model.predict(face)

        if confidence < 70:
         name = labels[label]
         text = f"{name} ({round(confidence, 2)})"
         color = (0, 255, 0)

         if name not in marked_people:
                mark_attendance(name)
                marked_people.add(name)

        else:
            text = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
