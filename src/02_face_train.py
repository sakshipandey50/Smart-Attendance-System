import cv2
import os
import numpy as np

# Path to dataset
dataset_path = "dataset"

faces = []
labels = []
label_dict = {}
current_label = 0

# Loop through each person folder
for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_folder):
        continue

    label_dict[current_label] = person_name

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        img = cv2.resize(img, (200, 200))
        faces.append(img)
        labels.append(current_label)

    current_label += 1

# Convert to numpy array

labels = np.array(labels)

# Create LBPH face recognizer
model = cv2.face.LBPHFaceRecognizer_create()

# Train model
model.train(faces, labels)

# Create models folder if not exists
if not os.path.exists("models"):
    os.makedirs("models")

# Save trained model
model.save("models/face_model.yml")

# Save label dictionary
np.save("models/labels.npy", label_dict)

print("Model trained and saved successfully!")