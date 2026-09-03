import cv2
import numpy as np

# Load the authentic Saree model in veranda (kurti base)
src_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_in_kurti_tryon_1788408981254.jpg"
img = cv2.imread(src_path)
h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Mask for fabric: only inside the body area (y: 0.135 to 0.96)
body_mask = np.zeros((h, w), dtype=bool)
body_mask[int(h*0.135):int(h*0.96), int(w*0.18):int(w*0.95)] = True

blue_fabric = (hsv[:, :, 0] >= 90) & (hsv[:, :, 0] <= 135) & (hsv[:, :, 1] > 35) & body_mask

# Shift fabric to rich Emerald Green (matching the green suit reference garment)
hsv[blue_fabric, 0] = 68 # Emerald Green Hue
hsv[blue_fabric, 1] = 195 # Deep rich green saturation
hsv[blue_fabric, 2] = np.clip(hsv[blue_fabric, 2].astype(np.float32) * 1.08 + 10, 20, 185).astype(np.uint8)

# Convert embroidery borders and trim to delicate Gold Peacock piping
gold_trim = blue_fabric & (img[:, :, 2] > 105) & (img[:, :, 0] > 85)
hsv[gold_trim, 0] = 22 # Warm Gold
hsv[gold_trim, 1] = 150
hsv[gold_trim, 2] = 220

# Flared pants strictly in legs region (x in [0.28, 0.44], y in [0.70, 0.83])
legs_mask = np.zeros((h, w), dtype=bool)
legs_mask[int(h*0.70):int(h*0.83), int(w*0.28):int(w*0.44)] = True
pants_green = legs_mask & (hsv[:, :, 2] > 160) & (hsv[:, :, 1] < 45)
hsv[pants_green, 0] = 68
hsv[pants_green, 1] = 180
hsv[pants_green, 2] = 135

green_tryon_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Apply only inside body region to keep background pillars 100% clean
res = img.copy()
res[body_mask] = green_tryon_result[body_mask]

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", res)
print("Pristine Emerald Green Suit Tryon with EXACT Saree Model face, neck & hands generated!")
