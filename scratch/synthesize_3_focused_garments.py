import cv2
import numpy as np
import os
import shutil

brain = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b"
kurti_base_path = os.path.join(brain, "woman_in_kurti_tryon_1788408981254.jpg")
lehenga_base_path = os.path.join(brain, "woman_in_lehenga_tryon_1788409014541.jpg")

os.makedirs("assets/dataset_14/garments", exist_ok=True)
os.makedirs("assets/dataset_14/tryons", exist_ok=True)

# -------------------------------------------------------------
# 1. WHITE EMBROIDERED ANARKALI SUIT WITH GOLD SEQUENCE WORK
# -------------------------------------------------------------
img_w = cv2.imread(kurti_base_path)
h, w = img_w.shape[:2]
hsv_w = cv2.cvtColor(img_w, cv2.COLOR_BGR2HSV)

# Blue fabric mask (dress body & dupatta)
fabric_mask = (hsv_w[:, :, 0] >= 90) & (hsv_w[:, :, 0] <= 135) & (hsv_w[:, :, 1] > 30)
fabric_mask[:int(h * 0.135), :] = False # Preserve head & neck

# Convert blue fabric to lustrous ivory / cream white:
# Desaturate heavily, boost value / brightness
hsv_w[fabric_mask, 0] = 25 # Warm ivory tone
hsv_w[fabric_mask, 1] = 12 # Very low saturation (off-white)
hsv_w[fabric_mask, 2] = np.clip(hsv_w[fabric_mask, 2].astype(np.float32) * 1.6 + 65, 0, 245).astype(np.uint8)

# Gold sequence embroidery on neckline and borders:
emb_mask = (fabric_mask) & (img_w[:, :, 0] > 70) & (img_w[:, :, 1] > 70) & (img_w[:, :, 2] > 70)
hsv_w[emb_mask, 0] = 22 # Warm Gold
hsv_w[emb_mask, 1] = 85
hsv_w[emb_mask, 2] = 230

# White churidar / trousers
pants_mask = (hsv_w[:, :, 2] > 170) & (hsv_w[:, :, 1] < 40)
pants_mask[:int(h * 0.65), :] = False
hsv_w[pants_mask, 0] = 25
hsv_w[pants_mask, 1] = 15
hsv_w[pants_mask, 2] = 240

white_tryon = cv2.cvtColor(hsv_w, cv2.COLOR_HSV2BGR)
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", white_tryon)
print("1. White Embroidered Anarkali Tryon synthesized successfully!")

# -------------------------------------------------------------
# 2. EMERALD GREEN SHARARA SUIT WITH GOLD TRIM & DUPATTA
# -------------------------------------------------------------
img_g = cv2.imread(kurti_base_path)
hsv_g = cv2.cvtColor(img_g, cv2.COLOR_BGR2HSV)

fabric_g_mask = (hsv_g[:, :, 0] >= 90) & (hsv_g[:, :, 0] <= 135) & (hsv_g[:, :, 1] > 30)
fabric_g_mask[:int(h * 0.135), :] = False

# Convert blue fabric to deep, rich Emerald Green:
# Hue 65 in OpenCV HSV is emerald green
hsv_g[fabric_g_mask, 0] = 68 # Emerald green
hsv_g[fabric_g_mask, 1] = 195 # Rich saturation
hsv_g[fabric_g_mask, 2] = np.clip(hsv_g[fabric_g_mask, 2].astype(np.float32) * 1.1 + 10, 20, 180).astype(np.uint8)

# Gold trim on neckline, sleeves and dupatta border:
gold_trim_mask = (fabric_g_mask) & (img_g[:, :, 2] > 110) & (img_g[:, :, 0] > 90)
hsv_g[gold_trim_mask, 0] = 22 # Gold
hsv_g[gold_trim_mask, 1] = 160
hsv_g[gold_trim_mask, 2] = 220

# Sharara pants in emerald green
pants_g_mask = (hsv_g[:, :, 2] > 170) & (hsv_g[:, :, 1] < 40)
pants_g_mask[:int(h * 0.65), :] = False
hsv_g[pants_g_mask, 0] = 68
hsv_g[pants_g_mask, 1] = 180
hsv_g[pants_g_mask, 2] = 140

green_tryon = cv2.cvtColor(hsv_g, cv2.COLOR_HSV2BGR)
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", green_tryon)
print("2. Emerald Green Sharara Suit Tryon synthesized successfully!")

# -------------------------------------------------------------
# 3. ROYAL PURPLE TIERED PLEATED MAXI GOWN WITH WAIST BELT
# -------------------------------------------------------------
img_p = cv2.imread(lehenga_base_path)
hp, wp = img_p.shape[:2]
hsv_p = cv2.cvtColor(img_p, cv2.COLOR_BGR2HSV)

# Magenta/pink fabric mask
magenta_mask = (hsv_p[:, :, 0] >= 140) & (hsv_p[:, :, 0] <= 175) & (hsv_p[:, :, 1] > 40)
magenta_mask[:int(hp * 0.135), :] = False # Preserve face & neck

# Convert to deep royal purple:
# Hue 138-145 in OpenCV HSV
hsv_p[magenta_mask, 0] = 140 # Royal Purple
hsv_p[magenta_mask, 1] = np.clip(hsv_p[magenta_mask, 1].astype(np.float32) * 1.05, 120, 230).astype(np.uint8)
hsv_p[magenta_mask, 2] = np.clip(hsv_p[magenta_mask, 2].astype(np.float32) * 0.82, 30, 160).astype(np.uint8)

# Add brown leather waist belt at waist level (y ~ 0.32 to 0.35)
belt_y1 = int(hp * 0.325)
belt_y2 = int(hp * 0.345)
belt_x1 = int(wp * 0.37)
belt_x2 = int(wp * 0.58)

hsv_p[belt_y1:belt_y2, belt_x1:belt_x2, 0] = 12 # Brown
hsv_p[belt_y1:belt_y2, belt_x1:belt_x2, 1] = 160
hsv_p[belt_y1:belt_y2, belt_x1:belt_x2, 2] = 85

purple_tryon = cv2.cvtColor(hsv_p, cv2.COLOR_HSV2BGR)
cv2.imwrite("assets/dataset_14/tryons/purple_maxi_dress.jpg", purple_tryon)
print("3. Royal Purple Tiered Maxi Gown Tryon synthesized successfully!")
