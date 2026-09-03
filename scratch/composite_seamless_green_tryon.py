import cv2
import numpy as np
from PIL import Image

# 1. Load green dress RGBA
g_nobg = Image.open("scratch/green_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)
h_g, w_g = dress_rgba.shape[:2]

hsv_g = cv2.cvtColor(dress_rgba[:, :, :3], cv2.COLOR_RGB2HSV)
green_mask = (hsv_g[:, :, 0] >= 35) & (hsv_g[:, :, 0] <= 85) & (hsv_g[:, :, 1] > 40) & (dress_rgba[:, :, 3] > 20)

gy, gx = np.where(green_mask)

# Crop ONLY the green garment starting strictly at the green fabric top
garment_only = dress_rgba[gy.min()-5:gy.max()+5, gx.min():gx.max()]

garment_bgra = np.zeros_like(garment_only)
garment_bgra[:, :, 0] = garment_only[:, :, 2]
garment_bgra[:, :, 1] = garment_only[:, :, 1]
garment_bgra[:, :, 2] = garment_only[:, :, 0]
garment_bgra[:, :, 3] = garment_only[:, :, 3]

# 2. Clean veranda background
clean_bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_no_jewelry_tryon_1788362616967.jpg")
h, w = clean_bg.shape[:2]

inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[0:int(h*0.96), int(w*0.18):int(w*0.82)] = 255
clean_veranda = cv2.inpaint(clean_bg, inpaint_mask, 5, cv2.INPAINT_TELEA)

# 3. Saree model photo
model_orig = cv2.imread("inputs/persons/model_female_001.jpg")
model_scaled = cv2.resize(model_orig, (w, h), interpolation=cv2.INTER_LANCZOS4)

# Base canvas
canvas = clean_veranda.copy()
head_h = int(h * 0.17)
canvas[0:head_h, :] = model_scaled[0:head_h, :]

# 4. Fit Green Garment seamlessly right below the choker (overlapping the red sliver)
gh, gw = garment_bgra.shape[:2]
target_w = int(w * 0.78)
target_h = int(gh * (target_w / float(gw)))

# Connect top of green straps right at base of choker
y_pos = head_h - 26
if y_pos + target_h > h:
    target_h = h - y_pos
    target_w = int(gw * (target_h / float(gh)))

garment_fitted = cv2.resize(garment_bgra, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
x_pos = int((w - target_w) / 2) + 2

g_bgr = garment_fitted[:, :, :3]
g_mask = (garment_fitted[:, :, 3] > 40).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
g_mask = cv2.erode(g_mask, kernel, iterations=1)
g_alpha = cv2.GaussianBlur(g_mask, (5, 5), 0).astype(np.float32) / 255.0
g_alpha = g_alpha[:, :, np.newaxis]

roi = canvas[y_pos:y_pos+target_h, x_pos:x_pos+target_w]
canvas[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = (
    g_bgr * g_alpha + roi * (1.0 - g_alpha)
).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", canvas)
print("Finished perfect Seamless Emerald Green Suit Tryon!")
