import cv2
import numpy as np

orig = cv2.imread("inputs/persons/model_female_001.jpg")
h1, w1 = orig.shape[:2]

gen = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_no_dupatta_flawless_1788439177260.jpg")
hg, wg = gen.shape[:2]

# In gen, hair bun starts at y = 105, feet end at y = 1205 (total height of person = 1100 px)
# In orig, hair bun starts at y = 20, feet/hem end at y = 690 (total height = 670 px out of 711 = 94.2% of frame!)
# In gen, person height is 1100 / 1264 = 87.0% of frame.
# To match Image 1's exact scale, framing, and headroom:
# Top crop starts around y = 80, bottom crop around y = 1245
# Width crop to maintain aspect ratio 2:3

target_aspect = w1 / float(h1) # 474 / 711 = 0.6666

# Crop box in gen:
crop_y1 = int(hg * 0.055) # cut off excess headroom
crop_y2 = int(hg * 0.985)
crop_h = crop_y2 - crop_y1

crop_w = int(crop_h * target_aspect)
center_x = int(wg * 0.50)
crop_x1 = int(center_x - crop_w / 2)
crop_x2 = crop_x1 + crop_w

aligned = gen[crop_y1:crop_y2, crop_x1:crop_x2]
aligned_resized = cv2.resize(aligned, (wg, hg), interpolation=cv2.INTER_LANCZOS4)

cv2.imwrite(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_exact_framing.jpg", aligned_resized)
print("Aligned image generated with exact Image 1 scale and framing!")
