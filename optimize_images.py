from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent / "static" / "images"
for image_path in root.glob("*"):
    if image_path.is_dir() or image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.save(image_path, optimize=True, quality=75)
        print(f"Optimized {image_path.name}")
