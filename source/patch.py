import re,sys
CSS=r'''
/* automation demo */
.auto{display:grid;grid-template-columns:1fr 360px;gap:64px;align-items:start}
.auto .note{display:inline-flex;gap:10px;align-items:flex-start;background:var(--card);border:1px dashed var(--rule);border-radius:10px;padding:12px 14px;font-size:14px;color:#3d3a33;max-width:560px}
.auto .note b{font:500 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--acc);white-space:nowrap;padding-top:2px}
.auto .steps{list-style:none;padding:0;margin:26px 0 0;counter-reset:s;max-width:560px}
.auto .steps li{counter-increment:s;display:grid;grid-template-columns:34px 1fr;padding:10px 0;border-top:1px solid var(--rule);color:#3d3a33;font-size:15px}
.auto .steps li::before{content:counter(s,lower-roman)'.';font:13px var(--mono);color:var(--mut);padding-top:2px}
.presets{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0}
.presets button{font:14px var(--sans);color:var(--ink);background:transparent;border:1px solid var(--rule);border-radius:999px;padding:8px 14px;cursor:pointer;text-align:left;transition:border-color .2s,background .2s}
.presets button:hover{border-color:var(--ink);background:var(--card)}
.leadc{margin-top:28px;background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:18px 20px;max-width:560px;box-shadow:0 14px 30px -22px rgba(60,48,20,.4)}
.leadc .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.leadc dl{display:grid;grid-template-columns:110px 1fr;margin:0}
.leadc dt{font:12px var(--mono);color:var(--mut);padding:7px 0;border-top:1px solid var(--rule)}
.leadc dd{margin:0;padding:6px 0;border-top:1px solid var(--rule);font-family:var(--serif);font-size:17px;min-height:1.6em}
.leadc dd.e{color:#b3ab9b;font-family:var(--sans);font-size:14px}
.leadc dd.f{animation:fl 1.2s ease}
@keyframes fl{from{background:var(--acc2)}to{background:transparent}}
.phone{position:relative;justify-self:center;width:100%;max-width:340px;background:#fff;border:1px solid var(--rule);border-radius:36px;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,.06),0 30px 60px -30px rgba(60,48,20,.45)}
.phone .scr{border-radius:26px;background:#faf8f3;border:1px solid #eee8db;overflow:hidden;display:flex;flex-direction:column;height:520px}
.phone .bar{display:flex;align-items:center;gap:10px;padding:16px 16px 12px;border-bottom:1px solid #eee8db;background:#fff}
.phone .av{width:32px;height:32px;border-radius:50%;background:var(--acc);color:#fff;display:grid;place-items:center;font:600 13px var(--sans)}
.phone .bar b{display:block;font-size:14px;font-weight:500}.phone .bar small{font:11px var(--mono);color:var(--mut)}
#msgs{flex:1;overflow-y:auto;padding:14px 12px;display:flex;flex-direction:column;gap:8px;scroll-behavior:smooth}
.m{max-width:82%;padding:9px 13px;border-radius:18px;font-size:14px;line-height:1.4;animation:mi .25s ease}
.m.sys{align-self:center;max-width:100%;background:none;font:11px var(--mono);color:var(--mut);text-transform:uppercase;letter-spacing:.05em;padding:4px}
.m.bot{align-self:flex-start;background:#ebe5d7;border-bottom-left-radius:6px}
.m.you{align-self:flex-end;background:var(--acc);color:#fff;border-bottom-right-radius:6px}
.m.dots{display:flex;gap:4px}.m.dots i{width:6px;height:6px;border-radius:50%;background:#8d8676;animation:bl 1s infinite}.m.dots i:nth-child(2){animation-delay:.15s}.m.dots i:nth-child(3){animation-delay:.3s}
@keyframes mi{from{opacity:0;transform:translateY(6px)}}@keyframes bl{50%{opacity:.25}}
#chat{display:flex;gap:6px;padding:10px;border-top:1px solid #eee8db;background:#fff}
#say{flex:1;min-width:0;font:15px var(--sans);border:1px solid var(--rule);border-radius:999px;padding:9px 14px;background:#faf8f3;color:var(--ink)}
#chat button{font:500 14px var(--sans);border:0;border-radius:999px;padding:0 16px;background:var(--ink);color:var(--bg);cursor:pointer}
.reset{font:12px var(--mono);background:none;border:0;color:var(--mut);cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.tag{display:inline-block;font:500 10.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid currentColor;border-radius:999px;padding:1px 7px;margin-right:8px;vertical-align:2px}
.tag.c{color:var(--acc)}.tag.d{color:var(--mut)}
@media (max-width:899px){.auto{grid-template-columns:1fr;gap:40px}.phone .scr{height:480px}.leadc dl{grid-template-columns:90px 1fr}}
'''
HTML='''<section id="automation"><div class="wrap">
 <div class="sh rv"><span class="mono">Try an automation</span><div><h2>The missed call that still books the job.</h2><p class="lead" style="margin-top:16px">When a small business misses a call, an automatic text can reply in seconds, ask the right questions and hand the owner a tidy lead. Play the customer and watch the summary fill in.</p></div></div>
 <div class="auto">
  <div class="rv">
   <p class="note"><b>Demo</b><span>A scripted demo that runs in your browser. No AI service is called and no message is sent anywhere.</span></p>
   <ol class="steps"><li>A call goes unanswered.</li><li>A text goes out right away and asks what the customer needs.</li><li>Replies are sorted into a lead summary the owner can act on.</li></ol>
   <p class="mono" style="margin:26px 0 0" id="pl">Try a message</p>
   <div class="presets" id="presets" role="group" aria-labelledby="pl"><button type="button">My pool is green, can someone come Saturday?</button><button type="button">Garage door spring snapped, door won't open</button><button type="button">How much for a weekly lawn mow?</button><button type="button">Need a deep clean for a 3 bed house</button></div>
   <div class="leadc" aria-live="polite"><div class="top"><span class="mono">Lead summary</span><button type="button" class="reset" id="reset">Start over</button></div>
    <dl id="lead"><dt>Service</dt><dd class="e" data-k="service">Waiting…</dd><dt>Urgency</dt><dd class="e" data-k="urgency">Waiting…</dd><dt>Timing</dt><dd class="e" data-k="timing">Waiting…</dd><dt>Name</dt><dd class="e" data-k="name">Waiting…</dd><dt>Next step</dt><dd class="e" data-k="next">Waiting…</dd></dl></div>
  </div>
  <div class="phone rv" aria-label="Phone showing the text conversation"><div class="scr">
   <div class="bar"><span class="av" aria-hidden="true">PS</span><div><b>Your business</b><small>Auto-reply · demo</small></div></div>
   <div id="msgs" role="log" aria-live="polite"></div>
   <form id="chat" autocomplete="off"><label for="say" class="skip">Your message</label><input id="say" placeholder="Type as the customer…" maxlength="160"><button type="submit">Send</button></form>
  </div></div>
 </div>
</div></section>

'''
JS=r'''
// automation demo (scripted, nothing sent)
(()=>{const box=document.getElementById('msgs');if(!box)return;
const form=document.getElementById('chat'),say=document.getElementById('say'),dd=k=>document.querySelector('#lead dd[data-k="'+k+'"]');
const rules=[[/pool|chlorine|green water/i,'Pool cleaning'],[/garage|spring|opener/i,'Garage door repair'],[/lawn|mow|grass|yard/i,'Lawn care'],[/clean|maid|deep clean/i,'House cleaning'],[/plumb|leak|pipe|drain|toilet/i,'Plumbing'],[/ac\b|a\/c|air con|hvac|heat/i,'Heating and cooling'],[/roof/i,'Roofing']];
let stage=0,busy=false,L={};
function add(t,c){const m=document.createElement('div');m.className='m '+c;m.textContent=t;box.appendChild(m);box.scrollTop=box.scrollHeight;return m}
function set(k,v){const e=dd(k);e.textContent=v;e.classList.remove('e','f');void e.offsetWidth;if(!RM)e.classList.add('f');L[k]=v}
function reply(t,cb){busy=true;const d=document.createElement('div');d.className='m bot dots';d.setAttribute('aria-label','typing');d.innerHTML='<i></i><i></i><i></i>';box.appendChild(d);box.scrollTop=box.scrollHeight;
 setTimeout(()=>{d.remove();add(t,'bot');busy=false;cb&&cb()},RM?0:900)}
function handle(t){
 if(stage===0){const r=rules.find(r=>r[0].test(t));set('service',r?r[1]:'General enquiry');
  set('urgency',/snapp|broke|won.?t|leak|flood|urgent|asap|emergency|today|now/i.test(t)?'High, same day if possible':/how much|price|quote|cost/i.test(t)?'Low, asking for a quote':'Normal');
  const tm=t.match(/monday|tuesday|wednesday|thursday|friday|saturday|sunday|today|tomorrow|this week|weekend/i);if(tm)set('timing',tm[0][0].toUpperCase()+tm[0].slice(1).toLowerCase());
  stage=1;reply('Thanks! We can help with that. What\'s your name and zip code?')}
 else if(stage===1){const n=t.match(/(?:i'?m|name is|this is|it'?s)\s+([a-z]+)/i)||t.match(/^([a-z]+)/i);if(n)set('name',n[1][0].toUpperCase()+n[1].slice(1).toLowerCase());
  stage=2;if(L.timing)reply('Got it. We\'ll aim for '+L.timing.toLowerCase()+'. The owner will call you back shortly to confirm.',fin);else reply('Got it. When works best for a visit?')}
 else if(stage===2){set('timing',t.slice(0,40));reply('Perfect. The owner will call you back shortly to confirm.',fin)}
 else reply('Thanks, your details are with the owner. (Demo finished. Press Start over to try again.)')}
function fin(){stage=3;set('next','Owner calls back to confirm')}
function start(){box.innerHTML='';stage=0;L={};document.querySelectorAll('#lead dd').forEach(e=>{e.textContent='Waiting…';e.className='e'});add('Missed call from (555) 010-2049','sys');add('Hi! Sorry we missed your call. What can we help you with today?','bot')}
function send(t){t=t.trim();if(!t||busy)return;add(t,'you');handle(t)}
form.addEventListener('submit',e=>{e.preventDefault();send(say.value);say.value=''});
document.querySelectorAll('#presets button').forEach(b=>b.addEventListener('click',()=>{start();send(b.textContent)}));
document.getElementById('reset').addEventListener('click',start);
start()})();
'''
for fn in sys.argv[1:]:
    s=open(fn).read()
    s=s.replace('@media (prefers-reduced-motion:reduce)',CSS+'@media (prefers-reduced-motion:reduce)',1)
    s=s.replace('<section id="concepts">',HTML+'<section id="concepts">',1)
    s=s.replace("map={services:'portfolio',concepts:'portfolio'}","map={services:'portfolio',automation:'portfolio',concepts:'portfolio'}")
    s=s.replace('<span class="mono">2019–2024</span><div><h4>Geologist</h4><div class="org">Planet One Group · Achiaa Mining · Sri Sai Drill Tech</div>','<span class="mono">2019–2025</span><div><h4>Geologist</h4><div class="org">Planet One Minerals · Achiaa Mining · Sri Sai Drilling Technologies</div>')
    s=s.replace('<a href="https://wa.me/233546496092" target="_blank" rel="noopener">+233 54 649 6092</a></div>','<a href="https://wa.me/233546496092" target="_blank" rel="noopener">+233 54 649 6092</a></div>\n  <div><p class="mono">Phone</p><a href="tel:+233576564754">+233 57 656 4754</a></div>')
    s=s.replace('.cgrid{display:grid;grid-template-columns:repeat(3,1fr)','.cgrid{display:grid;grid-template-columns:repeat(4,1fr)')
    s=s.replace('<div class="btns"><a class="btn ghost" href="#resume">Read my resume</a></div>','<div class="btns"><a class="btn ghost" href="#resume">Read my resume</a><!-- CV_BUTTON (off until Eustace approves the CV): <a class="btn solid" href="/Eustace-Crentsil-CV.pdf" download>Download CV</a> --></div>')
    s=s.replace('<p>A site for a public relations firm.</p>','<p><span class="tag c">Client</span>A site for a public relations firm.</p>')
    s=s.replace('<p>An online furniture and decor shop.</p>','<p><span class="tag d">Demo</span>An online furniture and decor shop.</p>')
    i=s.rindex('</script>');s=s[:i]+JS+s[:0]+s[i:]
    open(fn,'w').write(s)
