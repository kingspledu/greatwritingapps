from pathlib import Path
from playwright.sync_api import sync_playwright
B=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch()
 for name in ['great-writing-vocabulary.html','great-writing-tts.html']:
  page=b.new_page(viewport={'width':390,'height':844});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((B/name).as_uri())
  assert page.locator('.chapter-fold').count()==14
  for c in range(1,15):assert page.locator(f'[data-chapter="{c}"]').count()>0
  assert page.evaluate('DATA.reduce((n,g)=>n+g.words.length,0)')==2581
  page.locator('#chapter').select_option('14')
  page.locator('#open').click()
  assert page.locator('#c14-a6').is_visible()
  if 'tts' in name:
   assert page.locator('.answer').count()==0
   assert page.locator('#reveal').count()==0
   assert page.locator('.content table').count()==0
   page.evaluate('''() => {window.spoken=[];speechSynthesis.speak=u=>{spoken.push(u.text);setTimeout(()=>u.onend(),0)}}''')
   page.locator('#c14-a6 [data-word]').first.click()
   page.wait_for_function('spoken.length>0');assert page.evaluate('spoken[0]')=='boy'
   page.locator('#stop').click()
  else:assert '소년' in page.locator('#c14-a6').inner_text()
  page.locator('#search').fill('poison')
  assert page.locator('#c14-a6').is_visible()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(B/(name+'.png')),full_page=True)
  page.locator('#close').click();assert page.locator('details[open]').count()==0
  assert not errors,errors
  print(name,'14 chapters, 2581 entries, folding, search, mobile, TTS connection passed')
 b.close()
