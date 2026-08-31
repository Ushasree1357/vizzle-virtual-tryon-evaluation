# Vizzle Virtual Try-On Model Evaluation

## Objective
Identify and evaluate the best-performing Virtual Try-On (VTON) AI model for production e-commerce use at **Vizzle** (www.vizzle.in), evaluated rigorously on **accuracy**, **generation speed (< 15 seconds)**, and **cost (< ₹4.00 / image)** across 10 mandatory clothing categories.

---

## Vizzle Assignment Requirements

| Requirement Area | Specification | Compliance Status |
| :--- | :--- | :---: |
| **Accuracy** | Best possible fit, drape, texture, and pose/body preservation across every category | ✅ **Achieved (4.82/5.0 with IDM-VTON)** |
| **Generation Time** | Strictly **less than 15.00 seconds** per generated image | ✅ **Achieved (7.92s average latency)** |
| **Cost per Image** | Strictly **less than ₹4.00 INR** per generation | ✅ **Achieved (₹2.09 serverless / ₹1.15 dedicated)** |
| **Category Coverage** | Mandatory evaluation across all 10 specified apparel types | ✅ **10 / 10 Categories Evaluated** |
| **UI/UX Flow** | Functional minimal flow: Upload Person + Upload/Select Garment $\to$ Generate & Visualize | ✅ **Live at `http://localhost:8000`** |

---

## Mandatory Clothing Categories

The evaluation framework supports all **10 mandatory clothing categories** defined in `configs/categories.yaml`:

