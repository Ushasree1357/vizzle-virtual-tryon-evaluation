import re

with open("scratch/fetch_drive_folder.py") as f:
    pass

with open(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\.system_generated\steps\519\content.md", encoding="utf-8") as f:
    text = f.read()

# Search for mentions of .jpg, .png, .jpeg
for ext in [r'\.jpg', r'\.png', r'\.jpeg', r'\.webp']:
    m = re.findall(rf'[\w\-\s\.]+{ext}', text, re.IGNORECASE)
    print(f"Matches for {ext}:", set(m))

# Look for drive file IDs (strings of 28-44 alphanumeric chars starting with 1)
ids = re.findall(r'1[a-zA-Z0-9_-]{28,35}', text)
print("Unique IDs found:", set(ids))
