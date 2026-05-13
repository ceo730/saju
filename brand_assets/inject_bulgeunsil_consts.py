"""IMG_BS_* 상수 3개를 IMG_ENDING 라인 다음에 삽입합니다."""
import sys
from pathlib import Path

HTML = Path(r"c:\projects\subin\saju_repo\admin_page_version4.html")
SNIPPET = Path(r"c:\projects\subin\saju_repo\brand_assets\bulgeunsil\bulgeunsil_inline.js")

html_text = HTML.read_text(encoding="utf-8")
snippet = SNIPPET.read_text(encoding="utf-8").strip()

# 이미 삽입되었으면 중단 (idempotent)
if "IMG_BS_COVER" in html_text:
    print("[SKIP] IMG_BS_* already present in HTML.")
    sys.exit(0)

lines = html_text.split('\n')
out = []
inserted = False
for line in lines:
    out.append(line)
    if not inserted and line.startswith('const IMG_ENDING'):
        for sl in snippet.split('\n'):
            out.append(sl)
        inserted = True

if not inserted:
    print("[ERROR] IMG_ENDING line not found.")
    sys.exit(1)

HTML.write_text('\n'.join(out), encoding="utf-8")
print(f"[OK] Inserted {snippet.count(chr(10))+1} IMG_BS_* constants after IMG_ENDING.")
print(f"     HTML size: {HTML.stat().st_size/1024:.0f} KB")
