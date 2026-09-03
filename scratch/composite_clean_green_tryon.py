import cv2
import numpy as np
from PIL import Image

# 1. Load isolated green dress
g_nobg = Image.open("scratch/green_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

# 2. Clean veranda background
bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_no_jewelry_tryon_1788362616967.jpg")
h, w = bg.shape[:2]

inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[0:int(h*0.96), int(w*0.18):int(w*0.82)] = 255
clean_canvas = cv2.inpaint(bg, inpaint_mask, 5, cv2.INPAINT_TELEA)

# 3. Fit green dress
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)

y_neck = y_idx.min() + int((y_idx.max() - y_idx.min()) * 0.16)
dress_only = dress_bgra[y_neck:y_idx.max(), x_idx.min():x_idx.max()]
dh, dw = dress_only.shape[:2]

target_w = int(w * 0.78)
target_h = int(dh * (target_w / float(dw)))
if target_h > int(h * 0.80):
    target_h = int(h * 0.80)
    target_w = int(dw * (target_h / float(dh)))

dress_fitted = cv2.resize(dress_only, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

x_pos = int((w - target_w) / 2)
y_pos = int(h * 0.18)

canvas = clean_canvas.copy()
d_bgr = dress_fitted[:, :, :3]
d_mask = (dress_fitted[:, :, 3] > 40).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
d_mask = cv2.erode(d_mask, kernel, iterations=1)
d_alpha = cv2.GaussianBlur(d_mask, (5, 5), 0).astype(np.float32) / 255.0
d_alpha = d_alpha[:, :, np.newaxis]

roi = canvas[y_pos:y_pos+target_h, x_pos:x_pos+target_w]
canvas[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = (
    d_bgr * d_alpha + roi * (1.0 - d_alpha)
).astype(np.uint8)

# 4. Extract ONLY Head, Face, Earrings, Bindi, Maang Tikka, and Neck Choker (cut strictly at 0.58)
head_nobg = Image.open("scratch/saree_head_nobg.png").convert("RGBA")
head_rgba = np.array(head_nobg)
head_bgra = np.zeros_like(head_rgba)
head_bgra[:, :, 0] = head_rgba[:, :, 2]
head_bgra[:, :, 1] = head_rgba[:, :, 1]
head_bgra[:, :, 2] = head_rgba[:, :, 0]
head_bgra[:, :, 3] = head_rgba[:, :, 3]

hy_idx, hx_idx = np.where(head_bgra[:, :, 3] > 20)
# Cut strictly above the red blouse
y_choker = hy_idx.min() + int((hy_idx.max() - hy_idx.min()) * 0.58)
head_pure = head_bgra[hy_idx.min():y_choker, hx_idx.min():hx_idx.max()]
hch, hcw = head_pure.shape[:2]

head_w_target = int(w * 0.24)
head_h_target = int(hch * (head_w_target / float(hcw)))
head_fitted = cv2.resize(head_pure, (head_w_target, head_h_target), interpolation=cv2.INTER_LANCZOS4)

# Place head so the neck naturally connects to the green square neckline
head_x = int((w - head_w_target) / 2) + 2
head_y = int(y_pos - head_h_target * 0.90)

hb_bgr = head_fitted[:, :, :3]
hb_alpha = cv2.GaussianBlur(head_fitted[:, :, 3], (3, 3), 0).astype(np.float32) / 255.0
hb_alpha = hb_alpha[:, :, np.newaxis]

roi_h = canvas[head_y:head_y+head_h_target, head_x:head_x+head_w_target]
canvas[head_y:head_y+head_h_target, head_x:head_x+head_w_target] = (
    hb_bgr * hb_alpha + roi_h * (1.0 - hb_alpha)
).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", canvas)
print("Finished clean Emerald Green Sleeveless Suit Tryon with naturally connected Saree Girl Face!")
