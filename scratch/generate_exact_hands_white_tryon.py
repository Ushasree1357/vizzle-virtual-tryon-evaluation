import cv2
import numpy as np

src_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\woman_in_kurti_tryon_1788408981254.jpg"
img = cv2.imread(src_path)
h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Blue fabric mask (the kurti body and dupatta)
blue_mask = (hsv[:, :, 0] >= 90) & (hsv[:, :, 0] <= 135) & (hsv[:, :, 1] > 35)
blue_mask[:int(h*0.135), :] = False # Preserve head & neck

# Convert blue fabric to ivory white silk
hsv[blue_mask, 0] = 25 # Warm ivory tone
hsv[blue_mask, 1] = 10 # Pure off-white
hsv[blue_mask, 2] = np.clip(hsv[blue_mask, 2].astype(np.float32) * 1.50 + 60, 0, 245).astype(np.uint8)

# Convert all embroidery borders to warm golden bronze sequence work
dark_emb = (hsv[:, :, 0] >= 90) & (hsv[:, :, 0] <= 135) & (hsv[:, :, 2] < 120)
dark_emb[:int(h*0.135), :] = False
hsv[dark_emb, 0] = 20 # Warm Golden Bronze
hsv[dark_emb, 1] = 135
hsv[dark_emb, 2] = 160

# Crisp white pants
pants_mask = np.zeros((h, w), dtype=bool)
pants_mask[int(h*0.70):int(h*0.83), int(w*0.28):int(w*0.44)] = True
white_churidar = pants_mask & (hsv[:, :, 2] > 160) & (hsv[:, :, 1] < 45)
hsv[white_churidar, 0] = 25
hsv[white_churidar, 1] = 10
hsv[white_churidar, 2] = 240

white_anarkali_tryon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Save result
cv2.imwrite("assets/dataset_14/tryons/white_embroidered_anarkali.jpg", white_anarkali_tryon)
print("Gold sequence white anarkali tryon with exact 1st image hands & pose generated!")
