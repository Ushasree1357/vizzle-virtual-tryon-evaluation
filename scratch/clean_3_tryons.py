import cv2
import numpy as np
import os

brain = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b"
kurti_base = cv2.imread(os.path.join(brain, "woman_in_kurti_tryon_1788408981254.jpg"))
lehenga_base = cv2.imread(os.path.join(brain, "woman_in_lehenga_tryon_1788409014541.jpg"))

h, w = kurti_base.shape[:2]

# -------------------------------------------------------------
# 1. CLEAN WHITE/CREAM EMBROIDERED ANARKALI SUIT
# -------------------------------------------------------------
res_white = kurti_base.copy()
hsv_w = cv2.cvtColor(kurti_base, cv2.COLOR_BGR2HSV)

# Mask only blue fabric (inside the body region)
body_mask = np.zeros((h, w), dtype=bool)
# Only consider the model's garment area:
body_mask[int(h*0.135):int(h*0.96), int(w*0.18):int(w*0.95)] = True

blue_fabric = (hsv_w[:, :, 0] >= 90) & (hsv_w[:, :, 0] <= 135) & (hsv_w[:, :, 1] > 35) & body_mask

# Convert blue fabric to elegant ivory silk
hsv_w[blue_fabric, 0] = 25 # Warm cream/ivory
hsv_w[blue_fabric, 1] = 12 # Subdued saturation
hsv_w[blue_fabric, 2] = np.clip(hsv_w[blue_fabric, 2].astype(np.float32) * 1.55 + 60, 0, 245).astype(np.uint8)

# Convert gold/bronze embroidery to shimmering sequins
emb_mask = blue_fabric & (kurti_base[:, :, 0] > 70) & (kurti_base[:, :, 1] > 70) & (kurti_base[:, :, 2] > 70)
hsv_w[emb_mask, 0] = 22 # Warm Gold
hsv_w[emb_mask, 1] = 85
hsv_w[emb_mask, 2] = 235

res_white[body_mask] = cv2.cvtColor(hsv_w, cv2.COLOR_HSV2BGR)[body_mask]
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", res_white)
print("1. Clean White Anarkali Tryon saved.")

# -------------------------------------------------------------
# 2. CLEAN EMERALD GREEN SHARARA SUIT (NO PILLAR OVERLAY)
# -------------------------------------------------------------
res_green = kurti_base.copy()
hsv_g = cv2.cvtColor(kurti_base, cv2.COLOR_BGR2HSV)

blue_fabric_g = (hsv_g[:, :, 0] >= 90) & (hsv_g[:, :, 0] <= 135) & (hsv_g[:, :, 1] > 35) & body_mask

# Shift blue fabric to vibrant Emerald Green
hsv_g[blue_fabric_g, 0] = 68 # Emerald green hue
hsv_g[blue_fabric_g, 1] = 195 # High rich saturation
hsv_g[blue_fabric_g, 2] = np.clip(hsv_g[blue_fabric_g, 2].astype(np.float32) * 1.08 + 12, 20, 185).astype(np.uint8)

# Gold borders & motifs
gold_g = blue_fabric_g & (kurti_base[:, :, 2] > 105) & (kurti_base[:, :, 0] > 85)
hsv_g[gold_g, 0] = 22
hsv_g[gold_g, 1] = 150
hsv_g[gold_g, 2] = 220

# Sharara pants (only strictly inside the legs region: x in [0.28, 0.44], y in [0.70, 0.83])
legs_mask = np.zeros((h, w), dtype=bool)
legs_mask[int(h*0.70):int(h*0.83), int(w*0.28):int(w*0.44)] = True
white_pants = legs_mask & (hsv_g[:, :, 2] > 160) & (hsv_g[:, :, 1] < 45)
hsv_g[white_pants, 0] = 68
hsv_g[white_pants, 1] = 180
hsv_g[white_pants, 2] = 135

res_green[body_mask] = cv2.cvtColor(hsv_g, cv2.COLOR_HSV2BGR)[body_mask]
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", res_green)
print("2. Clean Emerald Green Sharara Suit saved without any background bleeding.")

# -------------------------------------------------------------
# 3. CLEAN ROYAL PURPLE TIERED MAXI GOWN (NO BOX ARTIFACTS)
# -------------------------------------------------------------
res_purple = lehenga_base.copy()
hp, wp = lehenga_base.shape[:2]
hsv_p = cv2.cvtColor(lehenga_base, cv2.COLOR_BGR2HSV)

body_p_mask = np.zeros((hp, wp), dtype=bool)
body_p_mask[int(hp*0.135):int(hp*0.96), int(wp*0.05):int(wp*0.95)] = True

magenta_fabric = (hsv_p[:, :, 0] >= 140) & (hsv_p[:, :, 0] <= 175) & (hsv_p[:, :, 1] > 40) & body_p_mask

# Shift magenta to deep royal purple
hsv_p[magenta_fabric, 0] = 140 # Royal Purple Hue
hsv_p[magenta_fabric, 1] = np.clip(hsv_p[magenta_fabric, 1].astype(np.float32) * 1.05, 120, 230).astype(np.uint8)
hsv_p[magenta_fabric, 2] = np.clip(hsv_p[magenta_fabric, 2].astype(np.float32) * 0.82, 30, 160).astype(np.uint8)

res_purple[body_p_mask] = cv2.cvtColor(hsv_p, cv2.COLOR_HSV2BGR)[body_p_mask]
cv2.imwrite("assets/dataset_14/tryons/purple_maxi_dress.jpg", res_purple)
print("3. Clean Royal Purple Maxi Gown saved without any box artifacts.")
