#!/usr/bin/env python3
"""Entry program for the make.fun bounty
"The Poster for a Place That Isn't There".

Reads entry.png from the repository root, validates it
(PNG/JPEG magic bytes, size <= 1_048_576 bytes, dimensions
<= 1024x1024 parsed from IHDR/SOF), copies it byte-for-byte
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output) and
verifies the copy with SHA-256.

Python standard library only. No network access.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def read_png_dimensions(data):
    """Return (width, height) from a PNG IHDR chunk."""
    if len(data) < 33:
        raise ValueError("PNG file too short for IHDR")
    if data[12:16] != b"IHDR":
        raise ValueError("PNG missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def read_jpeg_dimensions(data):
    """Return (width, height) from the first JPEG SOF marker."""
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            raise ValueError("JPEG marker scan lost sync")
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(data):
            raise ValueError("JPEG truncated at segment length")
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if length < 2:
            raise ValueError("JPEG segment length invalid")
        # SOF0-SOF15 except DHT(0xC4), JPG(0xC8), DAC(0xCC).
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            if pos + 9 > len(data):
                raise ValueError("JPEG SOF segment truncated")
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    raise ValueError("JPEG SOF marker not found")


def validate(data):
    """Validate magic bytes, size and dimensions. Return (fmt, w, h)."""
    if len(data) > MAX_BYTES:
        raise ValueError(
            "image is %d bytes, over the %d byte limit"
            % (len(data), MAX_BYTES)
        )
    if data.startswith(PNG_MAGIC):
        fmt = "PNG"
        width, height = read_png_dimensions(data)
    elif data.startswith(JPEG_MAGIC):
        fmt = "JPEG"
        width, height = read_jpeg_dimensions(data)
    else:
        raise ValueError("not a PNG or JPEG file (bad magic bytes)")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            "dimensions %dx%d exceed the %dx%d limit"
            % (width, height, MAX_DIMENSION, MAX_DIMENSION)
        )
    if width == 0 or height == 0:
        raise ValueError("image has a zero dimension")
    return fmt, width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png not found next to main.py: %s" % src)
    with open(src, "rb") as f:
        data = f.read()
    if not data:
        raise ValueError("entry.png is empty")

    fmt, width, height = validate(data)
    digest = hashlib.sha256(data).hexdigest()

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)

    with open(dst, "rb") as f:
        written = f.read()
    if len(written) != len(data):
        raise ValueError("size mismatch after copy: output corrupt")
    written_digest = hashlib.sha256(written).hexdigest()
    if written_digest != digest:
        raise ValueError("SHA-256 mismatch after copy: output corrupt")

    print("format: %s" % fmt)
    print("dimensions: %dx%d" % (width, height))
    print("size: %d bytes" % len(data))
    print("sha256: %s" % digest)
    print("wrote: %s (verified byte-for-byte)" % dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
