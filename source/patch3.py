# patch3: move Portfolio + sample-site wall to /work/, leave a 3-card teaser on home.
# Run after build.py, patch.py, patch2.py:  python3 patch3.py index.html  (writes index.html and work/index.html)
import sys,re
fn=sys.argv[1];s=open(fn).read()
if 'id="feat"' in s: sys.exit('already patched')
# shared fixes (both pages)
s=s.replace('url(work.webp)','url(/work.webp)').replace('url(ba.webp)','url(/ba.webp)')
CSS=r'''
/* featured teaser */
.feat{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;list-style:none;margin:0;padding:0}
.feat a{display:block;text-decoration:none;background:var(--card);border:1px solid var(--rule);border-radius:12px;overflow:hidden;transition:transform .3s,box-shadow .3s}
.feat .img{display:block;aspect-ratio:16/10;border-bottom:1px solid var(--rule)}
.feat .t{display:block;padding:16px 18px 18px}.feat h3{font-size:24px;line-height:1.1}.feat p{margin:6px 0 0;color:var(--mut);font-size:14.5px}
.feat .st{display:block;margin-top:10px;font:12px var(--mono);color:var(--mut)}
@media (hover:hover){.feat a:hover{transform:translateY(-4px);box-shadow:0 24px 40px -28px rgba(40,30,10,.5)}.feat a:hover h3{color:var(--acc)}}
.more{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-top:26px}
.more a.btn{white-space:nowrap}
.wp-hd{padding-top:150px}
@media (max-width:899px){.feat{grid-template-columns:1fr;gap:12px}.feat a{display:grid;grid-template-columns:118px 1fr;align-items:center;padding:8px 0 8px 8px}.feat .img{width:118px;aspect-ratio:16/10;border-bottom:0;border-right:1px solid var(--rule)}.feat .t{padding:12px 14px}.feat h3{font-size:19px}.feat p{font-size:13.5px}.feat .st{display:none}.wp-hd{padding-top:110px}}
'''
s=s.replace('@media (prefers-reduced-motion:reduce)',CSS+'@media (prefers-reduced-motion:reduce)',1)
# JS guards so one script runs on both pages
R=[("const d=document.getElementById('date');d.textContent=","const d=document.getElementById('date');if(d)d.textContent="),
("tick();setInterval(tick,30000);","if(document.getElementById('acc')){tick();setInterval(tick,30000)}"),
("if(!RM){let w=0","if(!RM&&el){let w=0"),
("document.getElementById('chips').addEventListener","document.getElementById('chips')?.addEventListener"),
("rg=ba.querySelector('input');rg.addEventListener","rg=ba&&ba.querySelector('input');rg&&rg.addEventListener"),
("rail.addEventListener(","rail&&rail.addEventListener("),
("cp.addEventListener(","cp&&cp.addEventListener("),
("links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')=='#'+id))","links.forEach(a=>a.classList.toggle('on',(a.dataset.s||a.getAttribute('href'))=='#'+id))"),
("document.querySelectorAll('main section').forEach(s=>so.observe(s));","if(!document.body.classList.contains('wpage'))document.querySelectorAll('main section').forEach(s=>so.observe(s));")]
for a,b in R:
    assert a in s,a; s=s.replace(a,b)
# carve out sections
a=s.index('<section id="portfolio">');b=s.index('</div></section>',a)+len('</div></section>');PORT=s[a:b]
c=s.index('<section id="concepts">');e=s.index('</section>',c)+len('</section>');CON=s[c:e]
w0=CON.index(' <div class="wrap"><div class="wall');WALL=CON[w0:CON.rindex('</section>')]
SLIDER=CON[:w0]
rows=re.findall(r'<li class="prow".*?</li>',PORT)
def card(r):
    href=re.search(r'href="([^"]+)"',r).group(1);h=re.search(r'<h3>(.*?)</h3>',r).group(1);p=re.sub(r'<span class="tag.*?</span>','',re.search(r'<p>(.*?)</p>',r).group(1))
    st=re.search(r'class="st">(.*?)</span>',r).group(1);y=re.search(r'data-y="([^"]+)"',r).group(1)
    return f'<li><a href="{href}"><span class="img spr" style="background-position:0 {y}" role="img" aria-label="Screenshot of {h}"></span><span class="t"><h3>{h}</h3><p>{p}</p><span class="st">{st}</span></span></a></li>'
