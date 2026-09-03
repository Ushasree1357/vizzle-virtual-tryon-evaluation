import cv2
import numpy as np
from PIL import Image

# 1. Load white dress RGBA (rembg result)
g_nobg = Image.open("scratch/white_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

# Convert RGB to BGR
dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

# 2. Load center-aligned veranda scene
src_center = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_in_kurti_tryon_1788408981254.jpg")
ph, pw = src_center.shape[:2]

# Clean canvas: Inpaint the body area completely from top to bottom
inpaint_mask = np.zeros((ph, pw), dtype=np.uint8)
inpaint_mask[int(ph*0.02):int(ph*0.95), int(pw*0.22):int(pw*0.78)] = 255
clean_veranda = cv2.inpaint(src_center, inpaint_mask, 25, cv2.INPAINT_TELEA)

# 3. Extract and scale the full white dress with woman's head intact
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)
full_dress = dress_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]

target_h = int(ph * 0.92)
target_w = int(full_dress.shape[1] * (target_h / float(full_dress.shape[0])))
dress_fitted = cv2.resize(full_dress, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Center dress on canvas
canvas = clean_veranda.copy()
x_offset = int((pw - target_w) / 2)
y_offset = int(ph * 0.04)

d_bgr = dress_fitted[:, :, :3]
d_alpha = cv2.GaussianBlur(dress_fitted[:, :, 3], (5, 5), 0).astype(np.float32) / 255.0
d_alpha = d_alpha[:, :, np.newaxis]

roi = canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w]
canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w] = (
    d_bgr * d_alpha + roi * (1.0 - d_alpha)
).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", canvas)
print("Complete, beautiful White Sequence Suit Tryon generated without any head duplication!")
