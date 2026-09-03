import re
import json
import urllib.request
import os

url = "https://drive.google.com/drive/folders/1Wt9fa2h8qdzwrmWK7LRCPC1YKfPl2Mv5?usp=sharing"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8")

# Search for filenames and file IDs in the page
print("Length of content:", len(content))

# Look for image extensions
matches = re.findall(r'([-\w]{25,})[^\w]+([\w\s\-\(\)\.]+\.(?:jpg|jpeg|png|webp))', content, re.IGNORECASE)
print(f"Found {len(matches)} potential file matches:")
for m in matches:
    print(m)

# Also search for standard Google Drive array structures
file_entries = re.findall(r'\[\"([a-zA-Z0-9_-]{25,})\",\[\"([^\"]+)\"', content)
print(f"Found {len(file_entries)} entries via array pattern:")
for f in file_entries[:20]:
    print(f)
