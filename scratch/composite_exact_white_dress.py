import cv2
import numpy as np
from PIL import Image

# 1. Load white dress RGBA (rembg)
g_nobg = Image.open("scratch/white_dress_nobg.png").convert("RGBA")
dress_rgba = np.array(g_nobg)

# Convert RGB to BGR
dress_bgra = np.zeros_like(dress_rgba)
dress_bgra[:, :, 0] = dress_rgba[:, :, 2]
dress_bgra[:, :, 1] = dress_rgba[:, :, 1]
dress_bgra[:, :, 2] = dress_rgba[:, :, 0]
dress_bgra[:, :, 3] = dress_rgba[:, :, 3]

# 2. Load original crisp person in veranda
person = cv2.imread("inputs/persons/model_female_001.jpg")
ph, pw = person.shape[:2]

# Clean base: Start with original crisp person image
canvas = person.copy()

# Patch the red saree pallu sticking out on the lower right (x: 480-600, y: 550-800) with the clean pillar & stone step
# Copy pillar texture from above to cover the red pallu
patch_src = person[250:500, int(pw*0.78):pw]
patch_h, patch_w = patch_src.shape[:2]
canvas[int(ph*0.62):int(ph*0.62)+patch_h, int(pw*0.78):pw] = patch_src

# Cover any lower right floor red fringe with clean floor stone (from left side floor x: 50-180, y: 700-850)
floor_src = person[int(ph*0.75):int(ph*0.95), int(pw*0.05):int(pw*0.25)]
floor_src_flipped = cv2.flip(floor_src, 1)
fh, fw = floor_src.shape[:2]
canvas[int(ph*0.75):int(ph*0.75)+fh, int(pw*0.75):int(pw*0.75)+fw] = floor_src_flipped

# 3. Extract and scale the exact white sequence dress
alpha = dress_bgra[:, :, 3]
y_idx, x_idx = np.where(alpha > 20)

cropped_dress = dress_bgra[y_idx.min():y_idx.max(), x_idx.min():x_idx.max()]
target_h = int(ph * 0.86)
target_w = int(cropped_dress.shape[1] * (target_h / float(cropped_dress.shape[0])))

dress_fitted = cv2.resize(cropped_dress, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Place dress cleanly
x_offset = int((pw - target_w) / 2) + 4
y_offset = int(ph * 0.11)

d_bgr = dress_fitted[:, :, :3]
d_alpha = cv2.GaussianBlur(dress_fitted[:, :, 3], (3, 3), 0).astype(np.float32) / 255.0
d_alpha = d_alpha[:, :, np.newaxis]

roi = canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w]
canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w] = (
    d_bgr * d_alpha + roi * (1.0 - d_alpha)
).astype(np.uint8)

# 4. Seamlessly blend the Indian Model's exact head and neck at top
head_h = int(ph * 0.20)
head_crop = person[0:head_h, :]

head_mask = np.zeros((head_h, pw), dtype=np.float32)
cv2.ellipse(head_mask, (int(pw * 0.505), int(head_h * 0.52)), (int(pw * 0.14), int(head_h * 0.46)), 0, 0, 360, 1.0, -1)
head_mask = cv2.GaussianBlur(head_mask, (15, 15), 0)[:, :, np.newaxis]

canvas[0:head_h, :] = (head_crop * head_mask + canvas[0:head_h, :] * (1.0 - head_mask)).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", canvas)
print("Pristine, crisp exact white sequence dress tryon created!")
