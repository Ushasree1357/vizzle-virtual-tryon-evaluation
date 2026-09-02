"""
Vizzle Garment Extraction and Preprocessing Engine
Extracts clothing garments from Image 2, removing background and non-clothing parts.
"""

import os
import time
import logging
import cv2
import numpy as np
from PIL import Image
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import rembg

logger = logging.getLogger("GarmentExtractor")

@dataclass
class ExtractedGarment:
    success: bool
    category_id: str
    garment_rgba_path: str
    garment_rgb_path: str
    mask_path: str
    debug_composite_path: str
    bounding_box: Tuple[int, int, int, int]
    preprocessing_time_seconds: float
    message: str
    metadata: Dict[str, Any]

class GarmentExtractor:
    def __init__(self, output_dir: str = "results/preprocessed"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        try:
            self._rembg_session = rembg.new_session("u2netp")
        except Exception:
            self._rembg_session = None

    def extract(
        self,
        source_image_path: str,
        category_id: str,
    ) -> ExtractedGarment:
        t_start = time.perf_counter()
        cat = category_id.lower().replace("-", "").replace("_", "")
        base_name = os.path.splitext(os.path.basename(source_image_path))[0]
        
        pil_img = Image.open(source_image_path).convert("RGB")
        w, h = pil_img.size
        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # 1. Background segmentation via rembg
        if self._rembg_session is not None:
            rgba_foreground = rembg.remove(pil_img, session=self._rembg_session)
        else:
            rgba_foreground = rembg.remove(pil_img)
            
        foreground_np = np.array(rgba_foreground)
        alpha = foreground_np[:, :, 3].copy()

        # 2. Isolate garment from face/hair/shorts based on category
        if cat in {"shirt", "top", "tshirt", "coat"}:
            # Suppress head above neckline (top 26%)
            alpha[:int(h * 0.26), :] = 0
            # Suppress shorts/pants below shirt hemline (bottom 30%)
            alpha[int(h * 0.72):, :] = 0
        elif cat in {"jeans", "trousers"}:
            alpha[:int(h * 0.44), :] = 0
            alpha[int(h * 0.95):, :] = 0
        elif cat == "kurti":
            alpha[:int(h * 0.22), :] = 0
            alpha[int(h * 0.76):, :] = 0
        elif cat in {"saree", "lehenga", "jumpsuit"}:
            alpha[:int(h * 0.20), :] = 0
            alpha[int(h * 0.96):, :] = 0

        # Morphological clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel)
        _, binary_mask = cv2.threshold(alpha, 50, 255, cv2.THRESH_BINARY)

        # Crop to garment bounding box
        y_idx, x_idx = np.where(binary_mask > 0)
        if len(y_idx) > 0 and len(x_idx) > 0:
            ymin, ymax = int(np.min(y_idx)), int(np.max(y_idx))
            xmin, xmax = int(np.min(x_idx)), int(np.max(x_idx))
            bbox = (xmin, ymin, xmax - xmin, ymax - ymin)
        else:
            bbox = (0, 0, w, h)

        # Save extracted RGBA
        extracted_rgba = np.zeros((h, w, 4), dtype=np.uint8)
        extracted_rgba[:, :, :3] = np.array(pil_img)
        extracted_rgba[:, :, 3] = binary_mask

        # Clean RGB
        neutral_bg = np.ones((h, w, 3), dtype=np.uint8) * 248
        alpha_f = (binary_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
        garment_rgb = (np.array(pil_img).astype(np.float32) * alpha_f + neutral_bg * (1.0 - alpha_f)).astype(np.uint8)

        # Save artifacts
        prefix = f"{cat}_{base_name}"
        rgba_path = os.path.join(self.output_dir, f"{prefix}_extracted_rgba.png")
        rgb_path = os.path.join(self.output_dir, f"{prefix}_extracted_rgb.jpg")
        mask_path = os.path.join(self.output_dir, f"{prefix}_garment_mask.png")
        debug_path = os.path.join(self.output_dir, f"{prefix}_debug_pipeline.jpg")

        Image.fromarray(extracted_rgba).save(rgba_path)
        Image.fromarray(garment_rgb).save(rgb_path, quality=95)
        Image.fromarray(binary_mask).save(mask_path)
        Image.fromarray(garment_rgb).save(debug_path, quality=92)

        t_duration = round(time.perf_counter() - t_start, 4)

        return ExtractedGarment(
            success=True,
            category_id=category_id,
            garment_rgba_path=rgba_path,
            garment_rgb_path=rgb_path,
            mask_path=mask_path,
            debug_composite_path=debug_path,
            bounding_box=bbox,
            preprocessing_time_seconds=t_duration,
            message=f"Extracted {category_id} garment in {t_duration}s",
            metadata={"category": category_id, "bbox": bbox}
        )
