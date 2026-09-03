import os
import glob
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

USER_IMG = "inputs/persons/model_female_001.jpg"
EVAL_DIR = "results/drive_evaluation"
TEST_DATASET_DIR = "inputs/test_dataset"

def make_montage():
    test_files = sorted(glob.glob(os.path.join(TEST_DATASET_DIR, "*.png")))
    card_w, card_h = 240, 360
    padding = 20
    header_h = 60
    
    rows = len(test_files)
    total_w = card_w * 3 + padding * 4
    total_h = header_h + (card_h + padding) * rows + padding

    canvas = np.ones((total_h, total_w, 3), dtype=np.uint8) * 15 # Dark background #0f0f0f

    p1_cv = cv2.imread(USER_IMG)
    p1_resized = cv2.resize(p1_cv, (card_w, card_h), interpolation=cv2.INTER_AREA)

    for idx, g_path in enumerate(test_files):
        fname = os.path.basename(g_path)
        g_cv = cv2.imread(g_path)
        g_resized = cv2.resize(g_cv, (card_w, card_h), interpolation=cv2.INTER_AREA)

        # Output image
        out_path = glob.glob(os.path.join(EVAL_DIR, f"eval_{idx+1:02d}_*"))
        if out_path:
            res_cv = cv2.imread(out_path[0])
            res_resized = cv2.resize(res_cv, (card_w, card_h), interpolation=cv2.INTER_AREA)
        else:
            res_resized = p1_resized

        y_offset = header_h + idx * (card_h + padding)

        # Draw Person (Col 1)
        x1 = padding
        canvas[y_offset:y_offset+card_h, x1:x1+card_w] = p1_resized

        # Draw Garment (Col 2)
        x2 = x1 + card_w + padding
        canvas[y_offset:y_offset+card_h, x2:x2+card_w] = g_resized

        # Draw Result (Col 3)
        x3 = x2 + card_w + padding
        canvas[y_offset:y_offset+card_h, x3:x3+card_w] = res_resized

    pil_canvas = Image.fromarray(canvas)
    draw = ImageDraw.Draw(pil_canvas)

    # Header labels
    draw.text((padding + 30, 20), "1. Saree User Image (Model)", fill=(255, 255, 255))
    draw.text((padding + card_w + padding + 30, 20), "2. Test Garment (Drive Pack)", fill=(255, 255, 255))
    draw.text((padding + (card_w + padding)*2 + 30, 20), "3. VTO Try-On Evaluation Result", fill=(129, 140, 248))

    montage_path = os.path.join(EVAL_DIR, "vto_evaluation_montage.jpg")
    pil_canvas.save(montage_path, quality=95)
    print(f"[+] Montage saved at {montage_path} ({total_w}x{total_h})")

if __name__ == "__main__":
    make_montage()
