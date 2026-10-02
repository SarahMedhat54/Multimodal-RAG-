from pathlib import Path

IMAGES_DIR = Path("data/images")


FIXES = {
    "tigger": "tiger",
    "brown_bear": "brown_bear",
}

for img in IMAGES_DIR.glob("*.jpg"):
    new_name = img.name.lower()
    for wrong, right in FIXES.items():
        new_name = new_name.replace(wrong, right)
    if new_name != img.name:


        tmp = img.with_name("tmp_" + new_name)
        img.rename(tmp)
        tmp.rename(img.with_name(new_name))
        print(f"{img.name} -> {new_name}")

print("ok!")