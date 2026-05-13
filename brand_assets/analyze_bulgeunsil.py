"""붉은실 이미지 크기·비율 분석"""
from PIL import Image
from pathlib import Path

SRC = Path(r"C:\Users\wnsgu\Downloads\붉은실")
files = ["앞.png", "소개.png", "뒤.png"]

# A4 portrait = 595.28 x 841.89 pt (ratio 1.414)
A4_RATIO = 841.89 / 595.28

# 정통연구소 비교용
JT = Path(r"c:\projects\subin\saju_repo\brand_assets\jeongtong")
for fname in ["COVER.jpg", "INTRO1.jpg", "ENDING.jpg"]:
    with Image.open(JT / fname) as im:
        ratio = im.height / im.width
        size_kb = (JT / fname).stat().st_size / 1024
        print(f"[정통] {fname:<14} {im.width}x{im.height} ratio={ratio:.3f} size={size_kb:.0f}KB")

print(f"\nA4 portrait ratio = {A4_RATIO:.3f}\n")

for fname in files:
    p = SRC / fname
    with Image.open(p) as im:
        ratio = im.height / im.width
        size_kb = p.stat().st_size / 1024
        # JPEG quality 88로 변환 시 예상 크기 추정
        from io import BytesIO
        # A4 비율로 맞추기 위한 리사이즈 시뮬레이션
        # 정통이 893x1263이니까 동일 사이즈로 맞춤
        target_w = 893
        target_h = round(target_w * A4_RATIO)
        resized = im.convert("RGB").resize((target_w, target_h), Image.LANCZOS)
        buf = BytesIO()
        resized.save(buf, format="JPEG", quality=88)
        compressed_kb = len(buf.getvalue()) / 1024
        print(f"[붉은실] {fname:<10} 원본 {im.width}x{im.height} ratio={ratio:.3f} size={size_kb:.0f}KB → 893x{target_h} JPEG q88: {compressed_kb:.0f}KB")
