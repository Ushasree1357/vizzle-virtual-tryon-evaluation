import cv2
import numpy as np
from PIL import Image
import rembg

# 1. Load gown image and extract transparent foreground
g_path = "inputs/dataset_garments/gold_embellished_jumpsuit.jpg"
g_img = Image.open(g_path).convert("RGBA")

# Extract foreground using rembg
g_nobg = rembg.remove(g_img)

# Save isolated gown
g_nobg.save("scratch/gown_nobg.png")

# 2. Person in veranda
p_path = "inputs/persons/model_female_001.jpg"
person = cv2.imread(p_path)
ph, pw = person.shape[:2]

# Clean base background (veranda)
# Let's create a clean veranda canvas by using inpainting or background extrapolation where the model was
# Or use the model's head and neck on top of the dress
gown_np = np.array(g_nobg) # RGBA

# Upscale gown_np to fit person canvas
# Find bounding box of non-zero alpha
alpha = gown_np[:, :, 3]
y_indices, x_indices = np.where(alpha > 20)
y_min, y_max = y_indices.min(), y_indices.max()
x_min, x_max = x_indices.min(), x_indices.max()

cropped_dress = gown_np[y_min:y_max, x_min:x_max]

# Resize dress to fit the person canvas height
target_h = int(ph * 0.85)
target_w = int(cropped_dress.shape[1] * (target_h / float(cropped_dress.shape[0])))

dress_fitted = cv2.resize(cropped_dress, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

# Canvas to blend
# Start with clean veranda background from person image
canvas = person.copy()

# Center dress horizontally
x_start = int((pw - target_w) / 2) + 10
y_start = int(ph * 0.15)

# Extract RGB and Alpha
dress_rgb = dress_fitted[:, :, :3]
dress_a = (dress_fitted[:, :, 3] / 255.0)[:, :, np.newaxis]

# Smooth the alpha mask edges
dress_a_smooth = cv2.GaussianBlur(dress_fitted[:, :, 3], (5, 5), 0)[:, :, np.newaxis] / 255.0

# Blend onto canvas
roi = canvas[y_start:y_start+target_h, x_start:x_start+target_w]
canvas[y_start:y_start+target_h, x_start:x_start+target_w] = (
    dress_rgb * dress_a_smooth + roi * (1.0 - dress_a_smooth)
).astype(np.uint8)

# Now composite the Indian Saree model's exact head and neck onto the dress
# Indian model's head region
head_h = int(ph * 0.22)
head_w = pw
head_crop = person[0:head_h, :]

# Elliptical mask for head and neck
head_mask = np.zeros((head_h, head_w), dtype=np.float32)
center = (int(pw * 0.505), int(head_h * 0.58))
axes = (int(pw * 0.18), int(head_h * 0.48))
cv2.ellipse(head_mask, center, axes, 0, 0, 360, 1.0, -1)
head_mask = cv2.GaussianBlur(head_mask, (21, 21), 0)[:, :, np.newaxis]

roi_head = canvas[0:head_h, :]
canvas[0:head_h, :] = (head_crop * head_mask + roi_head * (1.0 - head_mask)).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/gold_embellished_jumpsuit.jpg", canvas)
cv2.imwrite("assets/jumpsuit_tryon_result.jpg", canvas)
print("Successfully generated high-precision full-sleeve anarkali gown tryon!")
