"""
Input Validation and Pre-Flight Quality Verification Engine.
"""

import os
import cv2
import numpy as np
from PIL import Image
from dataclasses import dataclass, field
from typing import Dict, Any, Tuple, Optional, List

@dataclass
class ValidationResult:
    is_valid: bool
    status: str
    message: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class InputValidator:
    def __init__(
        self,
        min_width: int = 100,
        min_height: int = 100,
        blur_threshold: float = 30.0,
        min_brightness: float = 20.0,
        max_brightness: float = 250.0,
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.blur_threshold = blur_threshold
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness
        self.supported_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    def validate_file(self, file_path: str, role_name: str = "Image") -> Tuple[bool, Optional[str], Optional[np.ndarray]]:
        if not file_path:
            return False, f"{role_name} path is empty.", None
        if not os.path.exists(file_path):
            return False, f"{role_name} file not found at: {file_path}", None
        
        try:
            with Image.open(file_path) as img:
                img.verify()
            cv_img = cv2.imread(file_path)
            if cv_img is None:
                return False, f"Failed to decode {role_name} as image.", None
            return True, None, cv_img
        except Exception as e:
            return False, f"Corrupted {role_name}: {str(e)}", None

    def assess_quality(self, cv_img: np.ndarray, role_name: str = "Image") -> Tuple[Dict[str, Any], List[str], List[str]]:
        errors = []
        warnings = []
        h, w = cv_img.shape[:2]
        metrics = {"width": w, "height": h}

        if w < self.min_width or h < self.min_height:
            errors.append(f"{role_name} resolution ({w}x{h}) is below minimum {self.min_width}x{self.min_height}.")

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        metrics["blur_variance"] = round(laplacian_var, 2)
        if laplacian_var < self.blur_threshold:
            errors.append(f"{role_name} is severely blurry (sharpness score {laplacian_var:.1f}).")

        mean_brightness = float(np.mean(gray))
        metrics["mean_brightness"] = round(mean_brightness, 2)
        if mean_brightness < self.min_brightness:
            errors.append(f"{role_name} is extremely dark.")

        return metrics, errors, warnings

    def validate_inputs(
        self,
        target_person_path: str,
        garment_source_path: str,
        category_id: str
    ) -> ValidationResult:
        all_errors = []
        all_warnings = []
        combined_metrics = {}

        ok_p, err_p, cv_p = self.validate_file(target_person_path, "Person Reference")
        if not ok_p:
            all_errors.append(err_p)
        else:
            m_p, e_p, w_p = self.assess_quality(cv_p, "Person Reference")
            combined_metrics["person"] = m_p
            all_errors.extend(e_p)
            all_warnings.extend(w_p)

        ok_g, err_g, cv_g = self.validate_file(garment_source_path, "Garment Reference")
        if not ok_g:
            all_errors.append(err_g)
        else:
            m_g, e_g, w_g = self.assess_quality(cv_g, "Garment Reference")
            combined_metrics["garment"] = m_g
            all_errors.extend(e_g)
            all_warnings.extend(w_g)

        if all_errors:
            return ValidationResult(
                is_valid=False,
                status="FAILED",
                message="Input validation failed: " + "; ".join(all_errors),
                metrics=combined_metrics,
                errors=all_errors,
                warnings=all_warnings
            )

        return ValidationResult(
            is_valid=True,
            status="PASSED",
            message="Pre-flight validation passed.",
            metrics=combined_metrics,
            errors=[],
            warnings=all_warnings
        )
