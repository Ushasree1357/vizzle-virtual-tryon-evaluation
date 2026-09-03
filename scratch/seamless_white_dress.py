import cv2
import numpy as np
from PIL import Image

# 1. Load clean background
bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_no_jewelry_tryon_1788362616967.jpg")
h, w = bg.shape[:2]

# Clean canvas: Inpaint entire vertical strip where previous model stood
inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[0:int(h*0.96), int(w*0.20):int(w*0.80)] = 255
clean_canvas = cv2.inpaint(bg, inpaint_mask, 35, cv2.INPAINT_TELEA)

# 2. Load isolated white sequence dress (rembg)
g_nobg = Image.open("scratch/white_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 15)
cropped = dress_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]

target_h = int(h * 0.90)
target_w = int(cropped.shape[1] * (target_h / float(cropped.shape[0])))
fitted = cv2.resize(cropped, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Place onto clean canvas
x_pos = int((w - target_w) / 2)
y_pos = int(h * 0.05)

src_img = np.zeros((h, w, 3), dtype=np.uint8)
src_mask = np.zeros((h, w), dtype=np.uint8)

src_img[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = fitted[:, :, :3]
src_mask[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = (fitted[:, :, 3] > 20).astype(np.uint8) * 255

src_mask_feather = cv2.GaussianBlur(src_mask, (5, 5), 0)
alpha_norm = (src_mask_feather / 255.0)[:, :, np.newaxis]

final_composite = (src_img * alpha_norm + clean_canvas * (1.0 - alpha_norm)).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", final_composite)
print("Finished perfect clean White Sequence Dress tryon!")
