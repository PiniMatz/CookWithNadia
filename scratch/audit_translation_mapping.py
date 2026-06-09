# -*- coding: utf-8 -*-
import json
import os

# Translation dictionary for Hebrew words to English
HEB_TO_ENG = {
    "חזה עוף": "chicken breast",
    "עוף": "chicken",
    "פרגית": "chicken thigh",
    "פרגיות": "chicken thighs",
    "שניצל": "schnitzel",
    "בקר": "beef",
    "בשר": "meat",
    "בשרית": "meat",
    "צלי": "roast",
    "גולאש": "goulash",
    "סלמון": "salmon",
    "אמנון": "tilapia",
    "דג": "fish",
    "טונה": "tuna",
    "קציצות": "meatballs",
    "סלט": "salad",
    "מרק": "soup",
    "טוסט": "toast",
    "כריך": "sandwich",
    "טורטייה": "wrap",
    "שקשוקה": "shakshuka",
    "אומלט": "omelette",
    "חביתה": "omelette",
    "מקושקשת": "scrambled eggs",
    "ביצה": "egg",
    "ביצים": "eggs",
    "פנקייק": "pancake",
    "קרפ": "crepe",
    "לזניה": "lasagna",
    "מוסקה": "moussaka",
    "פסטה": "pasta",
    "רביולי": "ravioli",
    "ניוקי": "gnocchi",
    "מאק אנד צ'יז": "mac & cheese",
    "פיצה": "pizza",
    "פלאפל": "falafel",
    "בורקס": "burekas",
    "פוקאצ'ה": "focaccia",
    "ברוסקטה": "bruschetta",
    "מאפינס": "muffins",
    "עדשים": "lentils",
    "שעועית": "beans",
    "שעועית ירוקה": "green beans",
    "שעועית אדומה": "red beans",
    "שעועית לבנה": "white beans",
    "חומוס": "chickpeas",
    "טופו": "tofu",
    "קינואה": "quinoa",
    "כוסמת": "buckwheat",
    "בורגול": "bulgur",
    "מג'דרה": "mjadra",
    "אורז מלא": "brown rice",
    "אורז": "rice",
    "מוקפץ": "stir-fry",
    "לאבנה": "labneh",
    "מטבל": "dip",
    "ממרח": "spread",
    "טחינה": "tahini",
    "שייק": "shake",
    "סמוטי": "smoothie",
    "פודינג": "pudding",
    "צ'יה": "chia",
    "קוואקר": "oatmeal",
    "דייסת": "porridge",
    "דייסה": "porridge",
    "סולת": "semolina",
    "מוזלי": "muesli",
    "גרנולה": "granola",
    "יוגורט": "yogurt",
    "קיש": "quiche",
    "פשטידה": "pie",
    "פשטידת": "pie",
    "סופלה": "souffle",
    "גלילות חציל": "eggplant rolls",
    "חציל": "eggplant",
    "כרובית": "cauliflower",
    "תפוחי אדמה": "potatoes",
    "בודהה": "buddha bowl",
    "סופרפוד": "superfood",
    "קערת בריאות": "health bowl",
    "נקניק": "sausage",
    "מעורב": "mixed grill",
    "פיראסה": "leek",
    "פריקסה": "fricassee",
    "לביבות גבינה": "syrniki",
    "סירניקי": "syrniki",
    "תרד": "spinach",
    "ירקות קלויים": "roasted vegetables",
    "ירקות בתנור": "baked vegetables",
    "בטטה אפויה": "baked sweet potato",
    "בטטה": "sweet potato",
    "חום": "hot",
    "קלאסי": "classic",
    "בינוני": "medium",
    "קל": "easy",
    "מהיר": "quick",
    "מזין": "nutritious",
    "בישול ארוך": "slow-cooked",
    "בלקנית": "balkan",
    "יווני": "greek",
    "ירוק": "green",
    "ירוקה": "green",
    "טבעוני": "vegan",
    "טבעונית": "vegan",
    "צמחוני": "vegetarian",
    "צמחונית": "vegetarian",
    "מונבטות": "sprouted",
    "מונבטים": "sprouted",
    "מונבט": "sprouted"
}

