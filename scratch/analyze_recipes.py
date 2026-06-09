# -*- coding: utf-8 -*-
import json
import os

# Define the proposed 26 assets
EXISTING_ASSETS = [
    "baked_salmon.png", "beef_lasagna.png", "beef_stew.png", "broccoli_quiche.png",
    "burger.png", "chicken_broccoli.png", "fish_meatballs.png", "lentil_stew.png",
    "mushroom_pasta.png", "pancake.png", "pastry.png", "pizza.png",
    "red_lentil_soup.png", "salad_fresh.png", "shakshuka.png", "soup_green.png",
    "tofu_quinoa_bowl.png"
]

NEW_PROPOSED_ASSETS = [
    "oatmeal_porridge.png", "scrambled_eggs.png", "caprese_toast.png", "chia_pudding.png",
    "muesli_yogurt.png", "green_beans.png", "bean_stew.png", "falafel_plate.png",
    "shakshuka_green.png", "egg_salad.png", "tuna_salad.png", "smoothie_bowl.png",
    "labneh_dip.png", "grilled_cheese.png", "pasta_red.png", "beef_meatballs.png",
    "roasted_vegetables.png"
]

ALL_ASSETS = EXISTING_ASSETS + NEW_PROPOSED_ASSETS

def propose_mapping(name, category, ingredients):
    name_lower = name.lower()
    
    # 1. Soups (Even if they contain pasta or meat, visually they are soups)
    if "מרק" in name_lower:
        if any(x in name_lower for x in ["עדשים כתומות", "עדשים אדומות", "בטטה", "תירס"]):
            return "red_lentil_soup.png"
        if "שעועית" in name_lower or "חרירה" in name_lower:
            return "bean_stew.png"
        return "soup_green.png"

    # 2. Salads (Egg salad and Tuna salad are visually distinct from Garden salad)
    if "סלט" in name_lower:
        if "ביצים" in name_lower:
            return "egg_salad.png"
        if "טונה" in name_lower or "ניסואז" in name_lower:
            return "tuna_salad.png"
        return "salad_fresh.png"

    # 3. Labneh / Dips / Spreads
    if any(x in name_lower for x in ["לאבנה", "מטבל", "ממרח", "טחינה"]):
        return "labneh_dip.png"

    # 4. Smoothies / Shakes
    if any(x in name_lower for x in ["שייק", "סמוטי"]):
        return "smoothie_bowl.png"

    # 5. Specific dish overrides
    if "לזניה" in name_lower or "מוסקה" in name_lower or "פאי רועים" in name_lower:
        return "beef_lasagna.png"
    if "פרנץ' טוסט" in name_lower:
        return "pancake.png"
    if any(x in name_lower for x in ["פסטה", "רביולי", "ניוקי", "מאק אנד צ'יז"]):
        if any(x in name_lower for x in ["בולונז", "בשר", "עגבניות", "רוזה"]):
            return "pasta_red.png"
        return "mushroom_pasta.png"
    if "פיצה" in name_lower:
        return "pizza.png"
    if "פלאפל" in name_lower:
        return "falafel_plate.png"
    if any(x in name_lower for x in ["בורקס", "פוקאצ'ה", "ברוסקטה", "לחם", "פאי בצל"]):
        return "pastry.png"
    if "מאפינס" in name_lower:
        return "pastry.png"
    if any(x in name_lower for x in ["פנקייק", "קרפ"]):
        return "pancake.png"

    # 6. Egg Dishes
    if "שקשוקה" in name_lower:
        if any(x in name_lower for x in ["ירוק", "ירוקה", "תרד"]):
            return "shakshuka_green.png"
        return "shakshuka.png"
    if any(x in name_lower for x in ["אומלט", "חביתה", "מקושקשת", "ביצה", "ביצים", "סירניקי", "לביבות גבינה"]):
        return "scrambled_eggs.png"

    # 7. Oats, Porridge, Chia, Yogurt
    if "צ'יה" in name_lower or "פודינג" in name_lower:
        return "chia_pudding.png"
    if "קוואקר" in name_lower or "דייסה" in name_lower or "סולת" in name_lower:
        return "oatmeal_porridge.png"
    if any(x in name_lower for x in ["מוזלי", "גרנולה", "יוגורט"]):
        return "muesli_yogurt.png"

    # 8. Toasts / Sandwiches / Wraps
    if any(x in name_lower for x in ["טוסט", "כריך", "טורטייה", "פריקסה"]):
        if "סלמון" in name_lower:
            return "baked_salmon.png"
        if any(x in name_lower for x in ["חזה עוף", "נקניק", "בשרי", "פרגית", "עוף"]):
            return "burger.png"
        if any(x in name_lower for x in ["זעתר", "צהובה", "גבינה צהובה"]):
            return "grilled_cheese.png"
        return "caprese_toast.png"

    # 9. Fish
    if any(x in name_lower for x in ["דג", "סלמון", "אמנון", "טונה"]):
        if "קציצות" in name_lower:
            return "fish_meatballs.png"
        return "baked_salmon.png"

    # 10. Meat / Poultry
    is_meat = any(x in name_lower for x in ["בשר", "בקר", "עוף", "פרגית", "פרגיות", "שניצל", "קבב", "המבורגר", "עראייס", "קדירה", "בשרית", "גולאש", "נקניק", "מעורב", "צלי", "קציצות"])
    if is_meat:
        if any(x in name_lower for x in ["המבורגר", "עראייס", "נקניק", "שווארמה", "קבב"]):
            return "burger.png"
        if any(x in name_lower for x in ["קדיר", "בקר", "צלי", "גולאש"]):
            return "beef_stew.png"
        if "קציצות" in name_lower:
            return "beef_meatballs.png"
        return "chicken_broccoli.png"

    # 11. Vegetarian / Vegan Main Dishes & Legumes
    if "שעועית ירוקה" in name_lower:
        return "green_beans.png"
    if any(x in name_lower for x in ["שעועית אדומה", "שעועית לבנה", "לובייה"]):
        return "bean_stew.png"
    if any(x in name_lower for x in ["קיש", "פשטידה", "פשטידת", "סופלה", "גלילות חציל", "כרובית אפויה", "מוקרם", "מוקרמים"]):
        return "broccoli_quiche.png"
    if any(x in name_lower for x in ["ירקות קלויים", "ירקות בתנור", "בטטה אפויה"]):
        return "roasted_vegetables.png"
    if any(x in name_lower for x in ["בודהה", "טופו", "קינואה", "כוסמת", "בורגול", "מג'דרה", "אורז", "מוקפץ"]):
        return "tofu_quinoa_bowl.png"
    if any(x in name_lower for x in ["עדשים", "קארי", "תבשיל", "דאל", "חציל ממולא", "פלפלים ממולאים"]):
        if "צ'ילי" in name_lower:
            return "bean_stew.png"
        return "lentil_stew.png"

    # Default fallbacks based on category
    if "בוקר" in category:
        return "tofu_quinoa_bowl.png"
    return "salad_fresh.png"

