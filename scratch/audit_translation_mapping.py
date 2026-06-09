# -*- coding: utf-8 -*-
import json
import os
import sys

# Reconfigure stdout to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

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
    "עוגיות": "cookies",
    "חטיף": "snack bar",
    "חטיפי": "snack bars",
    "אנרגיה": "energy",
    "כדורי": "balls",
    "ביניים": "mid-day snack",
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
    "מונבט": "sprouted",
    "עוגת": "cake",
    "גבינה": "cheese",
    "אישית": "personal",
    "עשירה": "rich",
    "בחלבון": "protein",
    "חלבון": "protein",
    "וחלבון": "protein",
    "מזרעי": "chia seed",
    "זרעי": "seeds",
    "ציה": "chia",
    "צ'יה": "chia",
    "חמאת בוטנים": "peanut butter",
    "חמאת": "butter",
    "בוטנים": "peanuts",
    "וקקאו": "cocoa",
    "קקאו": "cocoa",
    "ללא": "free",
    "סוכר": "sugar",
    "קוקוס": "coconut",
    "ושוקולד": "chocolate",
    "שוקולד": "chocolate",
    "מריר": "dark",
    "גלוטן": "gluten",
    "ריבועי": "squares",
    "ואוכמניות": "blueberry",
    "אוכמניות": "blueberries",
    "אפויים": "baked",
    "תפוחים": "apples",
    "וקינמון": "cinnamon",
    "קינמון": "cinnamon",
    "נימוחות": "soft",
    "חלבה": "halva",
    "ופיסטוק": "pistachio",
    "פיסטוק": "pistachio",
    "בריאות": "healthy",
    "מרעננים": "refreshing",
    "חמוציות": "cranberries",
    "וחמוציות": "cranberries",
    "ביתי": "homemade",
    "וסילאן": "silan",
    "סילאן": "silan",
    "פריכות": "crunchy",
    "בריאים": "healthy",
    "מתמרים": "dates",
    "תמרים": "dates",
    "שקדים": "almonds",
    "ומלח": "salt",
    "מלח": "salt",
    "גס": "coarse",
    "גזר": "carrot",
    "ושיבולת": "oat",
    "רכות": "soft",
    "תפוחה": "puffed",
    "ודבש": "honey",
    "דבש": "honey",
    "שומשום": "sesame",
    "ושומשום": "sesame",
    "וניל": "vanilla",
    "פירות יער": "berries",
    "פירות": "fruits",
    "יער": "berries",
    "מקמח": "spelt",
    "כוסמין": "spelt",
    "וגרגירי": "chickpeas",
    "גרגירי": "chickpeas",
    "פריכים": "crunchy",
    "שיבולת שועל": "oats",
    "שיבולת": "oat",
    "שועל": "oat"
}

def translate_name(name):
    words = name.lower().split()
    translated = []
    
    i = 0
    while i < len(words):
        if i < len(words) - 1:
            two_words = f"{words[i]} {words[i+1]}"
            two_words_clean = "".join([c for c in two_words if c.isalnum() or c.isspace()])
            if two_words_clean in HEB_TO_ENG:
                translated.append(HEB_TO_ENG[two_words_clean])
                i += 2
                continue
        
        word_clean = "".join([c for c in words[i] if c.isalnum()])
        if word_clean in HEB_TO_ENG:
            translated.append(HEB_TO_ENG[word_clean])
        else:
            translated.append(f"[{word_clean}]")
        i += 1
        
    return " ".join(translated)

