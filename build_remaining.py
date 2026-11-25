import json,re
from pathlib import Path
B=Path(__file__).parent
groups=[];titles={4:'Nouns',5:'Pronouns',6:'Adjectives',7:'The Conjunction And'}
for line in (B/'remaining-wordlists.txt').read_text(encoding='utf-8').splitlines():
 if line.startswith('['):
  c,title,page,a,sound=line[1:-1].split('|');c=int(c);titles[c]=title
  g=dict(chapter=c,activity=int(a),title=f'Words to Know · {sound}',label='Words to Know',source=f'교재 {page}쪽',page=page,grammar=False,tables=[],note='PDF의 Words to Know 전체 목록을 철자 그룹 순서로 정리했습니다.',words=[]);groups.append(g)
 elif line.strip():
  e,k=line.split('|',1);g['words'].append(dict(english=e,korean=k))
for line in (B/'remaining-supplement.txt').read_text(encoding='utf-8').splitlines():
 if line.startswith('['):
  c,a,title,page,kind=line[1:-1].split('|');g=dict(chapter=int(c),activity=int(a),title=title,label=title,source=f'교재 {page}쪽',page=page,grammar=kind=='grammar',tables=[],note='원문에서 단어·청크만 정리했습니다. 같은 묶음 안의 중복 표현은 한 번만 수록합니다.',words=[]);groups.append(g)
 elif line.strip():
  e,k=line.split('|',1);g['words'].append(dict(english=e,korean=k))
for g in groups:
 seen=set();g['words']=[w for w in g['words'] if not (w['english'].lower() in seen or seen.add(w['english'].lower()))]
 assert g['words']
 assert all(not re.search(r'[.!?]',w['english']) for w in g['words'])
 if g['grammar']:assert all(' ' not in w['english'] for w in g['words'])
groups.sort(key=lambda g:(g['chapter'],int(re.match(r'\d+',g['page'])[0]),g['activity']))
(B/'remaining-units-data.js').write_text('const REMAINING_UNITS = '+json.dumps(groups,ensure_ascii=False,indent=2)+';\nconst UNIT_TITLES = '+json.dumps(titles,ensure_ascii=False)+';\n',encoding='utf-8')
for name in ['great-writing-vocabulary.html','great-writing-tts.html']:
 p=B/name;s=p.read_text(encoding='utf-8-sig')
 s=s.replace('<script src="chapter7-data.js"></script>','<script src="chapter7-data.js"></script><script src="remaining-units-data.js"></script>')
 s=s.replace('DATA.push(...CHAPTER6,...CHAPTER7)','DATA.push(...CHAPTER6,...CHAPTER7,...REMAINING_UNITS)')
 s=s.replace('for(const c of [4,5,6,7])','for(const c of Array.from({length:14},(_,i)=>i+1))')
 s=s.replace("${{4:'Nouns',5:'Pronouns',6:'Adjectives',7:'The Conjunction And'}[c]}",'${UNIT_TITLES[c]}')
 s=re.sub(r'<select id="chapter">.*?</select>','<select id="chapter"><option value="all">전체</option>'+''.join(f'<option value="{i}">Chapter {i}</option>' for i in range(1,15))+'</select>',s)
 s=s.replace('CHAPTERS 4–7','CHAPTERS 1–14').replace('Chapter 4–7','Chapter 1–14')
 s=re.sub(r'<div class="stats">.*?</div>','<div class="stats" id="stats"></div>',s)
 s=s.replace("const root=document.getElementById('activities');", "document.getElementById('stats').innerHTML=`<span>14 Chapters</span><span>${DATA.length} 학습 묶음</span><span>${DATA.reduce((n,g)=>n+g.words.length,0)} 단어·표현</span>`;const root=document.getElementById('activities');")
 s=s.replace("${g.grammar?'문법 해설':'Activity '+g.activity}","${g.label|| (g.grammar?'문법 해설':'Activity '+g.activity)}")
 s=s.replace('const label=`${g.activity}-${i+1}`','const label=`${g.label?g.chapter+\'-\'+g.activity:g.activity}-${i+1}`')
 s=s.replace('Chapter 4·5 이미지 및 Unit 6·7 PDF 원문 기반','Great Writing Foundations Unit 1~14 원문 기반')
 s=s.replace('Unit 6 Activity 11·Unit 7 Activity 12는 음원·정답이 없어 제외했습니다.','음원과 정답 없이 확인할 수 없는 받아쓰기 단어는 임의로 추가하지 않았습니다.')
 p.write_text(s,encoding='utf-8')
print(f'{len(groups)} new groups, {sum(len(g["words"]) for g in groups)} new words/chunks')
