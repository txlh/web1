"""Download the imageio-ffmpeg wheel straight from PyPI and unpack it.

Used because `pip install` cannot write into its own temp dirs under the
agent sandbox; a plain urllib download + zipfile extraction needs no pip.
"""
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

TARGET = Path(r"D:\deepseek2\.pylibs")
CACHE = Path(r"D:\deepseek2\.pip-cache")
CACHE.mkdir(parents=True, exist_ok=True)
TARGET.mkdir(parents=True, exist_ok=True)


def main() -> int:
    print("querying PyPI ...")
    with urllib.request.urlopen("https://pypi.org/pypi/imageio-ffmpeg/json", timeout=60) as r:
        meta = json.load(r)

    version = meta["info"]["version"]
    wheel = next(
        (u for u in meta["urls"] if u["filename"].endswith("win_amd64.whl")),
        None,
    )
    if wheel is None:
        print("no win_amd64 wheel for", version)
        return 1

    dest = CACHE / wheel["filename"]
    if not dest.exists():
        print(f"downloading {wheel['filename']} ({wheel['size'] / 1024 / 1024:.1f} MB)")
        with urllib.request.urlopen(wheel["url"], timeout=300) as r, dest.open("wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
    else:
        print("using cached", dest.name)

    print("unpacking to", TARGET)
    with zipfile.ZipFile(dest) as z:
        z.extractall(TARGET)

    print("version:", version)
    for p in sorted(TARGET.glob("imageio_ffmpeg/binaries/*")):
        print(f"  {p.name}  {p.stat().st_size / 1024 / 1024:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
