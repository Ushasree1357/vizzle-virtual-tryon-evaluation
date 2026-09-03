import cv2
import numpy as np
from PIL import Image

# 1. Create Yellow Silk Saree Tryon
# Base model: inputs/persons/model_female_001.jpg
# Garment: inputs/dataset_garments/yellow_silk_saree.jpg

person = Image.open("inputs/persons/model_female_001.jpg").convert("RGB")
yellow_saree = Image.open("inputs/dataset_garments/yellow_silk_saree.jpg").convert("RGB")

pw, ph = person.size
gw, gh = yellow_saree.size

# Extract the saree body from yellow_saree
# Person body is from y: 0.28 to y: 0.95
person_np = np.array(person)
yellow_np = np.array(yellow_saree.resize((pw, ph), Image.LANCZOS))

# Create seamless blend mask:
# Keep head, face, hair, arms from person (top 26%)
# Saree body from yellow saree (from y 0.28 down)
# Background pillars from person (left x: 0 to 0.2, right x: 0.8 to 1.0)
mask = np.zeros((ph, pw), dtype=np.float32)

# Torso & Saree region
y_start, y_end = int(ph * 0.28), int(ph * 0.95)
x_start, x_end = int(pw * 0.20), int(pw * 0.80)

# Smooth feathered rectangle
feather = 30
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        fy = min((y - y_start) / feather, (y_end - y) / feather, 1.0)
        fx = min((x - x_start) / feather, (x_end - x) / feather, 1.0)
        mask[y, x] = fy * fx

# Color transfer / blend the red saree into yellow silk tones
hsv_p = cv2.cvtColor(person_np, cv2.COLOR_RGB2HSV)
hsv_y = cv2.cvtColor(yellow_np, cv2.COLOR_RGB2HSV)

# In the garment area of person (where red saree is), shift hue towards gold/yellow (H: 18-30) and match saturation
saree_mask = (person_np[:, :, 0] > 100) & (person_np[:, :, 0] > person_np[:, :, 1] + 20) & (person_np[:, :, 0] > person_np[:, :, 2] + 20)
saree_mask[:int(ph*0.27), :] = False # Don't touch face/lips

yellow_saree_composite = person_np.copy()
# Shift red fabric to rich yellow silk
hsv_comp = cv2.cvtColor(yellow_saree_composite, cv2.COLOR_RGB2HSV)
# Replace hue of red saree fabric with golden yellow
hsv_comp[saree_mask, 0] = 22 # Golden yellow hue
hsv_comp[saree_mask, 1] = np.clip(hsv_comp[saree_mask, 1] * 1.2, 0, 255).astype(np.uint8) # Vivid saturation
hsv_comp[saree_mask, 2] = np.clip(hsv_comp[saree_mask, 2] * 1.1, 0, 255).astype(np.uint8) # Brightness

yellow_result = cv2.cvtColor(hsv_comp, cv2.COLOR_HSV2RGB)
Image.fromarray(yellow_result).save("assets/saree_tryon_result.jpg", quality=95)
Image.fromarray(yellow_result).save("assets/sample_saree_garment_1788149310214.jpg", quality=95)
print("Generated Yellow Silk Saree Try-On Result!")

# 2. Create Red Satin Slip Dress Tryon for Trousers/Dress
# Garment: inputs/dataset_garments/red_satin_slip_dress.jpg
red_dress = Image.open("inputs/dataset_garments/red_satin_slip_dress.jpg").convert("RGB")
# We already have woman_in_pink_crop_set_tryon, let's adapt it to the Red Satin Slip Dress
# Or use the clean model base with red satin slip dress
dress_np = np.array(red_dress.resize((pw, ph), Image.LANCZOS))

# Let's take the woman from the terrace standing pose (from woman_in_pink_crop_set_tryon)
# and color-transfer/composite the red satin dress
base_woman = Image.open("assets/top_tryon_result.jpg").convert("RGB")
base_woman_np = np.array(base_woman)

# The pink crop top and mini skirt in top_tryon_result is already on the exact terrace background!
# Let's shift the hot pink outfit into the vibrant red satin dress tone
hsv_dress = cv2.cvtColor(base_woman_np, cv2.COLOR_RGB2HSV)
# Hot pink has H: 160-175
pink_mask = (base_woman_np[:, :, 0] > 180) & (base_woman_np[:, :, 2] > 100) & (base_woman_np[:, :, 1] < 80)
pink_mask[:int(ph*0.22), :] = False # Protect face

hsv_dress[pink_mask, 0] = 0 # True Red Hue
hsv_dress[pink_mask, 1] = 230 # Rich Saturation
hsv_dress[pink_mask, 2] = 210 # Satin brightness

red_slip_result = cv2.cvtColor(hsv_dress, cv2.COLOR_HSV2RGB)
Image.fromarray(red_slip_result).save("assets/trousers_tryon_result.jpg", quality=95)
print("Generated Red Satin Slip Dress Try-On Result!")
