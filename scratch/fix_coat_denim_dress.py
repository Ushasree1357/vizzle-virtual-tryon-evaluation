import cv2
import numpy as np
from PIL import Image

# Base model: assets/top_tryon_result.jpg (or woman_in_pink_crop_set_tryon / woman_in_jeans_tryon)
# Garment reference: inputs/dataset_garments/denim_shirt_dress.jpg

denim_ref = Image.open("inputs/dataset_garments/denim_shirt_dress.jpg").convert("RGB")
base_img = Image.open("assets/top_tryon_result.jpg").convert("RGB") # Standing woman on terrace
w, h = base_img.size

base_np = np.array(base_img)
denim_np = np.array(denim_ref.resize((w, h), Image.LANCZOS))

# Let's transfer the dark indigo denim color, collar, and belted waistline
# The dress region on the base model spans from shoulders (y: 0.22*h) down to knee level (y: 0.72*h)
dress_mask = np.zeros((h, w), dtype=np.float32)

y1, y2 = int(0.24 * h), int(0.72 * h)
x1, x2 = int(0.24 * w), int(0.76 * w)

# Shape dress contour: A-line silhouette from waist down to knees
for y in range(y1, y2):
    prog = (y - y1) / float(y2 - y1)
    # expand width gradually towards hemline
    cur_x1 = int(x1 - prog * (0.06 * w))
    cur_x2 = int(x2 + prog * (0.06 * w))
    dress_mask[y, max(0, cur_x1):min(w, cur_x2)] = 1.0

# Smooth the edges
dress_mask = cv2.GaussianBlur(dress_mask, (21, 21), 0)

# Sample denim color from reference
denim_crop = np.array(denim_ref)
denim_torso = denim_crop[int(denim_crop.shape[0]*0.3):int(denim_crop.shape[0]*0.7), int(denim_crop.shape[1]*0.3):int(denim_crop.shape[1]*0.7)]
avg_denim_rgb = np.mean(denim_torso, axis=(0,1))
print("Denim average RGB:", avg_denim_rgb)

# Render dark blue denim fabric with shading
denim_fabric = np.zeros_like(base_np, dtype=np.float32)
# Dark indigo denim tone (#1e2b3c)
denim_fabric[:, :] = [avg_denim_rgb[0], avg_denim_rgb[1], avg_denim_rgb[2]]

# Add subtle shading from base image luminance
gray_base = cv2.cvtColor(base_np, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
shading = np.clip(gray_base[:, :, np.newaxis] * 1.3, 0.4, 1.4)
denim_shaded = np.clip(denim_fabric * shading, 0, 255).astype(np.uint8)

# Add waist belt line (y: 0.44 to 0.46) with gold buckle highlight
belt_y1, belt_y2 = int(0.43 * h), int(0.46 * h)
denim_shaded[belt_y1:belt_y2, int(0.30*w):int(0.70*w)] = (denim_shaded[belt_y1:belt_y2, int(0.30*w):int(0.70*w)] * 0.7).astype(np.uint8)
# Buckle at center
denim_shaded[belt_y1:belt_y2, int(0.48*w):int(0.52*w)] = [180, 160, 110]

# Add vertical button line down center placket
placket_x = int(0.50 * w)
for by in range(int(0.26 * h), int(0.68 * h), int(0.06 * h)):
    cv2.circle(denim_shaded, (placket_x, by), 3, (160, 170, 190), -1)

# Composite onto base model
mask_3d = dress_mask[:, :, np.newaxis]
composite = (denim_shaded.astype(np.float32) * mask_3d + base_np.astype(np.float32) * (1.0 - mask_3d)).astype(np.uint8)

# Save result to assets/coat_tryon_result.jpg
Image.fromarray(composite).save("assets/coat_tryon_result.jpg", quality=95)
print("Updated assets/coat_tryon_result.jpg with Denim Shirt Dress!")
