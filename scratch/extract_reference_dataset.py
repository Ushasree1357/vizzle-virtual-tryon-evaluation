import cv2
import os

grid_path = r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\.user_uploaded\media_1788409895820.jpg"
grid = cv2.imread(grid_path)
h, w = grid.shape[:2]

r1_h = int(h / 3)
r2_h = int(2 * h / 3)

os.makedirs("inputs/dataset_garments", exist_ok=True)

# Row 1 (5 cols)
c_w = w / 5.0
items = [
    ("pink_crop_skirt_set", 0, r1_h, int(0 * c_w), int(1 * c_w)),
    ("purple_maxi_dress", 0, r1_h, int(1 * c_w), int(2 * c_w)),
    ("black_printed_kurti_set", 0, r1_h, int(2 * c_w), int(3 * c_w)),
    ("white_embroidered_anarkali", 0, r1_h, int(3 * c_w), int(4 * c_w)),
    ("emerald_green_suit", 0, r1_h, int(4 * c_w), int(5 * c_w)),
    
    # Row 2 (5 cols)
    ("pink_embroidered_saree", r1_h, r2_h, int(0 * c_w), int(1 * c_w)),
    ("yellow_silk_saree", r1_h, r2_h, int(1 * c_w), int(2 * c_w)),
    ("black_polo_tshirt", r1_h, r2_h, int(2 * c_w), int(3 * c_w)),
    ("denim_shirt_dress", r1_h, r2_h, int(3 * c_w), int(4 * c_w)),
    ("gingham_check_shirt", r1_h, r2_h, int(4 * c_w), int(5 * c_w)),
    
    # Row 3 (4 cols)
    ("white_crop_top", r2_h, h, 0, int(w * 0.20)),
    ("gold_embellished_jumpsuit", r2_h, h, int(w * 0.20), int(w * 0.39)),
    ("red_satin_slip_dress", r2_h, h, int(w * 0.39), int(w * 0.63)),
    ("blue_denim_jeans", r2_h, h, int(w * 0.63), w),
]

for name, y1, y2, x1, x2 in items:
    crop = grid[y1:y2, x1:x2]
    out_p = os.path.join("inputs/dataset_garments", f"{name}.jpg")
    cv2.imwrite(out_p, crop)
    print(f"Saved {name}: {crop.shape}")

# Now update the standard 10 category garments in inputs/garments/ and assets/
mapping = {
    "jumpsuit": ("gold_embellished_jumpsuit", "assets/jumpsuit_garment.jpg", "inputs/garments/jumpsuit/jumpsuit_001.jpg"),
    "jeans": ("blue_denim_jeans", "assets/jeans_garment.jpg", "inputs/garments/jeans/jeans_001.jpg"),
    "shirt": ("gingham_check_shirt", "assets/shirt_garment.jpg", "inputs/garments/shirt/shirt_001.jpg"),
    "tshirt": ("black_polo_tshirt", "assets/t-shirt_garment.jpg", "inputs/garments/tshirt/tshirt_001.jpg"),
    "kurti": ("black_printed_kurti_set", "assets/sample_kurti_garment_1788149531548.jpg", "inputs/garments/kurti/kurti_001.jpg"),
    "saree": ("yellow_silk_saree", "assets/sample_saree_garment_1788149310214.jpg", "inputs/garments/saree/saree_001.jpg"),
    "top": ("pink_crop_skirt_set", "assets/top_garment.jpg", "inputs/garments/top/top_001.jpg"),
    "lehenga": ("emerald_green_suit", "assets/lehenga_garment.jpg", "inputs/garments/lehenga/lehenga_001.jpg"),
    "coat": ("denim_shirt_dress", "assets/coat_garment.jpg", "inputs/garments/coat/coat_001.jpg"),
    "trousers": ("red_satin_slip_dress", "assets/trousers_garment.jpg", "inputs/garments/trousers/trousers_001.jpg"),
}

for cat, (src_name, asset_dest, input_dest) in mapping.items():
    src_p = os.path.join("inputs/dataset_garments", f"{src_name}.jpg")
    crop = cv2.imread(src_p)
    cv2.imwrite(asset_dest, crop)
    cv2.imwrite(input_dest, crop)
    print(f"Mapped {cat} -> {src_name}")
