import cv2

orig = cv2.imread("inputs/persons/model_female_001.jpg")
gen = cv2.imread(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\white_kurta_no_dupatta_flawless_1788439177260.jpg")

print("Original Image 1 shape:", orig.shape)
print("Generated shape:", gen.shape)