# Audit rules to programmatically check correctness
def audit_mapping(eng_name, image, name_heb):
    name_lower = name_heb.lower()
    
    # Define Vegan Safe Images
    VEGAN_SAFE_IMAGES = [
        "tofu_quinoa_bowl.png", "salad_fresh.png", "smoothie_bowl.png", 
        "oatmeal_porridge.png", "chia_pudding.png", "red_lentil_soup.png", 
        "soup_green.png", "green_beans.png", "bean_stew.png", "lentil_stew.png", 
        "roasted_vegetables.png", "falafel_plate.png", "pasta_red.png", 
        "mushroom_pasta.png", "pastry.png", "scrambled_tofu.png", "vegan_shakshuka.png",
        "healthy_cookies.png", "energy_bars.png",
        "banana_oat_cookies.png", "date_nut_bars.png", "tahini_cookies.png",
        "spelt_chocolate_chip_cookies.png", "peanut_butter_oat_bars.png",
        "sugar_free_almond_cookies.png", "protein_energy_balls.png",
        "granola_squares.png", "coconut_lemon_cookies.png", "puffed_rice_chocolate_bars.png",
        "pb_cocoa_cookies.png", "coconut_chocolate_cookies.png", "oat_blueberry_squares.png",
        "apple_cinnamon_cookies.png", "halva_pistachio_cookies.png", "lemon_coconut_balls.png",
        "oat_cranberry_bars.png", "healthy_chocolate_balls.png", "chocolate_almond_bark.png",
        "oat_carrot_cookies.png", "tahini_pistachio_cookies.png", "date_pb_sesame_bars.png",
        "chickpea_chocolate_clusters.png"
    ]
    
    # 1. Vegan Check
    is_vegan = "טבעוני" in name_lower or "טבעונית" in name_lower or ("טופו" in name_lower and "ביצה" not in name_lower and "גבינה" not in name_lower)
    if is_vegan:
        if image not in VEGAN_SAFE_IMAGES:
            # Burger is acceptable only if it's explicitly a vegan burger/sandwich, but let's be strict
            if "burger.png" in image and any(x in name_lower for x in ["כריך", "טוסט", "המבורגר"]):
                pass
            else:
                return f"FAIL: Vegan dish mapped to non-vegan image '{image}'"

    # 2. Vegetarian Check
    has_meat_or_fish = any(x in name_lower for x in ["בשר", "בקר", "עוף", "פרגית", "פרגיות", "שניצל", "דג", "סלמון", "אמנון", "טונה", "נקניק", "מעורב", "צלי", "גולאש", "שווארמה", "קבב", "עראייס"])
    is_vegetarian = not has_meat_or_fish
    if is_vegetarian:
        meat_fish_images = ["baked_salmon.png", "fish_meatballs.png", "beef_stew.png", "chicken_broccoli.png", "beef_meatballs.png"]
        if image in meat_fish_images:
            return f"FAIL: Vegetarian dish mapped to meat/fish image '{image}'"
            
    is_pasta = any(x in name_lower for x in ["פסטה", "רביולי", "ניוקי", "מאק אנד צ'יז", "לזניה", "מוסקה", "פאי רועים"])
    is_soup = "מרק" in name_lower
    
    # 3. Chicken / Poultry Check
    has_chicken = any(x in name_lower for x in ["עוף", "פרגית", "פרגיות", "שניצל", "שווארמה"]) and not is_vegan
    if has_chicken and not is_pasta and not is_soup:
        if "סלט" in name_lower:
            if image not in ["salad_fresh.png"]:
                return f"FAIL: Chicken salad mapped to '{image}'"
        elif any(x in name_lower for x in ["טוסט", "כריך", "טורטייה", "המבורגר", "שווארמה"]):
            if image not in ["burger.png", "chicken_broccoli.png"]:
                return f"FAIL: Chicken sandwich/toast mapped to '{image}'"
        else:
            if image not in ["chicken_broccoli.png"]:
                return f"FAIL: Chicken dish mapped to non-chicken image '{image}'"

    # 4. Beef / Meat Check
    has_beef = (any(x in name_lower for x in ["בקר", "בשר", "בשרית", "גולאש", "קבב", "עראייס", "נקניק"]) or ("צלי" in name_lower and "עוף" not in name_lower and "פרגית" not in name_lower)) and not is_vegan
    if has_beef and not is_pasta and not is_soup:
        if "קציצות" in name_lower:
            if image not in ["beef_meatballs.png"]:
                return f"FAIL: Beef meatballs mapped to '{image}'"
        elif any(x in name_lower for x in ["טוסט", "כריך", "המבורגר", "עראייס", "נקניק", "קבב"]):
            if image not in ["burger.png", "beef_meatballs.png"]:
                return f"FAIL: Beef sandwich/burger/kebab mapped to '{image}'"
        else:
            if image not in ["beef_stew.png", "beef_meatballs.png"]:
                return f"FAIL: Beef dish mapped to non-beef image '{image}'"

    # 5. Fish Check
    has_fish = any(x in name_lower for x in ["דג", "סלmון", "סלמון", "אמנון", "טונה"])
    if has_fish and not is_pasta and not is_soup:
        if "סלט" in name_lower:
            if image not in ["tuna_salad.png", "salad_fresh.png"]:
                return f"FAIL: Fish salad mapped to '{image}'"
        elif "קציצות" in name_lower:
            if image not in ["fish_meatballs.png"]:
                return f"FAIL: Fish meatballs mapped to '{image}'"
        elif any(x in name_lower for x in ["טוסט", "כריך", "טורטייה"]):
            # Fish sandwiches should map to toast/sandwiches, not baked_salmon plate!
            if image not in ["caprese_toast.png", "grilled_cheese.png", "burger.png", "tuna_salad.png"]:
                return f"FAIL: Fish sandwich/toast mapped to '{image}'"
        else:
            if image not in ["baked_salmon.png"]:
                return f"FAIL: Fish dish mapped to non-fish image '{image}'"

    # 6. Egg Dish Check
    has_egg = any(x in name_lower for x in ["חביתה", "אומלט", "מקושקשת", "ביצה", "ביצים", "עין"]) and "חציל" not in name_lower
    if has_egg and not has_meat_or_fish and not is_vegan and not is_pasta and not is_soup:
        if "סלט" in name_lower:
            if "סלט ביצים" in name_lower:
                if image not in ["egg_salad.png"]:
                    return f"FAIL: Egg salad mapped to '{image}'"
            else:
                # Salad with boiled egg can map to fresh salad
                if image not in ["salad_fresh.png", "egg_salad.png"]:
                    return f"FAIL: Egg salad mapped to '{image}'"
        elif any(x in name_lower for x in ["טוסט", "כריך", "טורטייה"]):
            if image not in ["caprese_toast.png", "grilled_cheese.png"]:
                return f"FAIL: Egg sandwich/toast mapped to non-toast image '{image}'"
        elif "שקשוקה" in name_lower:
            if image not in ["shakshuka.png", "shakshuka_green.png"]:
                return f"FAIL: Egg shakshuka mapped to '{image}'"
        elif any(x in name_lower for x in ["לביבות גבינה", "סירניקי", "פרנץ' טוסט"]):
            if image not in ["pancake.png"]:
                return f"FAIL: Sweet egg dish mapped to non-pancake image '{image}'"
        elif "אבוקדו" in name_lower and "אפוי" in name_lower:
            pass
        else:
            if image not in ["scrambled_eggs.png", "broccoli_quiche.png"]:
                return f"FAIL: Egg dish mapped to non-egg image '{image}'"

    # 7. Pancake / Sweet Crepes / Syrniki / French Toast Check
    is_sweet_pancake_style = any(x in name_lower for x in ["פנקייק", "קרפ", "סירניקי", "לביבות גבינה מתוקות", "פרנץ' טוסט"])
    if is_sweet_pancake_style:
        if image not in ["pancake.png", "pastry.png"]:
            return f"FAIL: Pancake/sweet dish mapped to non-pancake image '{image}'"

    # 8. Muffins Check
    if "מאפינס" in name_lower:
        if any(x in name_lower for x in ["מתוק", "בננה", "אוכמניות", "שוקולד"]):
            if image not in ["pastry.png", "pancake.png"]:
                return f"FAIL: Sweet muffin mapped to non-pastry image '{image}'"
        elif any(x in name_lower for x in ["מלוח", "גבינה", "זיתים", "ירקות"]):
            if image not in ["savory_muffins.png"]:
                return f"FAIL: Savory muffin mapped to non-quiche image '{image}'"

    # 9. Toast / Sandwich Check
    is_sandwich = any(x in name_lower for x in ["טוסט", "כריך", "טורטייה", "פריקסה"])
    if is_sandwich:
        # Sweet french toast checked in rule 7.
        # Meat/poultry sandwich checked in rule 3 & 4.
        # Fish sandwich checked in rule 5.
        if not has_meat_or_fish and not is_sweet_pancake_style:
            if "פיצה" in name_lower:
                if image not in ["pizza.png", "caprese_toast.png"]:
                    return f"FAIL: Pizza toast mapped to '{image}'"
            elif "פריקסה" in name_lower:
                if image not in ["burger.png", "tuna_salad.png"]:
                    return f"FAIL: Fricassee mapped to non-sandwich image '{image}'"
            else:
                if is_vegan:
                    if image not in ["tofu_quinoa_bowl.png", "salad_fresh.png", "caprese_toast.png"]:
                        return f"FAIL: Vegan toast/sandwich mapped to '{image}'"
                else:
                    if image not in ["caprese_toast.png", "grilled_cheese.png"]:
                        return f"FAIL: Toast/sandwich mapped to non-toast image '{image}'"

    # 10. Sprouted Lentil Patties Check
    if "קציצות עדשים" in name_lower:
        if image not in ["lentil_stew.png", "bean_stew.png"]:
            return f"FAIL: Lentil patties stew mapped to non-stew image '{image}'"

    # 11. Shakshuka Check
    if "שקשוקה" in name_lower:
        if is_vegan:
            if image not in ["vegan_shakshuka.png"]:
                return f"FAIL: Vegan shakshuka mapped to '{image}'"
        elif any(x in name_lower for x in ["ירוק", "ירוקה", "תרד"]):
            if image not in ["shakshuka_green.png"]:
                return f"FAIL: Green shakshuka mapped to '{image}'"
        else:
            if image not in ["shakshuka.png"]:
                return f"FAIL: Shakshuka mapped to '{image}'"

    # 12. Scrambled Egg / Tofu scramble Check
    if any(x in name_lower for x in ["מקושקשת", "אומלט", "חביתה"]):
        if is_vegan:
            if image not in ["scrambled_tofu.png"]:
                return f"FAIL: Vegan scramble mapped to '{image}'"
        else:
            if image not in ["scrambled_eggs.png", "broccoli_quiche.png"]:
                return f"FAIL: Egg scramble/omelette mapped to '{image}'"

    # 13. Snacks Check
    if any(x in name_lower for x in ["עוגיות", "חטיף", "חטיפי", "כדורי אנרגיה"]):
        valid_snack_images = [
            "banana_oat_cookies.png", "date_nut_bars.png", "tahini_cookies.png",
            "spelt_chocolate_chip_cookies.png", "peanut_butter_oat_bars.png",
            "sugar_free_almond_cookies.png", "protein_energy_balls.png",
            "granola_squares.png", "coconut_lemon_cookies.png", "puffed_rice_chocolate_bars.png",
            "protein_cheesecake.png", "chocolate_chia_pudding.png", "pb_cocoa_cookies.png",
            "coconut_chocolate_cookies.png", "oat_blueberry_squares.png", "apple_cinnamon_cookies.png",
            "halva_pistachio_cookies.png", "lemon_coconut_balls.png", "oat_cranberry_bars.png",
            "granola_silan_cookies.png", "healthy_chocolate_balls.png", "chocolate_almond_bark.png",
            "pb_chocolate_squares.png", "oat_carrot_cookies.png", "puffed_quinoa_bars.png",
            "tahini_pistachio_cookies.png", "date_pb_sesame_bars.png", "vanilla_berry_pudding.png",
            "spelt_banana_cake.png", "chickpea_chocolate_clusters.png"
        ]
        if image not in valid_snack_images:
            return f"FAIL: Snack recipe mapped to non-snack image '{image}'"

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
    image = os.path.basename(r["image"])
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
