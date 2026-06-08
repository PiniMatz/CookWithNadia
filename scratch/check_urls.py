import json
import urllib.request
import urllib.error

with open('src/data/recipes.json', encoding='utf-8') as f:
    recipes = json.load(f)

urls = set()
for r in recipes:
    img = r['image']
    if img.startswith('http'):
        urls.add(img)

print(f"Checking {len(urls)} external URLs...")
broken = []
for url in sorted(urls):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            status = res.getcode()
            if status != 200:
                broken.append((url, f"Status {status}"))
    except urllib.error.HTTPError as e:
        broken.append((url, f"HTTP Error {e.code}"))
    except Exception as e:
        broken.append((url, f"Error: {str(e)}"))

with open('scratch/broken_urls.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(f"Found {len(broken)} broken URLs out of {len(urls)}:\n")
    for url, err in broken:
        f_out.write(f"{url} -> {err}\n")
print(f"Finished. Found {len(broken)} broken URLs.")
