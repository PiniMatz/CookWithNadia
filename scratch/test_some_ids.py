import urllib.request
import urllib.error

# Candidates for grilled cheese / plain cheese toast
candidates = {
    "grilled_cheese_1": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=600&auto=format&fit=crop&q=80",
    "grilled_cheese_2": "https://images.unsplash.com/photo-1528736235302-52922df5c122?w=600&auto=format&fit=crop&q=80",
    "toast_butter_1": "https://images.unsplash.com/photo-1538220856186-0be0e085984d?w=600&auto=format&fit=crop&q=80",
    "toast_plain_1": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&auto=format&fit=crop&q=80",
    "toast_plain_2": "https://images.unsplash.com/photo-1592417817098-8f3d6eb19675?w=600&auto=format&fit=crop&q=80",
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
