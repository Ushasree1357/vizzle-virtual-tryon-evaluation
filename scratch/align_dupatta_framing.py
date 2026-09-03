import cv2
import numpy as np

orig = cv2.imread("inputs/persons/model_female_001.jpg")
h1, w1 = orig.shape[:2]

# The generation with the complete white suit + dupatta:
gen = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\saree_model_in_white_sequence_kurta_set_1788438426214.jpg")
hg, wg = gen.shape[:2]

target_aspect = w1 / float(h1) # 474 / 711 = 0.6666

# Crop box to match Image 1's exact head top and bottom step level:
# In Image 1:
# top of hair: y / h = 0.035
# chin: y / h = 0.185
# waist: y / h = 0.42
# feet on step: y / h = 0.94
# bottom edge of step: y / h = 0.99

# In gen:
# top of hair is at y = 100 (0.079 * hg)
# feet are at y = 1200 (0.949 * hg)
# bottom step is at y = 1264

crop_y1 = int(hg * 0.046) 
crop_y2 = int(hg * 0.985)
crop_h = crop_y2 - crop_y1

crop_w = int(crop_h * target_aspect)
center_x = int(wg * 0.50)
crop_x1 = int(center_x - crop_w / 2)
crop_x2 = crop_x1 + crop_w

aligned = gen[crop_y1:crop_y2, crop_x1:crop_x2]
aligned_resized = cv2.resize(aligned, (w1, h1), interpolation=cv2.INTER_LANCZOS4)

cv2.imwrite(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_anarkali_with_dupatta_aligned.jpg", aligned_resized)

# Also check difference in face location:
print(f"Orig: {w1}x{h1}, Aligned: {aligned_resized.shape[1]}x{aligned_resized.shape[0]}")
