#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered front page to the output directory.

The front page (entry.png, 1024x1024) is rendered at build time by
render.py from news.json. This entrypoint only copies it and verifies
it is a well-formed PNG within the competition limits. Stdlib only,
no network, deterministic.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def fail(msg):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    if not os.path.isfile(SRC):
        fail("entry.png missing next to main.py")

    with open(SRC, "rb") as fh:
        data = fh.read()

    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a PNG file")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        fail("entry.png is %dx%d, over the 1024x1024 limit" % (width, height))

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # Confirm the copy on disk matches the verified source byte for byte.
    with open(dst, "rb") as fh:
        copied = fh.read()
    if copied != data:
        fail("copied file differs from verified source")
    digest = hashlib.sha256(data).hexdigest()
    print("copied %s -> %s (%dx%d, %d bytes, sha256 %s)"
          % (SRC, dst, width, height, len(data), digest))


if __name__ == "__main__":
    main()
