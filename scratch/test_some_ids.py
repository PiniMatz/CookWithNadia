import urllib.request
import urllib.error

candidates = {
    "veggie_burger_1": "https://images.unsplash.com/photo-1525059696034-4967a8e1dca2?w=600&auto=format&fit=crop&q=80",
    "veggie_burger_2": "https://images.unsplash.com/photo-1584536286788-78a8e8e8116f?w=600&auto=format&fit=crop&q=80",
    "chia_pudding_1": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=600&auto=format&fit=crop&q=80",
    "chia_pudding_2": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&auto=format&fit=crop&q=80",
    "wrap_1": "https://images.unsplash.com/photo-1626700051175-6518c4793fde?w=600&auto=format&fit=crop&q=80",
}

print("Verifying candidate image URLs...")
for name, url in candidates.items():
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            print(f"{name}: SUCCESS (200)")
    except urllib.error.HTTPError as e:
        print(f"{name}: FAILED (HTTP {e.code})")
    except Exception as e:
        print(f"{name}: ERROR ({str(e)})")
