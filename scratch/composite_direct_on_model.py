import cv2
import numpy as np
from PIL import Image

# 1. Clean background of veranda (with no red pallu)
clean_bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_no_jewelry_tryon_1788362616967.jpg")
h, w = clean_bg.shape[:2]

# Inpaint center to give clean floor and door
inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[0:int(h*0.96), int(w*0.18):int(w*0.82)] = 255
clean_veranda = cv2.inpaint(clean_bg, inpaint_mask, 5, cv2.INPAINT_TELEA)

# 2. Original Saree model photo (for the pristine head, face, jewelry)
model_orig = cv2.imread("inputs/persons/model_female_001.jpg")
sh, sw = model_orig.shape[:2]

# Scale model_orig to match canvas dimensions if needed
model_scaled = cv2.resize(model_orig, (w, h), interpolation=cv2.INTER_LANCZOS4)

# 3. Load isolated emerald green dress
g_nobg = Image.open("scratch/green_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

# Extract dress from top of thin straps down to feet
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)

# Include the thin straps (y ~ 5% of dress crop)
y_strap = y_idx.min() + int((y_idx.max() - y_idx.min()) * 0.05)
dress_crop = dress_bgra[y_strap:y_idx.max(), x_idx.min():x_idx.max()]
dh, dw = dress_crop.shape[:2]

# Scale dress to match model proportions
target_w = int(w * 0.88)
target_h = int(dh * (target_w / float(dw)))

y_pos = int(h * 0.142) # Straps connect right below the gold choker at y=0.142
if y_pos + target_h > h:
    target_h = h - y_pos
    target_w = int(dw * (target_h / float(dh)))

dress_fitted = cv2.resize(dress_crop, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
x_pos = int((w - target_w) / 2) + 2

# Base: Clean veranda
final_img = clean_veranda.copy()

# Layer 1: Place the high-res Saree Model Head (hair, bindi, face, neck, choker)
head_h = int(h * 0.165)
final_img[0:head_h, :] = model_scaled[0:head_h, :]

# Layer 2: Seamlessly composite the Emerald Green Sleeveless Suit over the body
d_bgr = dress_fitted[:, :, :3]
d_mask = (dress_fitted[:, :, 3] > 40).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
d_mask = cv2.erode(d_mask, kernel, iterations=1)
d_alpha = cv2.GaussianBlur(d_mask, (5, 5), 0).astype(np.float32) / 255.0
d_alpha = d_alpha[:, :, np.newaxis]

roi = final_img[y_pos:y_pos+target_h, x_pos:x_pos+target_w]
final_img[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = (
    d_bgr * d_alpha + roi * (1.0 - d_alpha)
).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", final_img)
print("Finished perfect high-res Emerald Green Suit Tryon with crisp Saree Model Face!")
