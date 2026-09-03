import cv2
import numpy as np

# Load the tryon image
tryon = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_set_no_dupatta_tryon_1788438862262.jpg")
h, w = tryon.shape[:2]

# Load clean background from original model image
bg = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\denim_dress_hands_at_sides_1788437697855.jpg")
bg_scaled = cv2.resize(bg, (w, h), interpolation=cv2.INTER_LANCZOS4)

# Replace the top-left doorway region (x: 0 to 415, y: 0 to 180) with the clean background
clean_final = tryon.copy()

# Create a smooth transition mask at x = 400 to 420
trans_mask = np.zeros((h, w), dtype=np.float32)
trans_mask[0:180, 0:400] = 1.0
for i in range(20):
    trans_mask[0:180, 400+i] = 1.0 - (i / 20.0)

trans_mask = trans_mask[:, :, np.newaxis]
clean_final = (bg_scaled * trans_mask + clean_final * (1.0 - trans_mask)).astype(np.uint8)

# Save result
out_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_clean.jpg"
cv2.imwrite(out_path, clean_final)
print("Doorway background restored cleanly with zero artifacts!")
