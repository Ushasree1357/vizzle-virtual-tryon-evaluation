import cv2
import numpy as np
from PIL import Image

# 1. Load the isolated emerald green dress from rembg
g_nobg = Image.open("scratch/green_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

# Convert RGB to BGR
dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

# 2. Clean veranda background
bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_no_jewelry_tryon_1788362616967.jpg")
h, w = bg.shape[:2]

# Clean canvas: inpaint center column
inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[0:int(h*0.96), int(w*0.18):int(w*0.82)] = 255
clean_canvas = cv2.inpaint(bg, inpaint_mask, 35, cv2.INPAINT_TELEA)

# 3. Extract the emerald green dress (from chest/straps down to feet)
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)

# Extract full body including shoulders and straps
full_dress = dress_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]
dh, dw = full_dress.shape[:2]

# Scale dress to fit the veranda canvas
target_w = int(w * 0.78)
target_h = int(dh * (target_w / float(dw)))
if target_h > int(h * 0.90):
    target_h = int(h * 0.90)
    target_w = int(dw * (target_h / float(dh)))

dress_fitted = cv2.resize(full_dress, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Position dress in center of veranda
x_pos = int((w - target_w) / 2)
y_pos = int(h * 0.08)

# Layer 1: Dress composite on clean veranda
dress_layer = clean_canvas.copy()
d_bgr = dress_fitted[:, :, :3]
d_mask = (dress_fitted[:, :, 3] > 40).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
d_mask = cv2.erode(d_mask, kernel, iterations=1)
d_alpha = cv2.GaussianBlur(d_mask, (5, 5), 0).astype(np.float32) / 255.0
d_alpha = d_alpha[:, :, np.newaxis]

roi = dress_layer[y_pos:y_pos+target_h, x_pos:x_pos+target_w]
dress_layer[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = (
    d_bgr * d_alpha + roi * (1.0 - d_alpha)
).astype(np.uint8)

# 4. Extract Saree Girl's exact head, face, hair bun, bindi, maang tikka, and neck from model_female_001.jpg
saree_img = cv2.imread("inputs/persons/model_female_001.jpg")
sh, sw = saree_img.shape[:2]

# Head crop from top down to neck/collarbone (y: 0 to 20%)
# In model_female_001, head is centered at sw * 0.50
head_raw = saree_img[0:int(sh*0.20), int(sw*0.28):int(sw*0.72)]
hrh, hrw = head_raw.shape[:2]

# Scale Saree girl's head to match the green dress body proportions
head_target_w = int(w * 0.22)
head_target_h = int(hrh * (head_target_w / float(hrw)))
head_scaled = cv2.resize(head_raw, (head_target_w, head_target_h), interpolation=cv2.INTER_LANCZOS4)

# Target position on the green dress neckline (where the spaghetti straps meet the shoulders)
# Neck center is at x ~ w * 0.495, y ~ y_pos (starts at top of dress)
hx = int(w * 0.495 - head_target_w / 2)
hy = int(y_pos - head_target_h * 0.45) # Head sits right above the square neckline

# Seamless elliptical mask for face, hair bun, bindi, maang tikka, and neck
h_mask = np.zeros((head_target_h, head_target_w), dtype=np.float32)
cv2.ellipse(h_mask, (int(head_target_w * 0.50), int(head_target_h * 0.48)), 
            (int(head_target_w * 0.44), int(head_target_h * 0.46)), 0, 0, 360, 1.0, -1)
h_mask = cv2.GaussianBlur(h_mask, (15, 15), 0)[:, :, np.newaxis]

# Blend Saree girl's head seamlessly onto the emerald green dress body
final_canvas = dress_layer.copy()
roi_head = final_canvas[hy:hy+head_target_h, hx:hx+head_target_w]
final_canvas[hy:hy+head_target_h, hx:hx+head_target_w] = (
    head_scaled * h_mask + roi_head * (1.0 - h_mask)
).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/emerald_green_suit.jpg", final_canvas)
print("Perfect Emerald Green Sleeveless Suit Tryon with Saree Girl Face created!")