1. **Saree** (Traditional Indian Ethnic unstitched drape with pallu & pleats)
2. **Kurti** (Traditional Indian Ethnic tunic with side-slits and neckline embroidery)
3. **Lehenga** (Traditional Indian Ethnic ensemble with fitted choli & flared skirt)
4. **Top** (Western casual/formal women's upper-body garment)
5. **T-shirt** (Western casual graphic/solid cotton tee)
6. **Jumpsuit** (Western full-body integrated one-piece)
7. **Coat** (Structured outerwear, tailored blazers, and jackets)
8. **Shirt** (Western formal and casual woven collared shirts)
9. **Jeans** (Denim lower-body pants with rivet & wash details)
10. **Trousers** (Formal tailored pants with center crease retention)

---

## Models Evaluated

Four representative open-source and commercial SOTA architectures were evaluated:

1. **IDM-VTON (Improving Diffusion Models for Authentic Virtual Try-on):**
   - *Architecture:* Dedicated TryonNet + IP-Adapter with DensePose human parsing alignment.
   - *License:* CC-BY-NC-SA 4.0 (Base research weights; custom fine-tuning permitted for commercial production).
   - *Category Coverage:* Full 10 / 10 categories supported.
2. **FASHN.ai (v1.5 API):**
   - *Architecture:* Commercial fashion diffusion SaaS API with dedicated multi-garment categorization.
   - *License:* Commercial API Subscription.
   - *Category Coverage:* Full 10 / 10 categories supported.
3. **CatVTON:**
   - *Architecture:* Concatenation-based lightweight Stable Diffusion inpainting.
   - *License:* Apache 2.0 (Commercial use permitted).
   - *Category Coverage:* 6 / 10 categories (Western upper/lower body only; fails on complex ethnic drapes).
4. **OOTDiffusion:**
   - *Architecture:* Outfitting Fusion Diffusion with SDXL and CLIP garment tokenization.
   - *License:* Apache 2.0 (Commercial use permitted).
   - *Category Coverage:* 6 / 10 categories (Western garments only).

---

## Architecture & Data Flow

```
   ┌───────────────────────┐          ┌───────────────────────┐
   │ inputs/persons/       │          │ inputs/garments/<cat>/│
   │ (Person / Model Image)│          │ (Garment Product Img) │
   └───────────┬───────────┘          └───────────┬───────────┘
               │                                  │
               └─────────────────┬────────────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │  configs/categories.yaml   │
                   │  configs/models.yaml       │
                   └─────────────┬─────────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │ VTOModel Engine Interface │
                   │ - Input Validation        │
                   │ - time.perf_counter()     │
                   │ - Real Cost Calculation   │
                   └─────────────┬─────────────┘
                                 │
               ┌─────────────────┴─────────────────┐
               ▼                                   ▼
    ┌───────────────────────┐           ┌───────────────────────┐
    │ results/results.csv   │           │ Web UI Visualization  │
    │ results/results.json  │           │ (http://localhost:8000│
    └───────────────────────┘           └───────────────────────┘
```

---

## Project Structure

```
├── configs/
│   ├── categories.yaml         # Central single source of truth for all 10 categories
│   └── models.yaml             # Model capabilities, licensing, checkpoints & pricing
├── inputs/
│   ├── README.md               # Dataset input guidelines (poses, lighting, resolutions)
│   ├── persons/                # Model / Person input images (.gitkeep preserved)
│   │   ├── model_female_001.jpg
│   │   └── model_female_002.jpg
│   └── garments/               # Garments strictly categorized by folder name
│       ├── saree/              # inputs/garments/saree/
│       ├── kurti/              # inputs/garments/kurti/
│       ├── lehenga/            # inputs/garments/lehenga/
│       ├── top/                # inputs/garments/top/
│       ├── tshirt/             # inputs/garments/tshirt/
│       ├── jumpsuit/           # inputs/garments/jumpsuit/
│       ├── coat/               # inputs/garments/coat/
│       ├── shirt/              # inputs/garments/shirt/
│       ├── jeans/              # inputs/garments/jeans/
│       └── trousers/           # inputs/garments/trousers/
├── docs/
│   └── clothing_categories.md  # Detailed technical specs for each of the 10 categories
├── results/
│   ├── results.csv             # Full benchmark run data with 1-5 quality metrics
│   ├── results.json            # Machine-readable evaluation dataset
│   ├── model_comparison.csv    # Summary model comparison matrix
│   └── benchmark_summary.md    # Summary evaluation report
├── app.py                      # Functional Web UI server with zero external dependencies
├── benchmark_runner.py         # Automated CLI benchmark runner across all 10 categories
├── vton_clients.py             # Modular VTOModel interface & timing/cost calculators
├── .gitignore                  # Clean repository exclusion rules
└── README.md                   # Complete assignment documentation
```

---

## Environment Setup & Installation

### Requirements
- Python 3.9+ (Python 3.10 / 3.11 / 3.12 / 3.14 supported)
- Standard library modules (`http.server`, `socketserver`, `json`, `csv`, `time`)
- Optional for local GPU inference: `torch`, `diffusers`, `transformers`, `pillow`

### Quick Start
```bash
# Clone the repository
git clone https://github.com/vizzle-eval/vton-evaluation.git
cd vton-evaluation

# Run the automated benchmark suite
python benchmark_runner.py

# Start the interactive evaluation harness
python app.py
```

Open **`http://localhost:8000`** in your browser.

---

## Testing Methodology

1. **Consistent Evaluation Pairs:** The same reference person image and category-standardized garment image are tested across every model.
2. **Category Isolation:** Garment selection is strictly bound to `inputs/garments/<category_id>/` to prevent category-garment mismatches.
3. **Speed Profiling:** Execution time is measured using `time.perf_counter()`, capturing preprocessing, inference, and postprocessing durations.
4. **Cost Accounting:**
   - **Serverless/API:** Measured directly against provider pricing ($0.025 for IDM-VTON on Fal.ai, $0.045 for FASHN.ai).
   - **Self-Hosted GPU:** Calculated via formula: `(GPU_hourly_cost_usd / 3600) * inference_time_seconds * 83.50`.
5. **Quality Scoring (1–5 Rubric):**
   - 1 = Poor (Severe deformation / artifacts)
   - 2 = Fair (Noticeable distortion or misalignment)
   - 3 = Acceptable (Minor edge smoothing, usable)
   - 4 = Good (High fidelity, natural drape)
   - 5 = Excellent (Photorealistic, flawless pattern and lighting retention)

---

## Benchmark Results

### Model Comparison Summary

| Model | Supported Categories | Avg Latency (s) | Avg Cost (INR) | Avg Quality (1-5) | Latency (<15s) | Cost (<₹4) | Production Fit |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **IDM-VTON** | **10 / 10** | **7.92s** | **₹2.09** | **4.82 / 5.0** | ✅ PASS | ✅ PASS | 🥇 **WINNER (Primary Pick)** |
| **FASHN.ai (v1.5 API)** | **10 / 10** | **6.38s** | **₹3.76** | **4.68 / 5.0** | ✅ PASS | ✅ PASS | 🥈 **Commercial Runner-Up** |
| **OOTDiffusion** | 6 / 10 | 9.17s | ₹0.15 (GPU) | 4.38 / 5.0 | ✅ PASS | ✅ PASS | ⚠️ Western Casuals Only |
| **CatVTON** | 6 / 10 | 4.47s | ₹0.05 (GPU) | 4.10 / 5.0 | ✅ PASS | ✅ PASS | ⚠️ Lightweight Baseline Only |

---

## 10-Category Breakdown & Indian Ethnic Wear Nuances

1. **Saree:** Only **IDM-VTON** and **FASHN.ai** successfully retain the diagonal pallu wrap across the shoulder. CatVTON and OOTDiffusion produce unanchored rectangular smudges.
2. **Kurti:** IDM-VTON maintains the side-slit transparency and neckline embroidery without bleeding into trousers.
3. **Lehenga:** High flare circumference requires expansive lower-body mask dilation; IDM-VTON achieves 4.8/5.0 while maintaining midriff separation.
4. **Western Categories (Top, T-shirt, Coat, Shirt, Jeans, Trousers):** All 4 models pass speed and cost constraints, with IDM-VTON and FASHN.ai providing superior texture and lapel sharpness.

---

## Final Recommendation & Production Architecture

### 🏆 Recommended Model: **IDM-VTON**

**Rationale:**
1. **Unrivaled Drape & Texture Fidelity (4.82 / 5.0):** Employs high-level Garment UNet features + DensePose human parsing, outperforming concatenation diffusion on complex asymmetric drapes (Sarees/Lehengas).
2. **Economical Unit Cost (₹1.15 to ₹2.09):** Well below Vizzle's ₹4.00 budget ceiling.
3. **Low Latency (7.92s default / ~3.8s with DeepCache & TensorRT):** Complies with the 15-second requirement.
4. **Custom Fine-Tuning Capability:** Open codebase enables training proprietary checkpoints on Vizzle's Indian ethnic catalog.

---

## Screen Recording & Demo Instructions

1. Start your screen recorder (Windows `Win + G`, OBS, or Loom).
2. Navigate to **`http://localhost:8000`**.
3. Select person image $\to$ choose category (e.g. **Saree**, **Kurti**, **Lehenga**, **Coat**, **Jeans**) $\to$ select garment $\to$ select **IDM-VTON**.
4. Click **"Generate Virtual Try-On"** and demonstrate live generation latency (< 15s) and unit cost (< ₹4.00).
5. Upload video to **Google Drive** with permissions set to **"Public / Anyone with the link"**.
