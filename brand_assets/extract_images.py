"""정통연구소 PDF 이미지 15장을 admin_page_version4.html에서 추출합니다."""
import re
import base64
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "admin_page_version4.html"
OUT = Path(__file__).resolve().parent / "jeongtong"
OUT.mkdir(parents=True, exist_ok=True)

KEYS = [
    "COVER", "TOC",
    "INTRO1", "INTRO2", "INTRO3", "INTRO4",
    "CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7",
    "NAEJI", "ENDING",
]

text = HTML.read_text(encoding="utf-8")

results = []
for key in KEYS:
    pat = re.compile(
        r'const\s+IMG_' + re.escape(key) +
        r'\s*=\s*"data:image/(jpeg|png|jpg);base64,([^"]+)"',
        re.IGNORECASE,
    )
    m = pat.search(text)
    if not m:
        results.append((key, None, 0))
        continue
    ext = m.group(1).lower()
    if ext == "jpg":
        ext = "jpeg"
    data = base64.b64decode(m.group(2))
    out_path = OUT / f"{key}.{ 'jpg' if ext=='jpeg' else ext }"
    out_path.write_bytes(data)
    results.append((key, out_path.name, len(data)))

print(f"{'KEY':<8} {'FILE':<14} {'SIZE(KB)':>10}")
print("-" * 36)
for key, fname, size in results:
    if fname:
        print(f"{key:<8} {fname:<14} {size/1024:>9.1f}")
    else:
        print(f"{key:<8} (NOT FOUND)")
