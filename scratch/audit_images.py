import json

with open('src/data/recipes.json', encoding='utf-8') as f:
    recipes = json.load(f)

suspicious = []
meat_keywords = ["בקר", "עוף", "פרגית", "פרגיות", "שניצל", "שווארמה", "קבב", "המבורגר", "עראייס", "בשר", "צלי", "שקשוקה.png", "burger.png", "beef_stew.png", "chicken_broccoli.png", "fish_meatballs.png", "baked_salmon.png"]
vegan_keywords = ["טבעוני", "טבעונית", "צמחוני", "צמחונית"]

for r in recipes:
    name = r['name']
    image = r['image']
    tags = r['tags']
    is_vegan_or_veg = any(x in tags or x in name for x in ["טבעוני", "טבעונית", "צמחוני", "צמחונית"])
    
    # Check if a vegan/vegetarian dish is mapped to a meat image file or URL
    has_meat_image = False
    
    # Local meat images
    if any(m in image for m in ["burger.png", "beef_stew.png", "chicken_broccoli.png", "fish_meatballs.png", "baked_salmon.png"]):
        has_meat_image = True
        
    # Unsplash meat images (based on name-to-url checks in get_specific_image)
    # 1529042410759 is shawarma/kebab/meat
    # 1562967914-608f82629710 is schnitzel
    if any(x in image for x in ["1529042410759", "1562967914"]):
        has_meat_image = True
        
    if is_vegan_or_veg and has_meat_image:
        suspicious.append({
            "id": r["id"],
            "name": name,
            "image": image,
            "tags": tags,
            "reason": "Vegan/Vegetarian dish mapped to a meat image"
        })
        
    # Also check general mismatches
    # e.g. salad getting a soup image, soup getting a salad image, etc.
    if "מרק" in name and "soup" not in image and "red_lentil" not in image and "photo-1476718406336" not in image and "photo-1603105037880" not in image and "photo-1541832676-9b763b0239ab" not in image:
        # If a soup doesn't have a soup image
        suspicious.append({
            "id": r["id"],
            "name": name,
            "image": image,
            "tags": tags,
            "reason": "Soup dish does not have a soup image"
        })
        
    if "סלט" in name and "salad" not in image and "photo-1546069901" not in image and "photo-1540420773" not in image and "photo-1512621776951" not in image and "photo-1525351484163" not in image:
        # If a salad doesn't have a salad image
        suspicious.append({
            "id": r["id"],
            "name": name,
            "image": image,
            "tags": tags,
            "reason": "Salad dish does not have a salad image"
        })

print(f"Audited {len(recipes)} recipes.")
print(f"Found {len(suspicious)} suspicious image assignments:")
for s in suspicious:
    print(f"- [{s['id']}] {s['name']} -> {s['image']} ({s['reason']})")
