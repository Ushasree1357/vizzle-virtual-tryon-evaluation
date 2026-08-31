# Technical Specification: 10 Mandatory Clothing Categories

This document defines the technical characteristics, body regions, preprocessing strategies, input requirements, evaluation considerations, and known Virtual Try-On (VTO) challenges for all **10 mandatory clothing categories** in the Vizzle evaluation framework.

---

## 1. Saree

- **Category ID:** `saree`
- **Clothing Type:** Traditional Indian Ethnic
- **Body Region:** Full Body (Torso to Ankle + Shoulder Pallu Drape)
- **Expected Garment Image Format:**
  - High-resolution (minimum 768×1024) flat-lay or ghost mannequin image showing the full folded drape, distinct border (zari), body fabric pattern, and pallu section.
- **Expected Person Image:**
  - Front-facing full-body standing pose with arms slightly away from the torso and feet visible.
- **Evaluation Considerations:**
  - **Pallu Preservation:** Must accurately anchor over the left shoulder and drape diagonally across the chest without warping.
  - **Pleat Retention:** Vertical pleats along the waistline and center fall must remain crisp and natural.
  - **Blouse Separation:** Clean boundary between the fitted blouse neckline/sleeves and the saree drape.
- **Known VTO Challenges:**
  - Standard Western diffusion models (trained purely on VITON-HD or DressCode) fail completely because an unstitched 6-yard saree is an asymmetrical 3D wrap that cannot be modeled as a simple 2D bounded polygon.
  - Requires dense pose guidance (DensePose) to align the diagonal torso wrap correctly.

---

## 2. Kurti

- **Category ID:** `kurti`
- **Clothing Type:** Traditional Indian Ethnic Top / Tunic
- **Body Region:** Upper Body to Mid-Thigh / Calf
- **Expected Garment Image Format:**
  - Frontal ghost mannequin image showing neckline embroidery (yoke), full length, and side-slit cuts.
- **Expected Person Image:**
  - Full-body or 3/4th-body standing pose.
- **Evaluation Considerations:**
  - **Side-Slits:** The open slits at the waist/hips must show natural leg or bottom-wear separation rather than filling the gap with solid cloth artifacts.
  - **Neckline Embroidery:** Detailed zari/thread-work at the collar and yoke must remain razor-sharp.
  - **Hem Drape:** Natural flow over trousers or leggings.
- **Known VTO Challenges:**
  - Traditional upper-body masks terminate at the hips; applying a calf-length kurti causes mask truncation or smearing unless dynamic extended parsing is utilized.

---

## 3. Lehenga

- **Category ID:** `lehenga`
- **Clothing Type:** Traditional Indian Ethnic Set
- **Body Region:** Full Body (Cropped Torso + Flared Lower Body)
- **Expected Garment Image Format:**
  - Clean studio product photo of the lehenga skirt and choli (or high-resolution set layout on clean white background).
- **Expected Person Image:**
  - Upright full-body standing pose with clear midriff exposure.
- **Evaluation Considerations:**
  - **Skirt Flare Volume:** Preserving the wide circular sweep and heavy hemline without collapsing into a narrow tube.
  - **Midriff Definition:** Accurate gap separation between the bottom of the choli and the waistband of the lehenga skirt.
  - **Heavy Embroidery / Zari:** Preserving high-frequency golden sequin, mirror, and thread textures.
- **Known VTO Challenges:**
  - Skirt flare exceeds standard human body boundaries; requires generous dilation of the lower-body inpainting mask while preserving background integrity.

---

## 4. Top

- **Category ID:** `top`
- **Clothing Type:** Western Casual / Formal Top
- **Body Region:** Upper Body (Shoulders to Waist)
- **Expected Garment Image Format:**
  - Ghost mannequin or flat-lay on plain background showing neckline and sleeves.
- **Expected Person Image:**
  - Upper-body or full-body pose.
- **Evaluation Considerations:**
  - **Neckline Contour:** Adherence to specific neck designs (cowl, halter, sweetheart, square neck).
  - **Torso Fit:** Snug wrap conforming to the model's natural waistline.
  - **Fabric Sheen:** Preserving satin, silk, or chiffon specular highlights.
- **Known VTO Challenges:**
  - Asymmetric or off-shoulder cuts can cause artifact bleeding onto bare shoulder skin.

---

## 5. T-shirt

- **Category ID:** `tshirt`
- **Clothing Type:** Western Casual
- **Body Region:** Upper Body (Shoulders to Hips)
- **Expected Garment Image Format:**
  - Frontal flat-lay showing collar ribbing and central graphics/typography.
