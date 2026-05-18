// 시뮬레이션 가정값과 실제 calcSaju 결과 비교 스크립트
const { calcSaju, buildSipsungContext, CH_HJ, JI_HJ } = require('./calc_saju.js');

const people = [
  { name: '이서연', y: 1990, m: 3,  d: 15, h: 9,  mn: 0, assumed: '庚午 己卯 戊辰 丁巳' },
  { name: '강남경', y: 1999, m: 10, d: 1,  h: 13, mn: 0, assumed: '己卯 癸酉 庚子 癸未' },
  { name: '박준석', y: 1999, m: 1,  d: 18, h: 14, mn: 0, assumed: '戊寅 乙丑 乙未 癸未' },
  { name: '이하경', y: 2001, m: 2,  d: 5,  h: 11, mn: 0, assumed: '辛巳 庚寅 壬午 乙巳' },
];

function pillarsString(saju){
  return saju.pillars.filter(Boolean).map(p=>p.stem+p.branch).join(' ');
}

function ohengCounts(oh){
  return `목${oh['목']} 화${oh['화']} 토${oh['토']} 금${oh['금']} 수${oh['수']}`;
}

let match = 0, mismatch = 0;
const results = [];

for(const p of people){
  const saju = calcSaju(p.y, p.m, p.d, p.h, p.mn);
  const actual = pillarsString(saju);
  const eq = actual === p.assumed;
  if(eq) match++; else mismatch++;

  // 어느 기둥이 다른지 분석
  const aPart = actual.split(' ');
  const eParts = p.assumed.split(' ');
  const diffLabels = [];
  ['年','月','日','時'].forEach((lbl, i) => {
    if(aPart[i] !== eParts[i]) diffLabels.push(`${lbl}(실제 ${aPart[i]} vs 가정 ${eParts[i]})`);
  });

  results.push({
    name: p.name, ymd: `${p.y}-${String(p.m).padStart(2,'0')}-${String(p.d).padStart(2,'0')} ${String(p.h).padStart(2,'0')}:${String(p.mn).padStart(2,'0')}`,
    actualHanja: actual,
    ilgan: saju.ilgan,
    pillarsKr: saju.pillars.filter(Boolean).map(x=>x.stemKr+x.branchKr).join(' '),
    pillarsOh: saju.pillars.filter(Boolean).map(x=>`${x.stemOh}/${x.branchOh}`).join(' '),
    oheng: ohengCounts(saju.oheng),
    assumed: p.assumed,
    match: eq,
    diffLabels,
    sipsungLine: buildSipsungContext(saju).split('\n')[1] // "오행별 십성:" 줄
  });
}

console.log('='.repeat(70));
for(const r of results){
  console.log(`\n[${r.name} ${r.ymd}]`);
  console.log(`  실제 계산: ${r.actualHanja} (일간 ${r.ilgan})`);
  console.log(`  한글     : ${r.pillarsKr}`);
  console.log(`  오행기둥 : ${r.pillarsOh}`);
  console.log(`  오행분포 : ${r.oheng}`);
  console.log(`  가정 값  : ${r.assumed}`);
  console.log(`  일치 여부: ${r.match ? '✅ 일치' : '❌ 불일치 → ' + r.diffLabels.join(', ')}`);
  console.log(`  ${r.sipsungLine}`);
}
console.log('\n' + '='.repeat(70));
console.log(`종합: ${match}/4 일치, ${mismatch}/4 불일치`);