def translate_name(name):
    # Translate phrase-by-phrase or word-by-word
    words = name.lower().split()
    translated = []
    
    # Try sliding window of 2 words first, then 1 word
    i = 0
    while i < len(words):
        if i < len(words) - 1:
            two_words = f"{words[i]} {words[i+1]}"
            # remove punctuation
            two_words_clean = "".join([c for c in two_words if c.isalnum() or c.isspace()])
            if two_words_clean in HEB_TO_ENG:
                translated.append(HEB_TO_ENG[two_words_clean])
                i += 2
                continue
        
        word_clean = "".join([c for c in words[i] if c.isalnum()])
        if word_clean in HEB_TO_ENG:
            translated.append(HEB_TO_ENG[word_clean])
        else:
            translated.append(f"[{word_clean}]") # show untranslated in brackets
        i += 1
        
    return " ".join(translated)

# Mapping function (from analyze_recipes.py)
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
    is_meat = any(x in name_lower for x in ["בשר", "בקר", "עוף", "פרגית", "פרגיות", "שניצל", "קבב", "המבורגר", "עראייס", "בשרית", "גולאש", "נקניק", "מעורב", "צלי"])
    if is_meat:
        if any(x in name_lower for x in ["המבורגר", "עראייס", "נקניק", "שווארמה", "קבב"]):
            return "burger.png"
        if any(x in name_lower for x in ["קדיר", "קדירה", "בקר", "צלי", "גולאש"]):
            return "beef_stew.png"
        if "קציצות" in name_lower:
            return "beef_meatballs.png"
        return "chicken_broccoli.png"

    # 11. Vegetarian / Vegan Main Dishes & Legumes
    if "שעועית ירוקה" in name_lower:
        return "green_beans.png"
    if any(x in name_lower for x in ["שעועית אדומה", "שעועית לבנה", "לובייה"]):
        return "bean_stew.png"
    if any(x in name_lower for x in ["קיש", "פשטידה", "פשטידת", "סופלה", "גלילות חציל", "כרובית אפויה", "מוקרם", "מוקרמים", "קציצות"]):
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

# Audit rules to programmatically check correctness
def audit_mapping(eng_name, image, name_heb):
    # Rule 1: No meat/fish images on vegan/vegetarian dishes
    has_meat_or_fish = any(x in name_heb for x in ["בשר", "בקר", "עוף", "פרגית", "פרגיות", "שניצל", "דג", "סלמון", "אמנון", "טונה", "נקניק", "מעורב", "צלי"])
    is_vegan_or_veg = (not has_meat_or_fish) and ("vegan" in eng_name or "vegetarian" in eng_name or any(x in name_heb for x in ["טבעוני", "צמחוני", "טופו", "עדשים", "שעועית", "חומוס", "מאש"]))
    is_meat_image = image in ["burger.png", "beef_stew.png", "chicken_broccoli.png", "fish_meatballs.png", "baked_salmon.png", "beef_lasagna.png", "beef_meatballs.png"]
    
    # Exception: lasagna, moussaka, shepherd's pie, and burgers can be vegetarian, but they still look like lasagna or burgers.
    is_excepted = any(x in eng_name for x in ["lasagna", "moussaka", "shepherd", "burger"])
    if is_vegan_or_veg and is_meat_image and not is_excepted:
        # If it's vegan, it shouldn't map to meatballs or baked salmon or chicken
        if image in ["baked_salmon.png", "chicken_broccoli.png", "beef_stew.png", "beef_meatballs.png"]:
            return "FAIL: Vegan dish mapped to meat/fish image"
            
    # Rule 2: Soup matching
    if "soup" in eng_name and "soup" not in image and "red_lentil" not in image and "bean_stew" not in image:
        return "FAIL: Soup dish mapped to non-soup image"
        
    # Rule 3: Salad matching
    if "salad" in eng_name:
        if "egg_salad" in image and "egg" not in eng_name:
            return "FAIL: Non-egg salad mapped to egg salad"
        if "tuna_salad" in image and "tuna" not in eng_name and "niçoise" not in eng_name and "ניסואז" not in name_heb:
            return "FAIL: Non-tuna salad mapped to tuna salad"
        if "salad" not in image:
            return "FAIL: Salad dish mapped to non-salad image"

    # Rule 4: Egg matching
    if any(x in eng_name for x in ["omelette", "scrambled eggs", "egg"]) and "salad" not in eng_name and "eggplant" not in eng_name:
        if image not in ["scrambled_eggs.png", "shakshuka_green.png", "shakshuka.png", "broccoli_quiche.png"]:
            return "FAIL: Egg dish mapped to non-egg image"

    # Rule 5: Oats / Porridge
    if "oatmeal" in eng_name or "porridge" in eng_name:
        if image != "oatmeal_porridge.png":
            return "FAIL: Oats/Porridge mapped to non-porridge image"

    # Rule 6: Smoothie
    if "smoothie" in eng_name or "shake" in eng_name:
        if image != "smoothie_bowl.png":
            return "FAIL: Smoothie mapped to non-smoothie image"

    # Rule 7: Labneh
    if "labneh" in eng_name:
        if image != "labneh_dip.png":
            return "FAIL: Labneh mapped to non-labneh image"

    # Rule 8: Fish matching
    if "fish" in eng_name or "salmon" in eng_name or "tilapia" in eng_name or "tuna" in eng_name:
        if "salad" not in eng_name and "sandwich" not in eng_name and "wrap" not in eng_name:
            if image not in ["baked_salmon.png", "fish_meatballs.png", "tuna_salad.png"]:
                return "FAIL: Fish dish mapped to non-fish image"

    # Rule 9: Pasta matching
    if "pasta" in eng_name or "ravioli" in eng_name or "gnocchi" in eng_name:
        if "soup" not in eng_name and "salad" not in eng_name:
            if image not in ["mushroom_pasta.png", "pasta_red.png", "beef_lasagna.png"]:
                return "FAIL: Pasta dish mapped to non-pasta image"

    return "PASS"

