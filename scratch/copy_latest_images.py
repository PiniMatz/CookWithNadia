import os
import shutil
import glob

source_dir = r"C:\Users\pini_\.gemini\antigravity\brain\da901973-5028-491f-a583-333b54599e58"
dest_dir = r"c:\Users\pini_\Documents\Private\Pini\AntiGravity\BashlaNadia\src\images"

targets = [
    "pb_cocoa_cookies",
    "coconut_chocolate_cookies",
    "oat_blueberry_squares",
    "apple_cinnamon_cookies",
    "halva_pistachio_cookies",
    "lemon_coconut_balls",
    "oat_cranberry_bars",
    "granola_silan_cookies",
    "healthy_chocolate_balls",
    "chocolate_almond_bark",
    "pb_chocolate_squares",
    "oat_carrot_cookies",
    "puffed_quinoa_bars",
    "tahini_pistachio_cookies",
    "date_pb_sesame_bars",
    "vanilla_berry_pudding",
    "spelt_banana_cake",
    "chickpea_chocolate_clusters"
]

os.makedirs(dest_dir, exist_ok=True)

for target in targets:
    # Look for target_*.png or target.png in source_dir
    pattern = os.path.join(source_dir, f"{target}_*.png")
    matches = glob.glob(pattern)
    
    # Also look for target.png
    direct_file = os.path.join(source_dir, f"{target}.png")
    if os.path.exists(direct_file):
        matches.append(direct_file)
        
    if not matches:
        print(f"No matches found for {target} in artifacts directory.")
        continue
        
    # Sort by modification time to get the latest
    matches.sort(key=os.path.getmtime, reverse=True)
    latest_file = matches[0]
    
    dest_path = os.path.join(dest_dir, f"{target}.png")
    shutil.copy2(latest_file, dest_path)
    print(f"Successfully copied: {os.path.basename(latest_file)} -> {target}.png")

print("Done copying all latest assets.")
