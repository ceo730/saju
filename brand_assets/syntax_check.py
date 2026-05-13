"""generatePDF 함수만 추출해서 node --check로 문법 검증."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HTML = Path(r"c:\projects\subin\saju_repo\admin_page_version4.html")
text = HTML.read_text(encoding="utf-8")

m = re.search(
    r'(async function generatePDF\(.*?\}\s*\n)// ══ UI ══',
    text, re.DOTALL,
)
if not m:
    print("[FAIL] Could not locate generatePDF function block.")
    sys.exit(1)

js = m.group(1)
# generatePDF는 외부 함수 (loadImg, getImg, drawPaljaCard 등)를 참조하므로
# syntax-only 체크를 위해 dummy declarations 앞에 붙임
prelude = """
// dummy stubs for syntax check
const window = {jspdf: {jsPDF: function(){}}};
async function ensureJsPDF(){}
async function loadImg(){}
function getImg(){return "";}
function drawPaljaCard(){}
function drawBarChart(){}
function drawLineChart(){}
function genGraphData(){}
const SAJU_COLORS = {};
const IMG_BS_COVER = "", IMG_BS_INTRO = "", IMG_BS_ENDING = "";
const document = {createElement(){return {getContext(){return{};},toDataURL(){return "";},width:0,height:0};}};
"""

with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
    f.write(prelude + js)
    tmppath = f.name

print(f"Extracted generatePDF block: {len(js)} chars  → {tmppath}")
r = subprocess.run(["node", "--check", tmppath], capture_output=True, text=True)
if r.returncode == 0:
    print("[OK] generatePDF JavaScript syntax valid.")
else:
    print("[FAIL] Syntax error:")
    print(r.stderr)
    sys.exit(r.returncode)