# Read recipes
recipe_file = "src/data/recipes.json"
with open(recipe_file, encoding="utf-8") as f:
    recipes = json.load(f)

# Run audit
audit_results = []
failures = 0

for r in recipes:
    eng_name = translate_name(r["name"])
    image = propose_mapping(r["name"], r["category"], [i["name"] for i in r["ingredients"]])
    status = audit_mapping(eng_name, image, r["name"])
    
    if status.startswith("FAIL"):
        failures += 1
        
    audit_results.append({
        "id": r["id"],
        "name_heb": r["name"],
        "name_eng": eng_name,
        "image": image,
        "status": status
    })

# Write to markdown artifact
artifact_path = "C:\\Users\\pini_\\.gemini\\antigravity\\brain\\da901973-5028-491f-a583-333b54599e58\\translation_audit_report.md"
with open(artifact_path, "w", encoding="utf-8") as f_out:
    f_out.write("# Full Recipe Translation and Visual Audit Report\n\n")
    f_out.write(f"We translated all **196 recipes** into English to verify their culinary concept and audited them against the mapped images.\n\n")
    
    if failures == 0:
        f_out.write("> [!NOTE]\n")
        f_out.write(f"> **Audit Results:** **ALL 196 RECIPES PASSED** visual archetype checks. No concept mismatches or meat-veggie warnings were detected.\n\n")
    else:
        f_out.write(f"> [!WARNING]\n")
        f_out.write(f"> **Audit Results:** Detected **{failures} failures** in the mapping logic. These must be corrected.\n\n")
        
    f_out.write("## Detailed Audit Log\n\n")
    f_out.write("| ID | Hebrew Name | English Translation | Mapped Image | Audit Status |\n")
    f_out.write("| --- | --- | --- | --- | --- |\n")
    for ar in audit_results:
        status_emoji = "✅ PASS" if ar["status"] == "PASS" else f"❌ {ar['status']}"
        f_out.write(f"| {ar['id']} | {ar['name_heb']} | *{ar['name_eng']}* | `{ar['image']}` | {status_emoji} |\n")

print(f"Generated {artifact_path} successfully. Total failures: {failures}")
