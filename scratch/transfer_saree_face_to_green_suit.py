import cv2
import numpy as np

# 1. Reload the pristine green tryon base (before the previous head overlay)
# We can recreate it quickly from green_dress_nobg.png on clean canvas
from PIL import Image

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
inpaint_mask[0:int(h*0.96), int(w*0.20):int(w*0.80)] = 255
clean_canvas = cv2.inpaint(bg, inpaint_mask, 35, cv2.INPAINT_TELEA)

# 3. Fit green dress
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)
cropped = dress_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]

target_h = int(h * 0.88)
target_w = int(cropped.shape[1] * (target_h / float(cropped.shape[0])))
fitted = cv2.resize(cropped, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

x_pos = int((w - target_w) / 2)
y_pos = int(h * 0.08)

src_img = np.zeros((h, w, 3), dtype=np.uint8)
src_mask = np.zeros((h, w), dtype=np.uint8)

src_img[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = fitted[:, :, :3]
raw_mask = (fitted[:, :, 3] > 40).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
src_mask[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = cv2.erode(raw_mask, kernel, iterations=1)

src_mask_feather = cv2.GaussianBlur(src_mask, (5, 5), 0)
alpha_norm = (src_mask_feather / 255.0)[:, :, np.newaxis]

composite = (src_img * alpha_norm + clean_canvas * (1.0 - alpha_norm)).astype(np.uint8)

# 4. Extract Saree Girl's exact head and neck from model_female_001.jpg
saree_img = cv2.imread("inputs/persons/model_female_001.jpg")
sh, sw = saree_img.shape[:2]

# Head crop from top to collarbone (y: 0 to 22%)
head_crop_raw = saree_img[0:int(sh*0.225), int(sw*0.25):int(sw*0.75)]
hch, hcw = head_crop_raw.shape[:2]

# Target dimensions on composite:
# The green dress neckline is at y ~ int(h*0.24), center x ~ int(w*0.505)
target_head_w = int(w * 0.32)
target_head_h = int(hch * (target_head_w / float(hcw)))
head_resized = cv2.resize(head_crop_raw, (target_head_w, target_head_h), interpolation=cv2.INTER_LANCZOS4)

# Place head directly resting on green neckline
hx_start = int(w * 0.505 - target_head_w / 2)
hy_start = int(h * 0.05)

# Create smooth elliptical blend mask for head, face, hair bun, earrings, and choker
head_blend_mask = np.zeros((target_head_h, target_head_w), dtype=np.float32)
cv2.ellipse(head_blend_mask, (int(target_head_w * 0.50), int(target_head_h * 0.48)), 
            (int(target_head_w * 0.44), int(target_head_h * 0.48)), 0, 0, 360, 1.0, -1)
head_blend_mask = cv2.GaussianBlur(head_blend_mask, (15, 15), 0)[:, :, np.newaxis]

roi = composite[hy_start:hy_start+target_head_h, hx_start:hx_start+target_head_w]
composite[hy_start:hy_start+target_head_h, hx_start:hx_start+target_head_w] = (
    head_resized * head_blend_mask + roi * (1.0 - head_blend_mask)
).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", composite)
print("Saree model face & head seamlessly blended onto Emerald Green Suit!")