- **Expected Person Image:**
  - Front-facing standing pose.
- **Evaluation Considerations:**
  - **Graphic Integrity:** Zero geometric warping or character degradation on chest prints.
  - **Sleeve Drape:** Natural sleeve angle conforming to arm pose.
  - **Fabric Folds:** Realistic subtle cotton folds over chest and torso.
- **Known VTO Challenges:**
  - Over-smoothing in diffusion denoising can blur fine printed text or graphic micro-details.

---

## 6. Jumpsuit

- **Category ID:** `jumpsuit`
- **Clothing Type:** Western Full-Body
- **Body Region:** Full Body (Shoulders to Ankles)
- **Expected Garment Image Format:**
  - Full-length product photo showing bodice, waist cinch/belt, and trouser legs.
- **Expected Person Image:**
  - Full-body standing pose with feet visible.
- **Evaluation Considerations:**
  - **Vertical Continuity:** Seamless fabric connection across the waist without artificial seam breaks.
  - **Proportional Balance:** Accurate torso-to-leg length proportions.
  - **Leg Silhouette:** Preservation of wide-leg or tapered trouser styling.
- **Known VTO Challenges:**
  - Disconnect between upper-body parsing and lower-body parsing models if separate passes are attempted. Requires single-pass full-body inpainting.

---

## 7. Coat

- **Category ID:** `coat`
- **Clothing Type:** Structured Outerwear / Blazer
- **Body Region:** Upper Body (Shoulders to Mid-Thigh)
- **Expected Garment Image Format:**
  - Structured ghost mannequin image displaying lapels, padded shoulders, and buttons.
- **Expected Person Image:**
  - Upper-body or full-body pose with arms relaxed at sides.
- **Evaluation Considerations:**
  - **Lapel Crispness:** Sharp, un-smudged collar and lapel edges.
  - **Shoulder Structure:** Realistic padded shoulder silhouette adhering to the model's shoulder line.
  - **Layering:** Natural exposure of the inner shirt/top in the chest V-opening.
- **Known VTO Challenges:**
  - Outerwear must layer *over* existing clothes rather than skin-tight replacement, demanding precise boundary dilation.

---

## 8. Shirt

- **Category ID:** `shirt`
- **Clothing Type:** Western Formal / Casual Woven Shirt
- **Body Region:** Upper Body
- **Expected Garment Image Format:**
  - Buttoned frontal view showing structured collar, placket, and cuffs.
- **Expected Person Image:**
  - Upper-body or full-body pose.
- **Evaluation Considerations:**
  - **Collar Rigidity:** Preserving sharp collar points and stand.
  - **Placket Alignment:** Vertical straight alignment of buttons and front seams.
  - **Pattern Matching:** Seamless continuity of stripes/checks across shoulder and chest panels.
- **Known VTO Challenges:**
  - Pattern distortion around armpits and collar fold seams during latent warping.

---

## 9. Jeans

- **Category ID:** `jeans`
- **Clothing Type:** Denim Bottom Wear
- **Body Region:** Lower Body (Waist to Ankles)
- **Expected Garment Image Format:**
  - Front-facing flat-lay showing waistband, fly, pockets, and leg cut.
- **Expected Person Image:**
  - Full-body or lower-body pose with clear waistline visibility.
- **Evaluation Considerations:**
  - **Waistband Alignment:** Natural seating at the hip/waist without clipping into upper-body shirts.
  - **Denim Wash & Stitching:** Retention of whiskers, fading gradients, and contrast topstitching.
  - **Leg Fit:** Accurate replication of skinny, straight, or relaxed silhouettes.
- **Known VTO Challenges:**
  - Resolving shoe/footwear boundaries cleanly at the ankle hem.

---

## 10. Trousers

- **Category ID:** `trousers`
- **Clothing Type:** Formal / Tailored Bottom Wear
- **Body Region:** Lower Body (Waist to Ankles)
- **Expected Garment Image Format:**
  - Frontal flat-lay showing waistband, pleats, and pressed leg creases.
- **Expected Person Image:**
  - Full-body standing pose.
- **Evaluation Considerations:**
  - **Crease Retention:** Sharp, straight center-pressed crease line down each leg.
  - **Fabric Fluidity:** Natural tailored drape of wool, linen, or polyester-blend textiles.
  - **Hem Break:** Clean drape over footwear without bunched artifacts.
- **Known VTO Challenges:**
  - Diffusion models often smooth out delicate vertical crease lines, turning formal trousers into casual leggings.
