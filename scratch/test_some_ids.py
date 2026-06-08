import urllib.request
import urllib.error

ids_to_test = {
    "oatmeal_1": "https://images.unsplash.com/photo-1505576399279-565b52d4ac71?w=600&auto=format&fit=crop&q=80",
    "oatmeal_2": "https://images.unsplash.com/photo-1517686469429-8faf88b9f7cf?w=600&auto=format&fit=crop&q=80",
    "oatmeal_3": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&auto=format&fit=crop&q=80",
    "oatmeal_4": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=600&auto=format&fit=crop&q=80",
    "oatmeal_5": "https://images.unsplash.com/photo-1501156938622-7a59f137667e?w=600&auto=format&fit=crop&q=80",
    "oatmeal_6": "https://images.unsplash.com/photo-1551248429-40975aa4de74?w=600&auto=format&fit=crop&q=80",
    "oatmeal_7": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=600&auto=format&fit=crop&q=80",
}

print("Testing oatmeal IDs...")
for k, url in ids_to_test.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=3) as res:
            print(f"{k}: SUCCESS (Status {res.getcode()})")
    except urllib.error.HTTPError as e:
        print(f"{k}: FAILED (HTTP Error {e.code})")
    except Exception as e:
        print(f"{k}: ERROR ({str(e)})")
