import cv2
import numpy as np
from PIL import Image

# Person in veranda
p_path = "inputs/persons/model_female_001.jpg"
person = cv2.imread(p_path)
ph, pw = person.shape[:2]

# Full sleeve beige gown
g_path = "inputs/dataset_garments/gold_embellished_jumpsuit.jpg"
gown = cv2.imread(g_path)

# Let's crop the gown woman cleanly
# Gown dimensions
gh, gw = gown.shape[:2]

# Upscale gown image for detail
gown_up = cv2.resize(gown, (pw, ph), interpolation=cv2.INTER_CUBIC)

# Person's head mask (from top down to neck)
# Head is roughly top 0% to 22% of person image
head_crop = person[0:int(ph*0.23), :]

# Create seamless composite:
# The gown body (from neck down) + the person's head & upper neck + veranda pillars & background
# Base background: person image
composite = person.copy()

# Gown body mask
# In gown_up, let's extract the full-sleeve dress body
# Dress starts at y = int(ph*0.20) down to int(ph*0.93)
dress_region = gown_up[int(ph*0.20):int(ph*0.93), :]

# Resize dress to fit person's proportions
dh = int(ph*0.75)
dw = int(pw*0.82)
dress_resized = cv2.resize(gown[int(gh*0.16):int(gh*0.92), int(gw*0.05):int(gw*0.95)], (dw, dh), interpolation=cv2.INTER_CUBIC)

# Let's create an alpha matte / clean segment for the dress
# Background in gown image is a smooth gradient (sunset/sky)
# The dress is beige/gold with intricate embroidery
# Let's remove the background using color thresholding / edge blending
hsv_g = cv2.cvtColor(dress_resized, cv2.COLOR_BGR2HSV)
# The sky background has low saturation or distinct hue
bg_mask = (dress_resized[:, :, 0] > 180) & (dress_resized[:, :, 1] > 180) & (dress_resized[:, :, 2] > 190)

# Dress mask
dress_mask = np.ones((dh, dw), dtype=np.uint8) * 255
dress_mask[bg_mask] = 0

# Smooth mask edges
dress_mask = cv2.GaussianBlur(dress_mask, (7, 7), 0)

# Placement coordinates on person
x_offset = int((pw - dw) / 2) + 15
y_offset = int(ph * 0.20)

# Blend dress onto person
for c in range(3):
    alpha = (dress_mask / 255.0)[:, :, np.newaxis]
    target_roi = composite[y_offset:y_offset+dh, x_offset:x_offset+dw]
    composite[y_offset:y_offset+dh, x_offset:x_offset+dw] = (
        dress_resized * alpha + target_roi * (1.0 - alpha)
    ).astype(np.uint8)

# Now restore the model's head, face, hair, and neck with seamless transition
head_h = int(ph * 0.22)
feather = 25
head_mask = np.ones((head_h + feather, pw), dtype=np.float32)
for i in range(feather):
    head_mask[head_h + i, :] = 1.0 - (i / float(feather))

head_full = person[0:head_h+feather, :]
roi_top = composite[0:head_h+feather, :]

for c in range(3):
    composite[0:head_h+feather, :, c] = (
        head_full[:, :, c] * head_mask + roi_top[:, :, c] * (1.0 - head_mask)
    ).astype(np.uint8)

cv2.imwrite("assets/dataset_14/tryons/gold_embellished_jumpsuit.jpg", composite)
cv2.imwrite("assets/jumpsuit_tryon_result.jpg", composite)
print("Synthesized full-hand dress tryon!")
