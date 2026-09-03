import cv2
import numpy as np

# Load Saree model
saree = cv2.imread("inputs/persons/model_female_001.jpg")
sh, sw = saree.shape[:2]

# Load face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(saree, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (fx, fy, fw, fh) in faces:
    print(f"Detected Saree Girl Face at: x={fx}, y={fy}, w={fw}, h={fh}")

# Load isolated green dress
green = cv2.imread("assets/dataset_14/tryons/emerald_green_suit.jpg")
gh, gw = green.shape[:2]
gray_g = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
faces_g = face_cascade.detectMultiScale(gray_g, 1.1, 4)
for (gx, gy, gw_box, gh_box) in faces_g:
    print(f"Detected Green Dress Face at: x={gx}, y={gy}, w={gw_box}, h={gh_box}")