# Read recipes
recipe_file = "src/data/recipes.json"
with open(recipe_file, encoding="utf-8") as f:
    recipes = json.load(f)

# Run mapping analysis
mapped_recipes = []
asset_counts = {asset: 0 for asset in ALL_ASSETS}

for r in recipes:
    asset = propose_mapping(r["name"], r["category"], [i["name"] for i in r["ingredients"]])
    asset_counts[asset] += 1
    mapped_recipes.append({
        "id": r["id"],
        "name": r["name"],
        "category": r["category"],
        "proposed_image": asset,
        "is_new": asset in NEW_PROPOSED_ASSETS
    })

# Write to markdown artifact
artifact_path = "C:\\Users\\pini_\\.gemini\\antigravity\\brain\\da901973-5028-491f-a583-333b54599e58\\recipe_image_mapping.md"
with open(artifact_path, "w", encoding="utf-8") as f_out:
    f_out.write("# Proposed Recipe-to-Image Mappings\n\n")
    f_out.write("This document lists all **196 recipes** in the CookWithNadia database and maps them to one of our **26 local assets** (17 existing and 9 proposed).\n\n")
    
    f_out.write("## Summary Statistics\n\n")
    f_out.write("| Image Asset | Type | Count of Recipes Mapped |\n")
    f_out.write("| --- | --- | --- |\n")
    for asset in ALL_ASSETS:
        status = "🆕 Proposed New" if asset in NEW_PROPOSED_ASSETS else "✅ Existing"
        f_out.write(f"| `{asset}` | {status} | {asset_counts[asset]} |\n")
        
    f_out.write("\n## Complete Recipe Mapping Table\n\n")
    f_out.write("| ID | Recipe Name | Category | Mapped Image | Status |\n")
    f_out.write("| --- | --- | --- | --- | --- |\n")
    for mr in mapped_recipes:
        status = "🆕 Proposed" if mr["is_new"] else "✅ Existing"
        f_out.write(f"| {mr['id']} | {mr['name']} | {mr['category']} | `{mr['proposed_image']}` | {status} |\n")

print(f"Generated {artifact_path} successfully.")
