import re
import urllib.request
import os

with open(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\.system_generated\steps\519\content.md", encoding="utf-8") as f:
    text = f.read()

# Match patterns where ID and filename appear together in the JS data
entries = re.findall(r'\[\"([a-zA-Z0-9_-]{25,})\",\[\"(Screenshot[^\"]+\.png)\"', text)
print(f"Found {len(entries)} file matches:")
file_dict = {}
for file_id, name in entries:
    file_dict[name] = file_id
    print(f"  {name} -> {file_id}")

os.makedirs("inputs/test_dataset", exist_ok=True)

# Download each file
for name, file_id in file_dict.items():
    dest = os.path.join("inputs/test_dataset", name.replace(" ", "_"))
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"Downloading {name} from {download_url}...")
    try:
        urllib.request.urlretrieve(download_url, dest)
        print(f"  Saved to {dest}, size: {os.path.getsize(dest)} bytes")
    except Exception as e:
        print(f"  Failed: {e}")
