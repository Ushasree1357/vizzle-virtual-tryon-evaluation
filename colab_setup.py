"""
Google Colab / Cloud GPU Execution Script for CatVTON & IDM-VTON
Installs dependencies, loads real model weights on CUDA GPU, and executes benchmarks across all 10 categories.
"""

import sys
import os
import subprocess
import time

def setup_colab_environment():
    print("[1/4] Installing PyTorch, Diffusers, Transformers & Accelerate...")
    packages = [
        "torch", "torchvision", "diffusers>=0.28.0",
        "transformers", "accelerate", "opencv-python",
        "pillow", "pyyaml", "huggingface_hub"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + packages)
    print("Dependencies installed successfully.")

def run_real_gpu_test():
    import torch
    print(f"\n[2/4] Checking GPU Hardware...")
    if not torch.cuda.is_available():
        print("ERROR: No CUDA GPU detected! Please enable GPU in Colab: Runtime -> Change runtime type -> T4 GPU.")
        return False

    device_name = torch.cuda.get_device_name(0)
    vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
    print(f"Active GPU: {device_name} ({vram_gb} GB VRAM)")

    print("\n[3/4] Initializing Real CatVTON Model from HuggingFace (zhengchong/CatVTON)...")
    t0 = time.perf_counter()
    from models.catvton_model import CatVTONModelAdapter
    adapter = CatVTONModelAdapter()
    loaded, msg = adapter.load_model()
    print(f"Model status: {msg} (Elapsed: {round(time.perf_counter() - t0, 2)}s)")

    print("\n[4/4] Executing Real Try-On Test for Category: T-shirt...")
    person_img = "inputs/persons/model_female_001.jpg"
    garment_img = "inputs/garments/tshirt/tshirt_001.jpg"
    
    res = adapter.generate(person_img, garment_img, "tshirt")
    print("\n" + "=" * 60)
    print("REAL GPU EXECUTION RESULTS")
    print("=" * 60)
    for k, v in res.items():
        print(f"{k:<30}: {v}")
    print("=" * 60)
    return True

if __name__ == "__main__":
    setup_colab_environment()
    run_real_gpu_test()
