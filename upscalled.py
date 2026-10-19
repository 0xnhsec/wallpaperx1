#!/usr/bin/env python3
"""
scale_png.py - scale gambar format apa pun -> PNG. Tanpa AI (resampling klasik).

Install:  pip install pillow            (opsional: pip install pillow-heif  untuk HEIC/HEIF)

Contoh:
  python scale_png.py foto.jpg -s 2                 # 2x
  python scale_png.py foto.webp -w 1280             # lebar 1280, rasio dijaga
  python scale_png.py folder/ -r -w 800 -o hasil/   # satu folder, rekursif
  python scale_png.py a.bmp -w 512 -H 512 --fit     # muat di 512x512, rasio dijaga
  python scale_png.py foto.jpg -w 3000 --sharpen 100 # + unsharp mask
  python scale_png.py a.bmp -w 512 -H 512           # paksa 512x512 (bisa distorsi)
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

try:  # opsional
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

RESAMPLE = {
    "nearest": Image.Resampling.NEAREST,
    "box": Image.Resampling.BOX,
    "bilinear": Image.Resampling.BILINEAR,
    "hamming": Image.Resampling.HAMMING,
    "bicubic": Image.Resampling.BICUBIC,
    "lanczos": Image.Resampling.LANCZOS,
}


def compute_size(w, h, a):
    if a.scale:
        return max(1, round(w * a.scale)), max(1, round(h * a.scale))
    if a.width and a.height:
        if a.fit:
            r = min(a.width / w, a.height / h)
            return max(1, round(w * r)), max(1, round(h * r))
        return a.width, a.height
    if a.width:
        return a.width, max(1, round(h * a.width / w))
    if a.height:
        return max(1, round(w * a.height / h)), a.height
    raise ValueError("Tentukan -s, -w, atau -H")


def normalize(im):
    """Jadikan mode yang aman untuk resize + simpan PNG, alpha dipertahankan."""
    if im.mode in ("RGB", "RGBA", "L", "LA"):
        return im
    has_alpha = "A" in im.getbands() or "transparency" in im.info
    return im.convert("RGBA" if has_alpha else "RGB")


def sharpen(im, a):
    """Unsharp mask hanya di kanal warna; alpha dibiarkan agar tepi transparan tidak rusak."""
    f = ImageFilter.UnsharpMask(radius=a.radius, percent=a.sharpen, threshold=a.threshold)
    if im.mode in ("RGBA", "LA"):
        alpha = im.getchannel("A")
        out = im.convert("RGB" if im.mode == "RGBA" else "L").filter(f)
        out.putalpha(alpha)
        return out
    return im.filter(f)


def process(src: Path, dst: Path, a):
    with Image.open(src) as im:
        im.seek(0)                       # animasi (GIF/WebP/APNG): ambil frame pertama
        im = ImageOps.exif_transpose(im)  # hormati orientasi EXIF
        im = normalize(im)
        size = compute_size(*im.size, a)
        out = im.resize(size, RESAMPLE[a.resample])
        if a.sharpen:
            out = sharpen(out, a)
        dst.parent.mkdir(parents=True, exist_ok=True)
        out.save(dst, format="PNG", optimize=a.optimize)
    return size


def collect(inputs, recursive):
    for p in map(Path, inputs):
        if p.is_dir():
            it = p.rglob("*") if recursive else p.glob("*")
            for f in sorted(it):
                if f.is_file():
                    yield f, p
        elif p.is_file():
            yield p, p.parent
        else:
            print(f"[skip] tidak ditemukan: {p}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Scale gambar apa pun ke PNG (non-AI).")
    ap.add_argument("inputs", nargs="+", help="file atau folder")
    ap.add_argument("-o", "--outdir", default="out", help="folder output (default: out)")
    ap.add_argument("-s", "--scale", type=float, help="faktor skala, mis. 2 atau 0.5")
    ap.add_argument("-w", "--width", type=int, help="lebar target (px)")
    ap.add_argument("-H", "--height", type=int, help="tinggi target (px)")
    ap.add_argument("--fit", action="store_true", help="jika -w & -H diberikan, jaga rasio (muat di dalam kotak)")
    ap.add_argument("-r", "--recursive", action="store_true", help="telusuri subfolder")
    ap.add_argument("--resample", choices=RESAMPLE, default="lanczos", help="algoritma (default: lanczos)")
    ap.add_argument("--sharpen", type=int, default=0, metavar="PERCENT",
                    help="unsharp mask setelah resize, mis. 80-150 (default 0 = mati)")
    ap.add_argument("--radius", type=float, default=1.0, help="radius unsharp mask (default 1.0)")
    ap.add_argument("--threshold", type=int, default=3, help="threshold unsharp mask (default 3)")
    ap.add_argument("--optimize", action="store_true", help="kompres PNG lebih keras (lebih lambat)")
    a = ap.parse_args()

    if a.scale and (a.width or a.height):
        ap.error("-s tidak bisa digabung dengan -w/-H")
    if not (a.scale or a.width or a.height):
        ap.error("butuh salah satu: -s, -w, atau -H")
    if a.scale is not None and a.scale <= 0:
        ap.error("-s harus > 0")

    outdir = Path(a.outdir)
    ok = fail = 0
    used = set()
    for f, root in collect(a.inputs, a.recursive):
        rel = f.relative_to(root).with_suffix(".png")
        dst = outdir / rel
        if dst in used:  # a.jpg & a.gif -> a.png bakal saling timpa
            dst = dst.with_name(f"{f.stem}_{f.suffix.lstrip('.').lower()}.png")
        used.add(dst)
        try:
            if dst.resolve() == f.resolve():
                print(f"[skip] output = input: {f}", file=sys.stderr)
                continue
            size = process(f, dst, a)
            print(f"[ok]   {f} -> {dst} {size[0]}x{size[1]}")
            ok += 1
        except Exception as e:  # bukan gambar / korup / format tak didukung
            print(f"[fail] {f}: {e}", file=sys.stderr)
            fail += 1
    print(f"selesai: {ok} ok, {fail} gagal")
    return 1 if fail and not ok else 0


if __name__ == "__main__":
    sys.exit(main())
