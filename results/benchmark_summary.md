# Vizzle Virtual Try-On Benchmark Evaluation Summary

- **Generated on:** 2026-08-31 04:28:21 (UTC)
- **Constraint 1 (Latency):** < 15.00 seconds per generated image
- **Constraint 2 (Cost):** < ₹4.00 per generated image
- **Scope:** 10 Mandatory Clothing Categories (Saree, Kurti, Lehenga, Top, T-shirt, Jumpsuit, Coat, Shirt, Jeans, Trousers)

---

## Model Comparison Matrix

| Model | Supported Categories | Avg Latency (s) | Avg Cost (INR) | Avg Quality (1-5) | Latency (<15s) | Cost (<₹4) | Final Recommendation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **IDM-VTON** | **10 / 10** | **7.92s** | **₹2.09** | **4.82 / 5.0** | ✅ PASS | ✅ PASS | 🥇 **PRIMARY PRODUCTION PICK** |
| **FASHN.ai (v1.5 API)** | **10 / 10** | **6.38s** | **₹3.76** | **4.68 / 5.0** | ✅ PASS | ✅ PASS | 🥈 **Commercial Runner-Up** |
| **OOTDiffusion** | 6 / 10 | 9.17s | ₹2.41 | 4.38 / 5.0 | ✅ PASS | ✅ PASS | ⚠️ Western Casuals Only |
| **CatVTON** | 6 / 10 | 4.47s | ₹1.38 | 4.10 / 5.0 | ✅ PASS | ✅ PASS | ⚠️ Lightweight Baseline Only |

---

## 10-Category Coverage Breakdown

| Category | IDM-VTON | FASHN.ai (v1.5) | OOTDiffusion | CatVTON |
| :--- | :---: | :---: | :---: | :---: |
| **Saree** | ✅ PASS (4.8/5) | ✅ PASS (4.5/5) | ❌ NOT SUPPORTED | ❌ NOT SUPPORTED |
| **Kurti** | ✅ PASS (4.9/5) | ✅ PASS (4.7/5) | ⚠️ PARTIAL | ⚠️ PARTIAL |
| **Lehenga** | ✅ PASS (4.8/5) | ✅ PASS (4.6/5) | ❌ NOT SUPPORTED | ❌ NOT SUPPORTED |
| **Top** | ✅ PASS (4.9/5) | ✅ PASS (4.8/5) | ✅ PASS (4.4/5) | ✅ PASS (4.1/5) |
| **T-shirt** | ✅ PASS (4.9/5) | ✅ PASS (4.8/5) | ✅ PASS (4.5/5) | ✅ PASS (4.4/5) |
| **Jumpsuit** | ✅ PASS (4.7/5) | ✅ PASS (4.6/5) | ⚠️ PARTIAL | ⚠️ PARTIAL |
| **Coat** | ✅ PASS (4.8/5) | ✅ PASS (4.7/5) | ✅ PASS (4.3/5) | ✅ PASS (3.9/5) |
| **Shirt** | ✅ PASS (4.9/5) | ✅ PASS (4.8/5) | ✅ PASS (4.4/5) | ✅ PASS (4.0/5) |
| **Jeans** | ✅ PASS (4.8/5) | ✅ PASS (4.7/5) | ✅ PASS (4.4/5) | ✅ PASS (4.2/5) |
| **Trousers** | ✅ PASS (4.8/5) | ✅ PASS (4.7/5) | ✅ PASS (4.3/5) | ✅ PASS (4.0/5) |
