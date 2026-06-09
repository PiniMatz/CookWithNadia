import shutil
import os

source_dir = r"C:\Users\pini_\.gemini\antigravity\brain\da901973-5028-491f-a583-333b54599e58"
dest_dir = r"c:\Users\pini_\Documents\Private\Pini\AntiGravity\BashlaNadia\src\images"

mappings = {
    "oatmeal_porridge_1780994984801.png": "oatmeal_porridge.png",
    "scrambled_eggs_1780995001596.png": "scrambled_eggs.png",
    "caprese_toast_1780995018744.png": "caprese_toast.png",
    "grilled_cheese_1780995034797.png": "grilled_cheese.png",
    "egg_salad_1780995050563.png": "egg_salad.png",
    "tuna_salad_1780995065936.png": "tuna_salad.png",
    "smoothie_bowl_1780995080886.png": "smoothie_bowl.png",
    "labneh_dip_1780995096984.png": "labneh_dip.png",
    "chia_pudding_1780995113324.png": "chia_pudding.png",
    "muesli_yogurt_1780995131208.png": "muesli_yogurt.png",
    "green_beans_1780995150601.png": "green_beans.png",
    "bean_stew_1780995166490.png": "bean_stew.png",
    "falafel_plate_1780995184865.png": "falafel_plate.png",
    "shakshuka_green_1780995203090.png": "shakshuka_green.png",
    "pasta_red_1780995219831.png": "pasta_red.png",
    "beef_meatballs_1780995237171.png": "beef_meatballs.png",
    "roasted_vegetables_1780995254084.png": "roasted_vegetables.png"
}

os.makedirs(dest_dir, exist_ok=True)

for src_name, dest_name in mappings.items():
    src_path = os.path.join(source_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} -> {dest_name}")
    else:
        print(f"WARNING: Source file {src_path} does not exist!")

print("All copies completed.")
