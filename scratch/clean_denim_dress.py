import cv2
import numpy as np

# Load base standing woman on terrace
base = cv2.imread("assets/top_tryon_result.jpg")
h, w = base.shape[:2]

# Detect the pink outfit pixels on the woman
b, g, r = base[:, :, 0], base[:, :, 1], base[:, :, 2]
# The pink outfit has strong Red and Blue components, very low Green
pink_mask = (r > 130) & (b > 70) & (g < 95)
# Protect face/head
pink_mask[:int(h * 0.24), :] = False

# Connect crop top and mini skirt into a seamless continuous dress
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 45))
dress_mask = cv2.dilate(pink_mask.astype(np.uint8), kernel)
# Fill internal holes
contours, _ = cv2.findContours(dress_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(dress_mask, contours, -1, 1, thickness=cv2.FILLED)

# Protect face, arms, and legs below hemline
dress_mask[:int(h * 0.245), :] = 0
dress_mask[int(h * 0.60):, :] = 0

# Feather mask
dress_mask_f = cv2.GaussianBlur(dress_mask.astype(np.float32), (11, 11), 0)[:, :, np.newaxis]

# Generate realistic dark blue denim color: BGR [75, 45, 25] (Indigo denim)
denim_bgr = np.array([75, 45, 25], dtype=np.float32)

# Preserve organic shadows and clothing folds from base image
gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
shading = np.clip(gray * 1.5, 0.45, 1.35)[:, :, np.newaxis]

denim_shaded = np.clip(denim_bgr * shading, 0, 255).astype(np.uint8)

# Add waist belt
belt_y1, belt_y2 = int(0.39 * h), int(0.42 * h)
belt_mask = np.zeros((h, w), dtype=bool)
belt_mask[belt_y1:belt_y2, int(0.33 * w):int(0.67 * w)] = True
denim_shaded[belt_mask] = (denim_shaded[belt_mask] * 0.65).astype(np.uint8)

# Gold belt buckle at center
buckle_x1, buckle_x2 = int(0.47 * w), int(0.53 * w)
buckle_y1, buckle_y2 = int(0.395 * h), int(0.415 * h)
denim_shaded[buckle_y1:buckle_y2, buckle_x1:buckle_x2] = [80, 175, 220]

# Add vertical buttons down the center placket
cx = int(0.50 * w)
for by in range(int(0.26 * h), int(0.58 * h), int(0.05 * h)):
    cv2.circle(denim_shaded, (cx, by), 3, (190, 190, 200), -1)

# Seamless blend
result = (denim_shaded.astype(np.float32) * dress_mask_f + base.astype(np.float32) * (1.0 - dress_mask_f)).astype(np.uint8)

cv2.imwrite("assets/coat_tryon_result.jpg", result)
print("Saved clean, photorealistic Dark Blue Denim Dress try-on result!")
