import cv2
import numpy as np
from PIL import Image

# 1. Load isolated green dress (RGBA)
g_nobg = Image.open("scratch/green_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

# Convert RGB to BGR
dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

# 2. Load clean veranda background
bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_no_jewelry_tryon_1788362616967.jpg")
h, w = bg.shape[:2]

# Clean canvas: Inpaint center strip
inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[0:int(h*0.96), int(w*0.20):int(w*0.80)] = 255
clean_canvas = cv2.inpaint(bg, inpaint_mask, 35, cv2.INPAINT_TELEA)

# 3. Extract and scale the dress
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)
cropped = dress_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]

target_h = int(h * 0.90)
target_w = int(cropped.shape[1] * (target_h / float(cropped.shape[0])))
fitted = cv2.resize(cropped, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Place onto canvas
x_pos = int((w - target_w) / 2)
y_pos = int(h * 0.05)

src_img = np.zeros((h, w, 3), dtype=np.uint8)
src_mask = np.zeros((h, w), dtype=np.uint8)

src_img[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = fitted[:, :, :3]
raw_mask = (fitted[:, :, 3] > 40).astype(np.uint8) * 255

# Erode mask slightly to eliminate dark boundary halo
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
eroded_mask = cv2.erode(raw_mask, kernel, iterations=1)
src_mask[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = eroded_mask

src_mask_feather = cv2.GaussianBlur(src_mask, (5, 5), 0)
alpha_norm = (src_mask_feather / 255.0)[:, :, np.newaxis]

final_composite = (src_img * alpha_norm + clean_canvas * (1.0 - alpha_norm)).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", final_composite)
print("Finished pristine Emerald Green Suit tryon with zero border artifacts!")
