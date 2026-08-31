# Input Dataset Structure & Guidelines for Virtual Try-On Evaluation

This directory contains the input person (model) images and category-specific garment images used for evaluating Virtual Try-On models across all 10 mandatory categories.

---

## Directory Organization

```
inputs/
├── persons/                     # Person / Model images (full-body / upper-body)
│   ├── model_female_001.jpg
│   └── model_female_002.jpg
└── garments/                    # Garment images categorized strictly by folder
    ├── saree/                   # Indian Ethnic Saree garments
    │   └── saree_001.jpg
    ├── kurti/                   # Indian Ethnic Kurti garments
    │   └── kurti_001.jpg
    ├── lehenga/                 # Indian Ethnic Lehenga sets
    │   └── lehenga_001.jpg
    ├── top/                     # Western tops / blouses
    │   └── top_001.jpg
    ├── tshirt/                  # Western casual T-shirts
    │   └── tshirt_001.jpg
    ├── jumpsuit/                # Western full-body jumpsuits
    │   └── jumpsuit_001.jpg
    ├── coat/                    # Structured coats & blazers
    │   └── coat_001.jpg
    ├── shirt/                   # Formal & casual woven shirts
    │   └── shirt_001.jpg
    ├── jeans/                   # Denim bottom-wear
    │   └── jeans_001.jpg
    └── trousers/                # Tailored formal trousers
        └── trousers_001.jpg
```

---

## Person / Model Image Requirements

To ensure fair and rigorous benchmarking across models:
1. **Pose:** Standing upright, front-facing pose with arms relaxed slightly away from the torso and legs clearly visible.
2. **Attire:** Neutral, fitted base layer (e.g., solid sleeveless top and fitted leggings/tights) with minimal occlusion.
3. **Background:** Clean, solid studio background (white or neutral grey) without busy background clutter.
4. **Resolution:** Recommended minimum resolution of **768 × 1024** (3:4 aspect ratio) or **1024 × 1024**.
5. **Lighting:** Uniform studio lighting with balanced key and fill lights, avoiding harsh directional shadows across the face or torso.

---

## Garment Image Requirements

1. **Presentation:** Ghost mannequin or clean flat-lay photography.
2. **Background:** Solid white/neutral background or background-separated PNG with transparency.
3. **Completeness:**
   - Full garment silhouette must be visible within the frame without cutoffs at edges.
   - For **Saree**, show the full folded drape, pallu texture, and border embroidery.
   - For **Lehenga**, include both the choli top and flared skirt.
   - For **Jumpsuit**, ensure full neckline-to-hem length is present.
4. **Resolution:** Minimum **768 × 1024** px in JPG/PNG format.
