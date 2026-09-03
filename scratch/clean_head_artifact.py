import cv2
import numpy as np

img_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_set_no_dupatta_tryon_1788438862262.jpg"
img = cv2.imread(img_path)
h, w = img.shape[:2]

# The small head artifact is located at top-left: y from 0 to 130, x from 315 to 455
mask = np.zeros((h, w), dtype=np.uint8)
mask[0:135, 320:455] = 255

# Inpaint using Telea
clean_img = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)

# Save result
out_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_clean.jpg"
cv2.imwrite(out_path, clean_img)
print("Artifact cleaned cleanly!")
