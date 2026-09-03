import re
import urllib.request
import os

with open(r"C:\Users\indra\.gemini\antigravity-ide\brain\cd2b60ca-e51e-4f7d-9fe5-d16f2bae4c0b\.system_generated\steps\519\content.md", encoding="utf-8") as f:
    text = f.read()

# Pattern: \x22(FILE_ID)\x22,\x5b\x221Wt9fa2h8qdzwrmWK7LRCPC1YKfPl2Mv5\x22\x5d,\x22(Screenshot[^\\]+\.png)\x22
pattern = r'\\x22([a-zA-Z0-9_-]{25,})\\x22,\\x5b\\x221Wt9fa2h8qdzwrmWK7LRCPC1YKfPl2Mv5\\x22\\x5d,\\x22(Screenshot[^\\]+\.png)\\x22'
matches = re.findall(pattern, text)

print(f"Found {len(matches)} files in folder:")
file_map = {}
for file_id, name in matches:
    file_map[name] = file_id
    print(f"  {name} -> {file_id}")

os.makedirs("inputs/test_dataset", exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
for name, file_id in file_map.items():
    clean_name = name.replace(" ", "_")
    dest = os.path.join("inputs/test_dataset", clean_name)
    # Direct download link
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0"
    print(f"Downloading {clean_name} ({file_id})...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
            out_file.write(response.read())
        print(f"  Success: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"  Download error with direct link, trying uc export: {e}")
        try:
            url2 = f"https://drive.google.com/uc?id={file_id}&export=download"
            req2 = urllib.request.Request(url2, headers=headers)
            with urllib.request.urlopen(req2) as response, open(dest, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  Success via uc: {dest} ({os.path.getsize(dest)} bytes)")
        except Exception as e2:
            print(f"  Failed: {e2}")
