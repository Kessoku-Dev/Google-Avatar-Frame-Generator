from __future__ import annotations

import argparse
import math
from pathlib import Path

# Safe GUI Import Fallback
try:
    from tkinter import Tk, filedialog
    HAS_GUI = True
except (ImportError, ModuleNotFoundError):
    HAS_GUI = False

from PIL import Image, ImageDraw, ImageOps


# Beautiful palettes aligning with the Web Application
PALETTES = {
    "classic": {
        "red": "#EA4335",
        "blue": "#4285F4",
        "yellow": "#FBBC05",
        "green": "#34A853",
    },
    "monochrome": {
        "red": "#1F2937",
        "blue": "#4B5563",
        "yellow": "#D1D5DB",
        "green": "#9CA3AF",
    },
    "neon": {
        "red": "#FF007F",
        "blue": "#00F0FF",
        "yellow": "#FFEF00",
        "green": "#39FF14",
    },
    "pastel": {
        "red": "#FFB3BA",
        "blue": "#BAE1FF",
        "yellow": "#FFFFBA",
        "green": "#BFFCC6",
    }
}

RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS

# Calibrated seam positions from the user's reference image.
# Pillow angles start at 3 o'clock and increase clockwise.
SEAMS = {
    "yellow_red": 206,
    "red_blue": 314,
    "blue_green": 48,
    "green_yellow": 138,
}

SEGMENTS = [
    ("red", SEAMS["yellow_red"], SEAMS["red_blue"]),
    ("blue", SEAMS["red_blue"], SEAMS["blue_green"]),
    ("green", SEAMS["blue_green"], SEAMS["green_yellow"]),
    ("yellow", SEAMS["green_yellow"], SEAMS["yellow_red"]),
]

DEFAULT_BORDER_RATIO = 0.04
DEFAULT_GAP_RATIO = 0.02


def pick_image_file() -> Path | None:
    """Prompts the user to pick an image file, using GUI filedialog if available, otherwise CLI input."""
    if HAS_GUI:
        try:
            root = Tk()
            root.withdraw()
            root.wm_attributes("-topmost", True)
            root.update()
            file_path = filedialog.askopenfilename(
                title="Choose an avatar image",
                filetypes=[
                    ("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp"),
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg;*.jpeg"),
                    ("All Files", "*.*"),
                ],
            )
            root.destroy()
            if file_path:
                return Path(file_path)
        except Exception:
            # Fall back to CLI prompt if tkinter throws any windows/display error
            pass

    print("\n--- CLI File Selector ---")
    while True:
        try:
            path_str = input("Please enter the path to your avatar image (or press Enter to exit): ").strip()
            if not path_str:
                return None
            path = Path(path_str)
            if path.exists() and path.is_file():
                return path
            print(f"Error: File '{path_str}' does not exist. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return None


def segment_span(start_angle: int, end_angle: int) -> int:
    return (end_angle - start_angle) % 360


def calculate_layout(output_size: int, border_ratio: float, gap_ratio: float) -> tuple[int, int]:
    if output_size < 32:
        raise ValueError("Output size must be at least 32.")

    border_width = max(1, round(output_size * border_ratio))
    gap = max(0, round(output_size * gap_ratio))
    return border_width, gap


def sample_point_for_angle(center: float, radius: float, angle_deg: float) -> tuple[int, int]:
    radians = math.radians(angle_deg)
    x = center + radius * math.cos(radians)
    y = center + radius * math.sin(radians)
    return round(x), round(y)


def draw_ring_segments(draw: ImageDraw.ImageDraw, arc_box: tuple[int, int, int, int], palette: str = "classic") -> None:
    colors = PALETTES.get(palette, PALETTES["classic"])
    for color_name, start_angle, end_angle in SEGMENTS:
        fill_color = colors[color_name]
        if end_angle < start_angle:
            draw.pieslice(arc_box, start=start_angle, end=360, fill=fill_color)
            draw.pieslice(arc_box, start=0, end=end_angle, fill=fill_color)
        else:
            draw.pieslice(arc_box, start=start_angle, end=end_angle, fill=fill_color)


def crop_and_zoom_avatar(
    source: Image.Image,
    target_diameter: int,
    zoom: float,
    offset_x: float,
    offset_y: float,
) -> Image.Image:
    """Crops, zooms and pans the avatar image to fit a square profile disk."""
    source = source.convert("RGBA")
    width, height = source.size
    min_dim = min(width, height)
    
    # Calculate crop size based on zoom scale (e.g. 1.0 = fit, 1.5 = zoom in)
    zoom = max(0.1, zoom) # Prevent division by zero
    crop_size = int(min_dim / zoom)
    
    # Adjust center coordinates with relative offsets (-0.5 to 0.5)
    center_x = width / 2 + (offset_x * width)
    center_y = height / 2 + (offset_y * height)
    
    # Determine bounding crop box
    left = center_x - crop_size / 2
    top = center_y - crop_size / 2
    right = center_x + crop_size / 2
    bottom = center_y + crop_size / 2
    
    # Crop (Pillow handles out of boundary values by filling transparently)
    cropped = source.crop((int(left), int(top), int(right), int(bottom)))
    
    # Resize to the final circular disk dimensions
    return cropped.resize((target_diameter, target_diameter), resample=RESAMPLE)


def build_avatar_canvas(
    source: Image.Image,
    output_size: int,
    border_width: int,
    gap: int,
    zoom: float = 1.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
    palette: str = "classic",
) -> Image.Image:
    avatar_diameter = output_size - (border_width + gap) * 2
    avatar = crop_and_zoom_avatar(source, avatar_diameter, zoom, offset_x, offset_y)

    avatar_mask = Image.new("L", (avatar_diameter, avatar_diameter), 0)
    mask_draw = ImageDraw.Draw(avatar_mask)
    mask_draw.ellipse((0, 0, avatar_diameter - 1, avatar_diameter - 1), fill=255)

    circular_avatar = Image.new("RGBA", (avatar_diameter, avatar_diameter), (0, 0, 0, 0))
    circular_avatar.paste(avatar, (0, 0), avatar_mask)

    canvas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
    ring_layer = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_layer)

    outer_ring_box = (0, 0, output_size - 1, output_size - 1)
    draw_ring_segments(ring_draw, outer_ring_box, palette)

    hole_margin = border_width
    ring_hole_box = (
        hole_margin,
        hole_margin,
        output_size - hole_margin - 1,
        output_size - hole_margin - 1,
    )
    ring_draw.ellipse(ring_hole_box, fill=(0, 0, 0, 0))

    canvas.alpha_composite(ring_layer)

    draw = ImageDraw.Draw(canvas)
    inner_disc_box = (
        border_width,
        border_width,
        output_size - border_width - 1,
        output_size - border_width - 1,
    )
    draw.ellipse(inner_disc_box, fill=(255, 255, 255, 255))

    avatar_offset = border_width + gap
    canvas.paste(circular_avatar, (avatar_offset, avatar_offset), circular_avatar)

    return canvas


