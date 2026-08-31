"""
Base Abstract Class for all Virtual Try-On Model Adapters
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional

class BaseVTOModel(ABC):
    def __init__(self, model_id: str, display_name: str, config: Optional[Dict[str, Any]] = None):
        self.model_id = model_id
        self.display_name = display_name
        self.config = config or {}
        self.is_loaded = False
        self.device = "cpu"

    @abstractmethod
    def load_model(self) -> Tuple[bool, str]:
        """
        Load actual model weights and dependencies.
        Returns (success: bool, message: str).
        """
        pass

    @abstractmethod
    def validate_inputs(self, person_image_path: str, garment_image_path: str, category_id: str) -> Tuple[bool, str]:
        """Validate input paths, files, and category compatibility."""
        pass

    @abstractmethod
    def generate(self, person_image_path: str, garment_image_path: str, category_id: str, **kwargs) -> Dict[str, Any]:
        """
        Perform real inference.
        Returns timing, cost, output path, and status.
        Raises RuntimeError on failure.
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Return model metadata, license, checkpoint details, and device."""
        pass
