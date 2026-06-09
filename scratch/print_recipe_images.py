import json

with open('src/data/recipes.json', encoding='utf-8') as f:
    recipes = json.load(f)

with open('scratch/recipe_images.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(f"Total recipes: {len(recipes)}\n\n")
    for r in recipes:
        f_out.write(f"ID: {r['id']}\n")
        f_out.write(f"Name: {r['name']}\n")
        f_out.write(f"Category: {r['category']}\n")
        f_out.write(f"Image: {r['image']}\n")
        f_out.write(f"Tags: {', '.join(r['tags'])}\n")
        f_out.write(f"Ingredients: {', '.join([i['name'] for i in r['ingredients']])}\n")
        f_out.write("-" * 40 + "\n")

print("Generated scratch/recipe_images.txt successfully.")
