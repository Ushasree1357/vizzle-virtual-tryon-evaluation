import cv2
import numpy as np

# Load the tryon
img = cv2.imread("assets/dataset_14/tryons/white_embroidered_anarkali.jpg")
h, w = img.shape[:2]

# Load clean background reference
bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\perfect_background_tryon_1788360834982.jpg")

# Replace the lower right floor area (x: 420-560, y: 720-950) where old blue tassels appear with clean stone step
clean_step = bg[int(h*0.75):h, int(w*0.75):w]
c_h, c_w = clean_step.shape[:2]
img[int(h*0.75):int(h*0.75)+c_h, int(w*0.75):int(w*0.75)+c_w] = clean_step

# Replace the upper left doorway (x: 0-220, y: 0-350) with clean doorway
clean_door = bg[0:int(h*0.35), 0:int(w*0.25)]
img[0:int(h*0.35), 0:int(w*0.25)] = clean_door

# Replace the top center header with clean transom arch
clean_arch = bg[0:int(h*0.12), int(w*0.20):int(w*0.80)]
img[0:int(h*0.12), int(w*0.20):int(w*0.80)] = clean_arch

# Save cleaned image
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", img)
print("Finished pristine touch-up of White Sequence Dress Tryon!")
