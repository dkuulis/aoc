import sys
import re

def _name(prefix: str) -> str:
    ext = ("." + prefix if prefix else "" ) + ".txt"
    filename = sys.argv[0].replace(".py", ext)
    return filename

def read_lines(prefix: str = "") -> list[list[str]]:
    filename = _name(prefix)

    with open(filename, 'r') as file:
        lines = file.readlines()

    return [line.rstrip("\n").rstrip("\r") for line in lines]

def read_content(prefix: str = "") -> list[list[str]]:
    filename = _name(prefix)

    with open(filename, 'r') as file:
        content = file.read().rstrip("\n").rstrip("\r")

    return content

def ints(d: dict) -> dict:
    for k, v in d.items():
        try:
            d[k] = int(v)
        except (ValueError, TypeError):
            pass # Leave the value unchanged if it can't be converted
    return d

def min_max(gen):
    try:
        first = next(gen)
    except StopIteration:
        raise ValueError("Generator is empty")

    min_val = max_val = first
    for val in gen:
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val

def save_bmp(data, filename, palette):
    """
    Save a 2D list of grayscale values (0-255) as a BMP image.
    """
    height = len(data)
    width = len(data[0])

    # Each pixel = 3 bytes (BGR)
    row_size = (width * 3 + 3) & ~3  # pad to multiple of 4
    pixel_array_size = row_size * height
    file_size = 54 + pixel_array_size

    with open(filename, "wb") as f:
        # BMP Header
        f.write(b"BM")
        f.write(file_size.to_bytes(4, "little"))
        f.write((0).to_bytes(4, "little"))  # reserved
        f.write((54).to_bytes(4, "little")) # pixel data offset

        # DIB Header (BITMAPINFOHEADER)
        f.write((40).to_bytes(4, "little")) # header size
        f.write(width.to_bytes(4, "little"))
        f.write(height.to_bytes(4, "little"))
        f.write((1).to_bytes(2, "little"))  # planes
        f.write((24).to_bytes(2, "little")) # bits per pixel
        f.write((0).to_bytes(4, "little"))  # compression
        f.write(pixel_array_size.to_bytes(4, "little"))
        f.write((2835).to_bytes(4, "little")) # horiz resolution
        f.write((2835).to_bytes(4, "little")) # vert resolution
        f.write((0).to_bytes(4, "little"))  # colors in palette
        f.write((0).to_bytes(4, "little"))  # important colors

        # Pixel data (bottom-up)
        for row in reversed(data):
            line = bytearray()
            for val in row:
                # grayscale → BGR triplet
                bgr = palette[val]
                line += bytes(bgr)
            # pad row to multiple of 4
            while len(line) < row_size:
                line += b"\x00"
            f.write(line)
