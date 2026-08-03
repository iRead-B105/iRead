"""Generate deterministic runtime color variants from approved UI masters.

The app must consume real files for visual variants instead of applying CSS
filters at runtime. This script preserves the source alpha, dimensions and
geometry and shifts only saturated yellow frame pixels to the approved target
palette.
"""

from __future__ import annotations

import colorsys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHOICE_CARD_DIR = (
    ROOT / "services" / "frontend-app" / "src" / "assets" / "training" / "choice-cards"
)

TARGETS = {
    "mint": 0.455,
    "purple": 0.725,
}


def recolor_yellow_accents(source: Path, destination: Path, target_hue: float) -> None:
    image = Image.open(source).convert("RGBA")
    output = Image.new("RGBA", image.size)
    recolored: list[tuple[int, int, int, int]] = []

    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha == 0:
                recolored.append((red, green, blue, alpha))
                continue

            hue, lightness, saturation = colorsys.rgb_to_hls(
                red / 255,
                green / 255,
                blue / 255,
            )
            chroma = max(red, green, blue) - min(red, green, blue)
            is_yellow_accent = 0.08 <= hue <= 0.19 and chroma >= 22
            if not is_yellow_accent:
                recolored.append((red, green, blue, alpha))
                continue

            adjusted_saturation = min(0.62, max(0.42, saturation * 0.72))
            adjusted_lightness = min(lightness, 0.87 if chroma < 60 else 0.81)
            out_red, out_green, out_blue = colorsys.hls_to_rgb(
                target_hue,
                adjusted_lightness,
                adjusted_saturation,
            )
            recolored.append(
                (
                    round(out_red * 255),
                    round(out_green * 255),
                    round(out_blue * 255),
                    alpha,
                )
            )

    output.putdata(recolored)
    output.save(destination, optimize=True)


def create_sentence_variant(source: Path, destination: Path) -> None:
    """Create the approved 2:1 sentence-card asset from the 3:2 word-card source."""
    image = Image.open(source).convert("RGBA")
    sentence = image.resize((1024, 512), Image.Resampling.LANCZOS)
    sentence.save(destination, optimize=True)


def main() -> None:
    for shape in ("letter", "word"):
        source = CHOICE_CARD_DIR / f"choice-card-{shape}-yellow.png"
        if not source.exists():
            raise FileNotFoundError(f"Missing approved master: {source}")

        for color_name, hue in TARGETS.items():
            destination = CHOICE_CARD_DIR / f"choice-card-{shape}-{color_name}.png"
            recolor_yellow_accents(source, destination, hue)
            print(destination.relative_to(ROOT))

    for color_name in ("yellow", *TARGETS):
        source = CHOICE_CARD_DIR / f"choice-card-word-{color_name}.png"
        destination = CHOICE_CARD_DIR / f"choice-card-sentence-{color_name}.png"
        create_sentence_variant(source, destination)
        print(destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
