import sys
CSS=r'''
/* contact form */
.cform{margin-top:64px;display:grid;grid-template-columns:300px 1fr;gap:48px;border-top:1px solid var(--rule);padding-top:28px}
.cform h3{font-size:30px;line-height:1.1}.cform .side p{color:#3d3a33;font-size:15px;margin-top:12px}
.cform form{display:grid;grid-template-columns:1fr 1fr;gap:16px 20px}
.cform .f{display:flex;flex-direction:column;gap:6px}.cform .f.w{grid-column:1/-1}
.cform label{font:500 12px var(--mono);letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}
.cform label i{font-style:normal;text-transform:none;letter-spacing:0;opacity:.8}
.cform input,.cform select,.cform textarea{font:16px var(--sans);color:var(--ink);background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:11px 13px;width:100%;transition:border-color .2s}
.cform textarea{min-height:130px;resize:vertical}
.cform input:focus,.cform select:focus,.cform textarea:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px var(--acc2)}
.cform [aria-invalid="true"]{border-color:#a5342a}
.cform .err{font-size:13px;color:#a5342a;min-height:0}
.cform .row{grid-column:1/-1;display:flex;flex-wrap:wrap;align-items:center;gap:16px}
.cform button[type=submit]{font:500 15px var(--sans);background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:13px 24px;cursor:pointer}
.cform button[disabled]{opacity:.6;cursor:wait}
.fstat{font-size:15px;margin:0}.fstat:empty{display:none}
.fstat{padding:12px 14px;border-radius:10px;border:1px solid var(--rule);background:var(--card);flex:1 1 260px}
.fstat.ok{border-color:#2f6b3e;color:#24502f}.fstat.bad{border-color:#a5342a;color:#7d271f}.fstat.info{border-color:var(--acc);color:var(--acc)}
.hp{position:absolute!important;left:-9999px;width:1px;height:1px;overflow:hidden}
.quote .lbl{display:block;margin-bottom:22px}
.quote .away{margin-top:34px}
@media (max-width:899px){.cform{grid-template-columns:1fr;gap:24px}.cform form{grid-template-columns:1fr}}
'''
FORM='''
 <div class="cform rv" id="brief">
  <div class="side"><p class="mono">Or send a short brief</p><h3>Tell me what you need.</h3><p>A few lines is enough. I'll reply by email, usually the same day.</p></div>
  <!-- FORMSPREE: replace YOUR_FORM_ID in the action below with the form ID from formspree.io (e.g. https://formspree.io/f/abcdwxyz), then redeploy. -->
  <form id="cf" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
   <div class="f"><label for="cf-name">Name</label><input id="cf-name" name="name" autocomplete="name" required maxlength="100" aria-describedby="cf-name-e"><span class="err" id="cf-name-e"></span></div>
   <div class="f"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required maxlength="150" aria-describedby="cf-email-e"><span class="err" id="cf-email-e"></span></div>
   <div class="f"><label for="cf-co">Business or company <i>(optional)</i></label><input id="cf-co" name="company" autocomplete="organization" maxlength="120"></div>
   <div class="f"><label for="cf-need">What do you need?</label><select id="cf-need" name="need" required aria-describedby="cf-need-e"><option value="">Choose one</option><option>Website</option><option>AI automation</option><option>Website care</option><option>Something else</option></select><span class="err" id="cf-need-e"></span></div>
   <div class="f w"><label for="cf-budget">Budget <i>(optional)</i></label><select id="cf-budget" name="budget"><option value="">Prefer not to say</option><option>Under $500</option><option>$500 – $1,500</option><option>$1,500 – $5,000</option><option>Over $5,000</option><option>Not sure yet</option></select></div>
   <div class="f w"><label for="cf-msg">Message</label><textarea id="cf-msg" name="message" required minlength="10" maxlength="3000" aria-describedby="cf-msg-e"></textarea><span class="err" id="cf-msg-e"></span></div>
   <div class="hp" aria-hidden="true"><label for="cf-gotcha">Leave this empty</label><input id="cf-gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
   <input type="hidden" name="_subject" value="New brief from eustacecrentsil.vercel.app">
   <div class="row"><button type="submit">Send brief</button><p class="fstat" id="cf-stat" role="status" aria-live="polite"></p></div>
  </form>
 </div>'''
