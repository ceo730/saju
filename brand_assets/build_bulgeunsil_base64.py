"""붉은실 PNG 3장을 JPEG로 변환 후 base64 data URL 스니펫을 생성합니다."""
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\Users\wnsgu\Downloads\붉은실")
OUT_DIR = Path(__file__).resolve().parent / "bulgeunsil"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_SNIPPET = OUT_DIR / "bulgeunsil_inline.js"

TARGET_W, TARGET_H = 893, 1263  # 정통연구소 INTRO1과 동일 (A4 비율)
QUALITY = 88

mapping = [
    ("앞.png", "IMG_BS_COVER"),
    ("소개.png", "IMG_BS_INTRO"),
    ("뒤.png", "IMG_BS_ENDING"),
]

snippets = []
for fname, varname in mapping:
    p = SRC / fname
    with Image.open(p) as im:
        rgb = im.convert("RGB").resize((TARGET_W, TARGET_H), Image.LANCZOS)
        # 검증용 jpg 파일 저장
        jpg_path = OUT_DIR / f"{varname.replace('IMG_BS_', '').lower()}.jpg"
        rgb.save(jpg_path, format="JPEG", quality=QUALITY)
        buf = BytesIO()
        rgb.save(buf, format="JPEG", quality=QUALITY)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        size_kb = len(buf.getvalue()) / 1024
        snippet = f'const {varname} = "data:image/jpeg;base64,{b64}";'
        snippets.append(snippet)
        print(f"{varname:<18} {jpg_path.name:<14} {size_kb:>7.1f} KB   b64 len={len(b64):,}")

OUT_SNIPPET.write_text("\n".join(snippets), encoding="utf-8")
print(f"\nSnippet saved: {OUT_SNIPPET}")
print(f"Total snippet size: {OUT_SNIPPET.stat().st_size/1024:.1f} KB")
