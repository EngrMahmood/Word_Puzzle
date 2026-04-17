from PIL import Image, ImageDraw, ImageFont
import os

RES_DIR = r"D:\word_puzzle\android\app\src\main\res"

APP_BLUE = (30, 58, 138, 255)      # #1E3A8A
WHITE = (255, 255, 255, 255)
GOLD = (250, 204, 21, 255)


def _load_bold_font(size: int):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "arialbd.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_master_icon(size: int = 1024) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Big circular base to keep icon legible even at 48x48.
    margin = int(size * 0.06)
    d.ellipse([margin, margin, size - margin, size - margin], fill=APP_BLUE)

    # Thick rounded tile shape.
    tile_size = int(size * 0.58)
    tx0 = (size - tile_size) // 2
    ty0 = int(size * 0.20)
    tx1 = tx0 + tile_size
    ty1 = ty0 + tile_size
    corner = int(size * 0.09)
    d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=corner, fill=WHITE)

    # Strong "WP" letters.
    font = _load_bold_font(int(size * 0.28))
    text = "WP"
    box = d.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.text(
        (size // 2 - tw // 2 - box[0], ty0 + tile_size // 2 - th // 2 - box[1]),
        text,
        fill=APP_BLUE,
        font=font,
    )

    # Small gold underline accent for puzzle branding.
    uy = int(size * 0.83)
    uw = int(size * 0.44)
    uh = max(8, int(size * 0.03))
    ux0 = (size - uw) // 2
    d.rounded_rectangle([ux0, uy, ux0 + uw, uy + uh], radius=uh // 2, fill=GOLD)

    return img


def save_launcher_icons(master: Image.Image) -> None:
    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    for folder, size in densities.items():
        out = os.path.join(RES_DIR, folder, "ic_launcher.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        master.resize((size, size), Image.Resampling.LANCZOS).save(out)
        print(f"updated {folder} -> {size}x{size}")


def save_splash(master: Image.Image) -> None:
    canvas_size = 1024
    splash = Image.new("RGBA", (canvas_size, canvas_size), WHITE)

    # Larger mark for startup readability.
    mark = master.resize((860, 860), Image.Resampling.LANCZOS)
    x = (canvas_size - mark.width) // 2
    y = (canvas_size - mark.height) // 2
    splash.paste(mark, (x, y), mark)

    out = os.path.join(RES_DIR, "drawable", "splash_logo.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    splash.convert("RGB").save(out)
    print("updated splash_logo.png -> 1024x1024 with larger centered mark")

    # Android 12+ splash API uses a centered icon resource; keep it tight and simple.
    splash_icon = master.resize((432, 432), Image.Resampling.LANCZOS)
    splash_icon_out = os.path.join(RES_DIR, "drawable", "splash_icon.png")
    splash_icon.save(splash_icon_out)
    print("updated splash_icon.png -> 432x432 for Android 12+ splash")


def main() -> None:
    master = build_master_icon(1024)
    master.save(r"D:\word_puzzle_logo_1024.png")
    save_launcher_icons(master)
    save_splash(master)
    print("done")


if __name__ == "__main__":
    main()