JS=r'''
// contact form (Formspree, progressive enhancement)
(()=>{const f=document.getElementById('cf');if(!f)return;const st=document.getElementById('cf-stat'),btn=f.querySelector('[type=submit]');
const MAIL='eustaceocrentsil@gmail.com',live=!/YOUR_FORM_ID/.test(f.action);
const msg=(t,c,html)=>{st.className='fstat '+c;html?st.innerHTML=t:st.textContent=t};
const checks={'cf-name':v=>v.trim()?'':'Please add your name.','cf-email':v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())?'':'Please add a valid email address.','cf-need':v=>v?'':'Please choose one.','cf-msg':v=>v.trim().length>=10?'':'Please write a little more (at least 10 characters).'};
function check(id){const el=document.getElementById(id),e=checks[id](el.value);el.setAttribute('aria-invalid',e?'true':'false');document.getElementById(id+'-e').textContent=e;return !e}
Object.keys(checks).forEach(id=>document.getElementById(id).addEventListener('blur',()=>check(id)));
f.addEventListener('submit',async ev=>{ev.preventDefault();const bad=Object.keys(checks).filter(id=>!check(id));
 if(bad.length){document.getElementById(bad[0]).focus();msg('Please fix the highlighted fields.','bad');return}
 if(!live){msg('This form isn\u2019t connected yet, so nothing was sent. Please email me at <a href="mailto:'+MAIL+'">'+MAIL+'</a> or message me on <a href="https://wa.me/233546496092" target="_blank" rel="noopener">WhatsApp</a>.','info',1);return}
 btn.disabled=true;btn.textContent='Sending…';msg('','');
 try{const r=await fetch(f.action,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}});
  if(r.ok){f.reset();Object.keys(checks).forEach(id=>document.getElementById(id).removeAttribute('aria-invalid'));msg('Thanks, your brief was sent. I\u2019ll reply by email soon.','ok')}
  else{let d={};try{d=await r.json()}catch(_){}msg((d.errors&&d.errors.map(x=>x.message).join(' '))||'Something went wrong and your brief was not sent.','bad');st.insertAdjacentHTML('beforeend',' Please email <a href="mailto:'+MAIL+'">'+MAIL+'</a> instead.')}
 }catch(_){msg('Your brief could not be sent (network error). Please email <a href="mailto:'+MAIL+'">'+MAIL+'</a> instead.','bad',1)}
 btn.disabled=false;btn.textContent='Send brief'})})();
'''
OLDQ_START='<div class="quote rv"><q>Building clean and meaningful experiences through thoughtful code and quiet design.</q>'
NEWQ='''<div class="quote rv"><span class="mono lbl">How I work</span><q>I plan the work, keep you in the loop and build it myself, so the website helps your business grow.</q>
 <div class="tags away" aria-label="Away from the desk"><span>Away from the desk:</span><span>Exploring nature in Ghana</span><span>Painting</span></div></div>'''
for fn in sys.argv[1:]:
    s=open(fn).read()
    a=s.index(OLDQ_START);b=s.index('</div></div>',a)+len('</div></div>');s=s[:a]+NEWQ+s[b:]
    s=s.replace('@media (prefers-reduced-motion:reduce)',CSS+'@media (prefers-reduced-motion:reduce)',1)
    a=s.index('<div class="cgrid rv">');b=s.index('\n </div>',a)+len('\n </div>');s=s[:b]+FORM+s[b:]
    s=s.replace('<!-- CV_BUTTON (off until Eustace approves the CV): <a class="btn solid" href="/Eustace-Crentsil-CV.pdf" download>Download CV</a> -->','<a class="btn solid" href="/Eustace-Crentsil-CV.pdf" download>Download CV (PDF)</a>')
    s=s.replace('<p class="lead" style="margin-top:16px">Where I studied, where I\'ve worked and what I\'ve picked up along the way.</p>','<p class="lead" style="margin-top:16px">Where I studied, where I\'ve worked and what I\'ve picked up along the way. <a href="/Eustace-Crentsil-CV.pdf" download style="color:var(--acc)">Download my CV (PDF)</a>.</p>')
    s=s.replace('<div class="ent"><span class="mono">Oct 2023–Dec 2025</span>','<div class="ent"><span class="mono">Feb–Mar 2026</span><div><h4>AI Trainer (QGIS Expert)</h4><div class="org">Freelance · micro1 (Remote)</div><ul><li>Built end-to-end QGIS projects for AI model training, converting raw data into structured, validated GIS datasets.</li><li>Wrote clear, step-by-step workflows and reasoning for GIS tasks used to train AI models.</li></ul></div></div>\n   <div class="ent"><span class="mono">Oct 2023–Dec 2025</span>',1)
    s=s.replace('<div class="org">ALX</div></div></div>','<div class="org">ALX</div></div></div>\n   <div class="ent"><span class="mono">Mar 2025</span><div><h4>Workflow Specialist Certificate</h4><div class="org">Asana</div></div></div>',1)
    i=s.rindex('</script>');s=s[:i]+JS+s[i:]
    open(fn,'w').write(s)
