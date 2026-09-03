import cv2
import numpy as np

orig = cv2.imread("inputs/persons/model_female_001.jpg")
h1, w1 = orig.shape[:2]

# Measure head position in orig:
# Hair starts near top:
gray1 = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
# In orig, the model's hair bun starts around y = 20 (which is 2.8% of height)
# In generated, the model's hair bun starts around y = 140 (which is 11.0% of height)
# So the generated model has ~8% extra empty headroom and is scaled down / zoomed out!
print(f"Orig height: {h1}, width: {w1}")