TEASER=('<section id="portfolio"><div class="wrap">\n <div class="sh rv"><span class="mono"><b>04</b> / Portfolio</span><div><h2>Selected work.</h2><p class="lead" style="margin-top:16px">A few recent projects. The full list, with the sample sites, is on the work page.</p></div></div>\n'
 ' <ul class="feat rv" id="feat">'+''.join(card(r) for r in rows[:3])+'</ul>\n'
 f' <div class="more rv"><span class="mono">{len(rows)} projects · 15 sample sites</span><a class="btn solid" href="/work/">See all work →</a></div>\n</div></section>')
SLIDER_H=SLIDER.replace('Drag the handle.</p>','Drag the handle.</p>').replace('</p>\n</div>','</p>\n <div class="more"><span></span><a class="btn ghost" href="/work/#samples">See all 15 sample sites →</a></div>\n</div>')
home=s[:a]+TEASER+s[b:c]+SLIDER_H+'</section>'+s[e:]
NAV_OLD='<a href="#portfolio"><span class="n">04</span>Portfolio</a>'
home=home.replace(NAV_OLD,'<a href="/work/" data-s="#portfolio"><span class="n">04</span>Portfolio</a>')
home=home.replace('<a class="btn solid" href="#portfolio">View my work</a>','<a class="btn solid" href="/work/">View my work</a>')
open(fn,'w').write(home)
# work page
h0=s.index('<main id="main">')+len('<main id="main">');h1=s.index('</main>')
PORT_W=PORT.replace('<span class="mono"><b>04</b> / Portfolio</span><div><h2>Selected work.</h2>','<span class="mono"><b>04</b> / Portfolio</span><div><h1 class="h2">Selected work.</h1>',1)
PORT_W=PORT_W.replace('<section id="portfolio">','<section id="portfolio" class="wp-hd">',1)
SAMP=('<section id="samples"><div class="wrap">\n <div class="sh rv"><span class="mono">Concept work</span><div><h2>Sample sites / concepts.</h2><p class="lead" style="margin-top:16px">On the side, I build sample sites for small US service businesses that don\'t have one yet, so the owner can see what theirs could look like. Each one has a short case study.</p></div></div>\n</div>\n'
 +WALL+'</section>\n<section id="cta"><div class="wrap"><div class="more rv"><p class="lead" style="margin:0">Have a project in mind?</p><a class="btn solid" href="/#contact">Get in touch →</a></div></div></section>\n')
wp=s[:h0]+'\n'+PORT_W+'\n\n'+SAMP+s[h1:]
wp=wp.replace('h2{font-size:clamp(34px,4.6vw,56px);line-height:1.05}','h2,h1.h2{font-size:clamp(34px,4.6vw,56px);line-height:1.05}',1)
wp=wp.replace('<body>','<body class="wpage">',1)
nav=re.search(r'<nav class="pill".*?</nav>',wp,re.S).group(0)
nn=nav.replace('href="#home" class="on"','href="/"').replace('href="#about"','href="/#about"').replace('href="#resume"','href="/#resume"').replace('href="#contact"','href="/#contact"').replace('href="#portfolio"','href="/work/" class="on" aria-current="page"')
wp=wp.replace(nav,nn).replace('<a href="#home">Back to top ↑</a>','<a href="#main">Back to top ↑</a>')
T='Work · Eustace Crentsil, web developer in Accra';D='Selected projects and sample sites by Eustace Crentsil, a web developer in Accra.'
wp=re.sub(r'<title>.*?</title>',f'<title>{T}</title>',wp,1)
wp=re.sub(r'(<meta name="description" content=")[^"]*',r'\g<1>'+D,wp,1)
wp=re.sub(r'(<meta property="og:description" content=")[^"]*',r'\g<1>'+D,wp,1)
wp=re.sub(r'(<meta property="og:title" content=")[^"]*',r'\g<1>'+T,wp,1)
wp=wp.replace('href="https://eustacecrentsil.vercel.app/">','href="https://eustacecrentsil.vercel.app/work/">',1).replace('og:url" content="https://eustacecrentsil.vercel.app/"','og:url" content="https://eustacecrentsil.vercel.app/work/"')
wp=re.sub(r'<script type="application/ld\+json">.*?</script>\n?','',wp,1,re.S)
open('work/index.html','w').write(wp)
