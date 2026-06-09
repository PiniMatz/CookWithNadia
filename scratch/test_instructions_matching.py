# -*- coding: utf-8 -*-
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Import get_recipe_instructions from generate_recipes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scratch.generate_recipes import get_recipe_instructions

with open("src/data/recipes.json", encoding="utf-8") as f:
    recipes = json.load(f)

print(f"Loaded {len(recipes)} recipes.")

categories_matched = {}

for r in recipes:
    name = r["name"]
    name_lower = name.lower()
    ing_names = [i["name"] for i in r["ingredients"]]
    category = r["category"]
    
    prep, cook, total, inst, rule_name = get_recipe_instructions(name, ing_names, category)
    
    # Try to determine which rule matched by searching the first instruction
    first_inst = inst[0]
        
    categories_matched[rule_name] = categories_matched.get(rule_name, 0) + 1
    
    # We want to print potential warnings:
    # 1. Fallbacks
    # 2. Savory spreads or salads matching sweet rules
    is_warning = False
    warning_reason = ""
    
    if rule_name == "Fallback":
        is_warning = True
        warning_reason = "Uses generic fallback instructions"
    elif rule_name == "9. Muesli/Yogurt" and any(x in name for x in ["ממרח", "לאבנה", "טחינה"]):
        is_warning = True
        warning_reason = "Savory spread matched sweet Yogurt/Muesli rule"
    elif rule_name == "4. Chia/Yogurt/Muesli" and "מאפינס" in name:
        is_warning = True
        warning_reason = "Muffin matched sweet Yogurt/Muesli rule"
        
    if is_warning or r["id"] < 15: # show base recipes too just in case
        print(f"ID {r['id']} - {name} ({r['category']}):")
        print(f"  -> Matched Rule: {rule_name}")
        print(f"  -> First Instruction: {first_inst}")
        if is_warning:
            print(f"  ⚠️ WARNING: {warning_reason}")
        print()

print("\n--- Summary of Matches ---")
for cat, count in sorted(categories_matched.items()):
    print(f"{cat}: {count}")
