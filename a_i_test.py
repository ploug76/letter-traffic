from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':760},device_scale_factor=2.625,is_mobile=True,has_touch=True)
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.add_init_script("window.LOG=[];speechSynthesis.speak=u=>LOG.push(u.text)")
  pg.goto('http://localhost:8765/');pg.evaluate("localStorage.setItem('ltClass',JSON.stringify({kids:[{id:'x',name:'IAN',fry:[1,1,1,1],pic:true,custom:[],speed:'med',prog:{},stars:0}]}))");pg.reload();pg.wait_for_timeout(300)
  pg.tap('.kb');pg.wait_for_timeout(300);DPR=pg.evaluate('DPR')
  def tapch(ch,lane):
    pg.evaluate("([ch,l])=>{spawnT=1e9;cars=[{x:200*DPR,d:l%2?1:-1,l,y:lanes()[l],ch,col:'#f0f',bus:false,sp:0,wob:0}]}",[ch,lane]);pg.wait_for_timeout(80)
    y=pg.evaluate("cars[0].g.ly/DPR");n=pg.evaluate('LOG.length');pg.touchscreen.tap(200,y);pg.wait_for_timeout(100);return pg.evaluate("LOG.slice(%d)"%n)
  bad=[]
  def play(W,isname=False):
    if not isname:pg.evaluate("w=>{state='play';setWord(w,'');}",W)
    word=pg.evaluate('word')
    # also wrong taps: a when needing i and vice versa
    for i,ch in enumerate(word):
      wrong={'a':'i','i':'a','A':'I','I':'A'}.get(ch)
      if wrong:
        sp=tapch(wrong,i%4);
        if pg.evaluate('idx')!=i:bad.append(('wrong filled',W,ch,wrong))
        if sp[-1:]!=[ {'a':'a.'}.get(wrong.lower(),wrong.lower())]:bad.append(('wrongspeech',wrong,sp))
      sp=tapch(ch,(i+1)%4)
      if pg.evaluate('idx')!=i+1:bad.append(('no fill',W,i,ch))
      if not sp or sp[0]!={'a':'a.'}.get(ch.lower(),ch.lower()):bad.append(('speech',ch,sp))
    pg.wait_for_timeout(50);return word,pg.evaluate("state")
  print(play(None,True))
  for W in ['A','I','AND','IS','IT','HAVE','SAID','THEIR','AM','IF','CAT','MAP','PIG','WAS','IN','AN']:
    w,st=play(W);
    if st!='celeb':bad.append(('nocomplete',W))
    pg.evaluate("celebT=0")
  prog=pg.evaluate("DB.kids[0].prog");print(prog)
  for W in ['A','I','AND','IS']:
    if prog.get(W)!=1:bad.append(('prog',W,prog.get(W)))
  if any(k not in ['A','I','AND','IS','IT','HAVE','SAID','THEIR','AM','IF','CAT','MAP','PIG','WAS','IN','AN'] for k in prog):bad.append(('extra prog',prog))
  print('words',pg.evaluate("[(setWord('I',''),word),(setWord('A',''),word)]"))
  pg.evaluate("state='play';setWord('I','');cars=[{x:120*DPR,d:-1,l:1,y:lanes()[1],ch:'I',col:'#f0f',bus:false,sp:0,wob:0},{x:280*DPR,d:-1,l:1,y:lanes()[1],ch:'L',col:'#0cf',bus:false,sp:0,wob:0}];spawnT=1e9");pg.wait_for_timeout(200);pg.screenshot(path='/workspace/letter-traffic/i-letter.png')
  print('bad',bad,'errors',errs)
