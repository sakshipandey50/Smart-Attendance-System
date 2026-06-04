import cv2
import os
import time

if not os.path.exists("dataset"):
    os.makedirs("dataset")

name = input("Enter person name: ")
person_path = os.path.join("dataset", name)

if not os.path.exists(person_path):
    os.makedirs(person_path)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)
count = 0

print("Look at the camera and move slightly...")

while count < 50:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        count += 1
        cv2.imwrite(f"{person_path}/{count}.jpg", face)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        print(f"Captured image {count}")

        time.sleep(0.5)   # wait half second

    cv2.imshow("Face Capture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Face images captured successfully!")