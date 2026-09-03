import cv2
import numpy as np

# 1. Load gown image and person image
g_path = "inputs/dataset_garments/gold_embellished_jumpsuit.jpg"
gown = cv2.imread(g_path)
gh, gw = gown.shape[:2]

p_path = "inputs/persons/model_female_001.jpg"
person = cv2.imread(p_path)
ph, pw = person.shape[:2]

# Fast precise background removal of the gown:
# The background in the reference photo is a sunset sky (smooth pink/blue/grey gradient)
# The dress and woman have strong texture, saturation, and contrast.
# Convert to LAB / HSV
hsv = cv2.cvtColor(gown, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(gown, cv2.COLOR_BGR2GRAY)

# Sky background has very low texture / high gradient smoothness or specific color range
# Let's use GrabCut with an initialized rectangle
mask = np.zeros((gh, gw), np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# Bounding box of the woman and gown in the image
rect = (int(gw * 0.10), int(gh * 0.05), int(gw * 0.80), int(gh * 0.93))
cv2.grabCut(gown, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# Foreground mask
fg_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Refine mask with morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
fg_mask_blurred = cv2.GaussianBlur(fg_mask.astype(np.float32), (7, 7), 0)

# Extract foreground
fg_gown = gown * fg_mask_blurred[:, :, np.newaxis]

# Find bounding box of extracted foreground
y_indices, x_indices = np.where(fg_mask > 0)
y1, y2 = y_indices.min(), y_indices.max()
x1, x2 = x_indices.min(), x_indices.max()

cropped_fg = fg_gown[y1:y2, x1:x2]
cropped_alpha = fg_mask_blurred[y1:y2, x1:x2]

# Resize to fit person's body
target_h = int(ph * 0.86)
target_w = int(cropped_fg.shape[1] * (target_h / float(cropped_fg.shape[0])))

dress_fitted = cv2.resize(cropped_fg, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
alpha_fitted = cv2.resize(cropped_alpha, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)[:, :, np.newaxis]

# Canvas based on person in veranda
canvas = person.copy()

x_offset = int((pw - target_w) / 2) + 12
y_offset = int(ph * 0.14)

# Blend onto canvas
roi = canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w]
canvas[y_offset:y_offset+target_h, x_offset:x_offset+target_w] = (
    dress_fitted * alpha_fitted + roi * (1.0 - alpha_fitted)
).astype(np.uint8)

# Now seamlessly blend Indian model's head & neck
head_h = int(ph * 0.22)
head_w = pw
head_crop = person[0:head_h, :]

head_mask = np.zeros((head_h, head_w), dtype=np.float32)
cv2.ellipse(head_mask, (int(pw * 0.505), int(head_h * 0.56)), (int(pw * 0.16), int(head_h * 0.46)), 0, 0, 360, 1.0, -1)
head_mask = cv2.GaussianBlur(head_mask, (15, 15), 0)[:, :, np.newaxis]

canvas[0:head_h, :] = (head_crop * head_mask + canvas[0:head_h, :] * (1.0 - head_mask)).astype(np.uint8)

# Save result
cv2.imwrite("assets/dataset_14/tryons/gold_embellished_jumpsuit.jpg", canvas)
cv2.imwrite("assets/jumpsuit_tryon_result.jpg", canvas)
print("GrabCut fast full-sleeve anarkali gown tryon synthesized successfully!")