def generate_google_style_avatar(
    input_path: Path,
    output_path: Path | None = None,
    output_size: int | None = None,
    border_ratio: float = DEFAULT_BORDER_RATIO,
    gap_ratio: float = DEFAULT_GAP_RATIO,
    zoom: float = 1.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
    palette: str = "classic",
) -> Path:
    with Image.open(input_path) as source:
        if output_size is None:
            output_size = min(source.size)

        border_width, gap = calculate_layout(output_size, border_ratio, gap_ratio)
        result = build_avatar_canvas(
            source=source,
            output_size=output_size,
            border_width=border_width,
            gap=gap,
            zoom=zoom,
            offset_x=offset_x,
            offset_y=offset_y,
            palette=palette
        )

    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}_google_frame.png")

    result.save(output_path)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Google-style color-ring avatar frame from a local image.",
    )
    parser.add_argument("input", nargs="?", help="Input avatar path. If omitted, a file picker is shown.")
    parser.add_argument("-o", "--output", help="Output PNG path. Defaults to the same folder as the input image.")
    parser.add_argument("-s", "--size", type=int, help="Output image size. Defaults to the shorter edge of the input image.")
    parser.add_argument("-b", "--border-ratio", type=float, default=DEFAULT_BORDER_RATIO, help=f"Ring width ratio (default: {DEFAULT_BORDER_RATIO})")
    parser.add_argument("-g", "--gap-ratio", type=float, default=DEFAULT_GAP_RATIO, help=f"White spacer gap ratio (default: {DEFAULT_GAP_RATIO})")
    parser.add_argument("-z", "--zoom", type=float, default=1.0, help="Avatar zoom factor (default: 1.0, zoom in > 1.0, zoom out < 1.0)")
    parser.add_argument("-x", "--offset-x", type=float, default=0.0, help="Horizontal offset ratio (-0.5 to 0.5, default: 0.0)")
    parser.add_argument("-y", "--offset-y", type=float, default=0.0, help="Vertical offset ratio (-0.5 to 0.5, default: 0.0)")
    parser.add_argument("-p", "--palette", choices=["classic", "monochrome", "neon", "pastel"], default="classic", help="Color palette to use (default: classic)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input) if args.input else pick_image_file()

    if input_path is None:
        print("No image selected. Exiting.")
        return

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = Path(args.output) if args.output else None
    saved_path = generate_google_style_avatar(
        input_path=input_path,
        output_path=output_path,
        output_size=args.size,
        border_ratio=args.border_ratio,
        gap_ratio=args.gap_ratio,
        zoom=args.zoom,
        offset_x=args.offset_x,
        offset_y=args.offset_y,
        palette=args.palette
    )
    print(f"Generated: {saved_path}")


if __name__ == "__main__":
    main()
