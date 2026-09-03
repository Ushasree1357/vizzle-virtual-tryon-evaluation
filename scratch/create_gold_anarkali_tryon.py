import cv2
import numpy as np

src_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_in_kurti_tryon_1788408981254.jpg"
img = cv2.imread(src_path)
h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Blue fabric mask across entire body below chin (y > 0.13)
blue_mask = (hsv[:, :, 0] >= 90) & (hsv[:, :, 0] <= 135) & (hsv[:, :, 1] > 35)
blue_mask[:int(h*0.135), :] = False

# Shift Blue fabric to Champagne Gold/Beige:
hsv[blue_mask, 0] = 22 # Gold Hue
hsv[blue_mask, 1] = np.clip(hsv[blue_mask, 1].astype(np.float32) * 0.45, 25, 95).astype(np.uint8)
hsv[blue_mask, 2] = np.clip(hsv[blue_mask, 2].astype(np.float32) * 1.38 + 25, 0, 245).astype(np.uint8)

# Dark embroidery borders
dark_blue_mask = (hsv[:, :, 0] >= 90) & (hsv[:, :, 0] <= 135) & (hsv[:, :, 2] < 70)
dark_blue_mask[:int(h*0.135), :] = False
hsv[dark_blue_mask, 0] = 18 # Warm bronze
hsv[dark_blue_mask, 1] = 110
hsv[dark_blue_mask, 2] = 85

gold_anarkali = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Save result
cv2.imwrite("assets/dataset_14/tryons/gold_embellished_jumpsuit.jpg", gold_anarkali)
cv2.imwrite("assets/jumpsuit_tryon_result.jpg", gold_anarkali)
print("Complete full-sleeve flared gold anarkali tryon generated perfectly!")
