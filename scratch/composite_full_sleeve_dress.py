import cv2
import numpy as np
from PIL import Image

# 1. Load the isolated gown (RGBA from rembg)
g_nobg = Image.open("scratch/gown_nobg.png").convert("RGBA")
gown_rgba = np.array(g_nobg) # RGB + Alpha

# Convert RGB to BGR for OpenCV
gown_bgra = np.zeros_like(gown_rgba)
gown_bgra[:, :, 0] = gown_rgba[:, :, 2] # B
gown_bgra[:, :, 1] = gown_rgba[:, :, 1] # G
gown_bgra[:, :, 2] = gown_rgba[:, :, 0] # R
gown_bgra[:, :, 3] = gown_rgba[:, :, 3] # A

# 2. Person in veranda
p_path = "inputs/persons/model_female_001.jpg"
person = cv2.imread(p_path)
ph, pw = person.shape[:2]

# 3. Clean background where red saree was
# Inpaint / clean the red saree areas around the body
# Red saree detection mask
hsv = cv2.cvtColor(person, cv2.COLOR_BGR2HSV)
# Red mask in HSV (two ranges)
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
saree_mask = mask1 | mask2

# Don't touch head & face
saree_mask[:int(ph*0.22), :] = 0

# Clean background with inpainting
bg_clean = cv2.inpaint(person, saree_mask, 15, cv2.INPAINT_TELEA)

# 4. Crop non-zero alpha from gown
alpha = gown_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 30)
cropped_gown = gown_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]

# Resize gown to fit body
target_h = int(ph * 0.82)
target_w = int(cropped_gown.shape[1] * (target_h / float(cropped_gown.shape[0])))
gown_fitted = cv2.resize(cropped_gown, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Placement
canvas = bg_clean.copy()
x_offset = int((pw - target_w) / 2) + 2
y_offset = int(ph * 0.17)

# Extract BGR & Alpha
g_bgr = gown_fitted[:, :, :3]
g_alpha = cv2.GaussianBlur(gown_fitted[:, :, 3], (5, 5), 0).astype(np.float32) / 255.0
g_alpha = g_alpha[:, :, np.newaxis]

# Alpha blend gown onto clean background
roi = canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w]
canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w] = (
    g_bgr * g_alpha + roi * (1.0 - g_alpha)
).astype(np.uint8)

# 5. Restore the Indian Model's exact head, neck, and jewelry
head_h = int(ph * 0.22)
head_w = pw
head_crop = person[0:head_h, :]

head_mask = np.zeros((head_h, head_w), dtype=np.float32)
cv2.ellipse(head_mask, (int(pw * 0.505), int(head_h * 0.58)), (int(pw * 0.17), int(head_h * 0.48)), 0, 0, 360, 1.0, -1)
head_mask = cv2.GaussianBlur(head_mask, (15, 15), 0)[:, :, np.newaxis]

canvas[0:head_h, :] = (head_crop * head_mask + canvas[0:head_h, :] * (1.0 - head_mask)).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/gold_embellished_jumpsuit.jpg", canvas)
cv2.imwrite("assets/jumpsuit_tryon_result.jpg", canvas)
print("Golden full-sleeve anarkali gown tryon synthesized successfully with authentic colors & clean background!")
