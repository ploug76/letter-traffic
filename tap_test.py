import random,sys
from playwright.sync_api import sync_playwright
LN='ay bee see dee ee eff gee aitch eye jay kay el em en oh pee cue ar ess tee you vee double-you ex why zee'.split()
def tolet(s):
  s=s.strip().rstrip('.').lower()
  return chr(97+LN.index(s)) if s in LN else s
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':390,'height':760},device_scale_factor=2.625,is_mobile=True,has_touch=True)
  pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.add_init_script("window.LOG=[];speechSynthesis.speak=u=>LOG.push(u.text)")
  pg.goto(sys.argv[1]);pg.evaluate("localStorage.setItem('ltClass',JSON.stringify({kids:[{id:'x',name:'HAL',fry:[1,1,0,0],pic:true,custom:[],speed:'med',prog:{},stars:0}]}))");pg.reload();pg.wait_for_timeout(300)
  pg.tap('.kb');pg.wait_for_timeout(300)
  # CSS scale check
  print('css vs canvas',pg.evaluate("(()=>{const r=c.getBoundingClientRect();return [r.width,r.height,W/DPR,H/DPR]})()"))
  S=pg.evaluate("S");DPR=pg.evaluate("DPR");lanesY=pg.evaluate("lanes()")
  tot=bad=0;fails=[]
  for trial in range(int(sys.argv[3]) if len(sys.argv)>3 else 40):
    cars=[]
    for l in range(4):
      xs=sorted(random.sample(range(40,360,10),random.randint(1,3)))
      for xx in xs:
        if cars and cars[-1]['l']==l and xx-cars[-1]['xc']<(100):continue
        ch=chr(random.choice([65,97])+random.randrange(26));cars.append({'l':l,'xc':xx,'ch':ch,'bus':random.random()<.35})
    js=[{'x':k['xc']*DPR,'d':(1 if k['l']%2 else -1),'l':k['l'],'y':lanesY[k['l']],'ch':k['ch'],'col':'#f0f','bus':k['bus'],'sp':0,'wob':0} for k in cars]
    pg.evaluate("cs=>{state='play';spawnT=1e9;word='########';idx=0;cars=cs}",js);pg.wait_for_timeout(60)
    order=sorted(range(len(cars)),key=lambda i:cars[i]['l'])  # draw order (stable)
    def geom(k):
      w=(120 if k['bus'] else 95)*S;h=(50 if k['bus'] else 38)*S;X=k['xc']*DPR;Y=lanesY[k['l']]
      return X,Y,w,h,Y-h*1.3-26*S
    def contains(k,px,py):
      X,Y,w,h,ly=geom(k)
      return ((px-X)**2+(py-ly)**2)**.5<=26*S or (abs(px-X)<=w/2 and Y-h*1.3<=py<=Y)
    for i,k in enumerate(cars):
      X,Y,w,h,ly=geom(k)
      for (px,py,tag) in [(X,ly,'letter'),(X+16*S,ly,'letterR'),(X-16*S,ly,'letterL'),(X,ly-16*S,'letterT'),(X,ly+16*S,'letterB'),(X,Y-h*.6,'body'),(X-w*.4,Y-h*.4,'bodyL'),(X+w*.4,Y-h*.4,'bodyR')]:
        if not(2<px/DPR<388 and 2<py/DPR<758):continue
        exp=None
        for j in reversed(order):
          if contains(cars[j],px,py):exp=cars[j]['ch'];break
        if exp is None:continue
        n=pg.evaluate("LOG.length");pg.touchscreen.tap(px/DPR,py/DPR);pg.wait_for_timeout(90)
        lg=pg.evaluate("LOG.slice(%d)"%n);got=tolet(lg[-1]) if lg else None
        tot+=1
        if got!=exp.lower():bad+=1;fails.append((tag,k["l"],k["xc"],k["bus"],exp,got,pg.evaluate("([a,b])=>{const q=hitAt(a,b);return q&&[q.ch,q.l,q.x/DPR,q.bus]}",[px,py])))
        pg.evaluate("cs=>{cars=cs;idx=0}",js);pg.wait_for_timeout(120)
  print('taps',tot,'wrong',bad,'errors',errs);[print(f) for f in fails[:12]]
  from collections import Counter;print(Counter(f[0] for f in fails))
