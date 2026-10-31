#!/usr/bin/env python3
"""patch4: improvement pass. Reads the pre-patch snapshot (SRC) and writes the site (DST).
Re-runnable: always starts from SRC. Pipeline: build.py -> patch.py -> patch2.py -> patch3.py -> patch4.py"""
import re, json, os, shutil, html
SRC = os.environ.get('SRC', '/workspace/p2.pre4')
DST = os.environ.get('DST', '/workspace/p2')
SITE = 'https://eustacecrentsil.vercel.app'
TODAY = '2026-10-31'
def rd(p): return open(os.path.join(SRC, p), encoding='utf-8').read()
def wr(p, s):
    full = os.path.join(DST, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(s)
def sub1(pat, rep, s, flags=re.S):
    n = re.subn(pat, rep, s, count=1, flags=flags)
    if n[1] != 1: raise SystemExit('pattern not found: ' + pat[:80])
    return n[0]
def rep1(old, new, s):
    if old not in s: raise SystemExit('text not found: ' + old[:80])
    return s.replace(old, new, 1)
def esc(t): return html.escape(t, quote=True)

CLIENTS = [('ttg-staffing', 'TTG Staffing'), ('edu3dgh', 'Edu3dcation Ghana'), ('iamnurseapproved', 'Nurse Approved')]
w = rd('work/index.html')
CONCEPTS = [(h.split('/')[2], html.unescape(n)) for n, _, h in re.findall(r'<b>(.*?)</b></a><small>(.*?)</small><a class="cs" href="(.*?)"', w)]
assert len(CONCEPTS) == 15
ORDER = CLIENTS + CONCEPTS
SLUGS = [s for s, _ in ORDER]

# ---------- nav ----------
def nav(active, home=False):
    if home:
        items = [('#home', 'Home', '', 'on'), ('/services/', 'Services', ' data-s="#services"', ''),
                 ('/work/', 'Work', ' data-s="#portfolio"', ''), ('#about', 'About', ' class="xs"', ''),
                 ('#resume', 'Resume', ' class="xs"', ''), ('#contact', 'Contact', '', 'cta')]
        lis = []
        for h, t, extra, cls in items:
            c = ' class="%s"' % cls if cls and 'class=' not in extra else ''
            lis.append('<li%s><a href="%s"%s%s>%s</a></li>' % (' class="xs"' if 'xs' in extra else '', h, '' if 'xs' in extra else extra, c, t))
        return '<nav class="pill" aria-label="Main"><ul>\n' + ''.join(lis) + '</ul></nav>'
    items = [('/', 'Home', 'home'), ('/services/', 'Services', 'services'), ('/work/', 'Work', 'work'),
             ('/#resume', 'Resume', 'resume'), ('/#contact', 'Contact', 'contact')]
    lis = []
    for h, t, k in items:
        cls = []
        if k == active: cls.append('on')
        if k == 'contact': cls.append('cta')
        a = ' class="%s"' % ' '.join(cls) if cls else ''
        cur = ' aria-current="page"' if k == active else ''
        li = ' class="xs"' if k == 'resume' else ''
        lis.append('<li%s><a href="%s"%s%s>%s</a></li>' % (li, h, a, cur, t))
    return '<nav class="pill" aria-label="Main"><ul>\n' + ''.join(lis) + '</ul></nav>'
NAV_CSS = ('nav.pill a.cta{background:var(--acc);color:#fff}nav.pill a.cta:hover{color:#fff;background:#1f3596}nav.pill a.cta.on{background:var(--ink)}'
           '@media(max-width:520px){nav.pill li.xs{display:none}nav.pill a{padding:7px 12px;font-size:13.5px}}')
def footer(home=False):
    top = '#home' if home else '#main'
    return ('<footer><div class="wrap mono"><span>© 2026 Eustace Crentsil · Based in Accra, Ghana · Working with clients in the US and worldwide</span>'
            '<span class="fl"><a href="/services/">Services</a> <a href="/work/">Work</a> <a href="/Eustace-Crentsil-CV.pdf" download>CV</a> <a href="/#contact">Contact</a></span>'
            '<a href="%s">Back to top ↑</a></div></footer>' % top)
FOOT_CSS = 'footer .fl{display:flex;gap:16px;flex-wrap:wrap}footer .fl a{text-decoration:none;border-bottom:1px solid var(--rule)}footer .fl a:hover{border-color:var(--ink)}'

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>'
def set_head(s, title, desc, url, ogt=None, ogd=None):
    s = sub1(r'<title>.*?</title>', '<title>%s</title>' % esc(title), s)
    s = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % esc(desc), s)
    s = sub1(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % (SITE + url), s)
    s = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % (SITE + url), s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % esc(ogt or title), s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % esc(ogd or desc), s)
    if 'twitter:title' not in s:
        s = sub1(r'(<meta name="twitter:card"[^>]*>)', r'\1<meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s">' % (esc(ogt or title).replace('\\', r'\\'), esc(ogd or desc).replace('\\', r'\\')), s)
    if 'og:site_name' not in s:
        s = sub1(r'(<meta property="og:type"[^>]*>)', r'\1<meta property="og:site_name" content="Eustace Crentsil"><meta property="og:locale" content="en_GB">', s)
    return s
def slashlinks(s):
    for slug in SLUGS:
        s = s.replace('href="/work/%s"' % slug, 'href="/work/%s/"' % slug)
        s = s.replace('href="/work/%s#' % slug, 'href="/work/%s/#' % slug)
    return s

CTA_BAND = '''<aside class="ctab" aria-label="Start a project"><div><p class="mono">Working on something similar?</p><h2 class="h3">%s</h2><p>%s</p></div><div class="b"><a class="btn solid" href="/#contact">Start a project</a><a class="btn ghost" href="/services/">See services</a></div></aside>'''
CASE_CSS = '''
.glh{margin:44px 0 0;color:var(--ink)}.glh+.facts{margin-top:10px}
.facts.g{grid-template-columns:repeat(3,1fr)}.facts.g div{padding-right:24px}
.facts.auto{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.cx{max-width:760px;margin:18px 0 0;font-size:15px;color:#3d3a33;border-left:3px solid #ecc9a0;padding:2px 0 2px 14px}
.cx a{color:var(--acc)}
.ctab{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;margin:72px 0 0;padding:28px;border:1px solid var(--ink);border-radius:14px;background:var(--card)}
.ctab .h3{font-size:clamp(24px,2.6vw,32px);line-height:1.15;margin:6px 0 8px}.ctab p{margin:0;color:#3d3a33}.ctab .b{display:flex;gap:10px;flex-wrap:wrap}
.pager{grid-template-columns:1fr auto 1fr;align-items:stretch}.pager .mid{display:flex;align-items:center;justify-content:center;text-align:center}
.body .txt h3:first-child{margin-top:0}
.duo .frame img{aspect-ratio:16/10;object-fit:cover;object-position:top}
.duo figure:last-child .frame img{aspect-ratio:390/800}
.btn:focus-visible{outline-offset:4px}
@media(max-width:900px){.facts.g{grid-template-columns:1fr 1fr}.facts.g div:last-child{grid-column:auto}.ctab{grid-template-columns:1fr}}
@media(max-width:520px){.facts.g{grid-template-columns:1fr}.pager{grid-template-columns:1fr}.pager .mid{order:3}}
@media(prefers-reduced-motion:reduce){.btn:hover{transform:none}}
'''

def pager(slug):
    i = SLUGS.index(slug); p = ORDER[i - 1]; n = ORDER[(i + 1) % len(ORDER)]
    return ('<nav class="pager" aria-label="More projects">'
            '<a href="/work/%s/"><span class="mono">← Previous project</span><b>%s</b></a>'
            '<a class="mid" href="/work/"><span class="mono">All work</span></a>'
            '<a class="r" href="/work/%s/"><span class="mono">Next project →</span><b>%s</b></a></nav>') % (p[0], esc(p[1]), n[0], esc(n[1]))

def common_case(s, slug, name):
    s = sub1(r'<nav class="pill".*?</nav>', nav('work'), s)
    s = sub1(r'<footer>.*?</footer>', footer(), s)
    s = sub1(r'<nav class="pager".*?</nav>', pager(slug), s)
    s = s.replace('</style>', CASE_CSS + NAV_CSS + FOOT_CSS + '\n</style>', 1)
    # hero image priority
    s = sub1(r'(<img src="/work/%s/desktop.webp")' % re.escape(slug), r'\1 fetchpriority="high"', s)
    s = slashlinks(s)
    s = s.replace('<span>Projects</span>', '<span>Client projects</span>').replace('<span>Sample sites</span>', '<span>Concept sites</span>')
    return s

# ---------- client case studies ----------
ROLE = '''<p>I worked on this project through Clottware, the company I co-founded and ran from October 2023 to December 2025. My part covered the whole delivery, from the first conversation to support after launch:</p>
  <ul>
   <li><b>Requirements.</b> I ran the first interviews with the client to work out what the site needed to do.</li>
   <li><b>Project management.</b> I scoped the work, set the timelines and kept the client updated as the build moved along.</li>
   <li><b>Design and front end.</b> I helped with the design and built parts of the front end.</li>
   <li><b>Content setup.</b> I set up the site's content.</li>
   <li><b>QA testing.</b> I tested the site before launch.</li>
   <li><b>Support and client relations.</b> After launch I handled ongoing support and was the client's main point of contact.</li>%s
  </ul>'''
CL = {
 'ttg-staffing': dict(
  title='TTG Staffing case study: freelance marketplace web app · Eustace Crentsil',
  desc='How I helped deliver TTG Staffing, a marketplace web app where clients post jobs, verified freelancers bid and the client hires. Requirements, project management, front end and QA.',
  kind='Marketplace web application', func='Job posting, bidding by verified freelancers, hiring',
  extra_role='',
  overview='<p>TTG Staffing brings clients and freelancers together in one place. A client posts a job, verified freelancers bid on it, and the client picks one of them to do the work.</p>',
  problem='<p>TTG had no website. Without one, there was no shared place for clients and freelancers to find each other, so matching people to work depended on the TTG team doing it by hand.</p>',
  objectives=['Give clients a simple way to post a job.', 'Let verified freelancers see jobs and bid on them.', 'Let the client compare bids and hire one freelancer.', 'Move the matching onto the site so the team spends less time pairing people.'],
  approach='''<p>A marketplace has two kinds of users who want different things, so I treated it as one flow seen from two sides. In the requirements interviews I mapped the steps for each side (post, bid, review, hire) before anything was designed, and used that flow to scope the work and set the timeline.</p>
  <p>The "verified" part mattered to the client: clients need to trust who is bidding. That shaped the build, because freelancers had to be checked before they could take part, rather than anyone being able to bid.</p>
  <p>Because the core is structured data (jobs, bids and accounts), the site was built with PHP and MySQL rather than a page builder.</p>''',
  tech='<ul><li><b>HTML/CSS</b> for the interface.</li><li><b>PHP</b> for the marketplace logic: posting, bidding and hiring.</li><li><b>MySQL</b> to store jobs, bids and accounts.</li></ul>',
  impl='<p>The site is built around the marketplace flow:</p><ul><li>Clients post a job.</li><li>Verified freelancers bid on it.</li><li>The client reviews the bids and hires one freelancer.</li></ul><p>Before launch I tested the flow end to end from both sides, then stayed on as the client\'s point of contact for support.</p>',
  deliv=['A marketplace web app covering job posting, bidding and hiring', 'Content set up across the site', 'Pre-launch QA of the full flow', 'Ongoing support after launch'],
  cta=('Need a web app built around how your business works?', 'I can help scope it, plan it and build it, from the first requirements call to support after launch.'),
 ),
 'edu3dgh': dict(
  title='Edu3dcation Ghana case study: WordPress website · Eustace Crentsil',
  desc='How I helped deliver the first website for Edu3dcation Ghana, a 3D technology education company for children in Ghana. WordPress build, project management, content and QA.',
  kind='Business website (WordPress)', func='Programme pages, gallery, partners, contact form with WhatsApp and office details',
  extra_role='',
  overview='<p>Edu3dcation Ghana runs 3D technology classes for children. Its site describes it as the Ghana and Africa arm of the Edu3dcation brand, with headquarters in Poland.</p><p>It teaches kindergarten and elementary school children and also trains teachers. Lessons cover 3D printing, 3D design, 3D scanning, VR, robotics and programming.</p>',
  problem='<p>Edu3dcation Ghana had no website. Parents and schools had no single place to learn about the classes or get in touch, so every question had to be answered one at a time.</p>',
  objectives=['Explain what the classes are and who they are for.', 'Give each teaching area its own page.', 'Make it easy for parents and schools to get in touch.', 'Let the team update the content themselves.'],
  approach='''<p>The audience is parents and schools, not technologists, so the site leads with what children learn and why, and keeps each teaching area (3D printing, robotics, VR and so on) on its own page instead of one long list.</p>
  <p>WordPress fit the job: it is a content site that the team needed to keep updated, with pages, a blog and a gallery. Using a CMS they can edit means they don't need a developer for every change.</p>
  <p>Contact matters most, so the site offers several routes: email, phone, WhatsApp, office locations and a contact form.</p>''',
  tech='<ul><li><b>WordPress</b> as the content management system.</li><li><b>PHP</b>, which WordPress runs on, for theme work.</li></ul>',
  impl='<p>The site includes:</p><ul><li>A home page that introduces the classes and the STEAM approach.</li><li>An about section with the company\'s vision and mission.</li><li>Pages for each teaching area: design and 3D printing, robotics, virtual reality, 3D scanning and 3D pens.</li><li>Menu items for partners, blog, franchise, tiers, modules and gallery.</li><li>A contact section with email, phone, WhatsApp, office locations, work hours and a contact form.</li></ul>',
  deliv=['A WordPress website with pages for each teaching area', 'Content set up across the site', 'A contact section with several ways to get in touch', 'Pre-launch QA and ongoing support'],
  cta=('Need a website your team can update themselves?', 'I build WordPress sites that are easy to manage, and I handle the planning so the project stays on track.'),
 ),
 'iamnurseapproved': dict(
  title='Nurse Approved case study: WordPress LMS website · Eustace Crentsil',
  desc='How I helped deliver Nurse Approved, a WordPress site with online courses on Tutor LMS and automatic certificates through Certify\'em. Requirements, integrations, project management and QA.',
  kind='Online learning website (WordPress + LMS)', func='Online courses, accounts and cart, automatic certificates after a passed quiz',
  extra_role='\n   <li><b>Integrations.</b> I integrated Tutor LMS to run the courses and Certify&#39;em to send certificates to people who pass a quiz.</li>',
  overview='<p>Nurse Approved educates and trains nurses. Its site says it is accredited as a provider of nursing continuing professional development by the American Nurses Credentialing Center\'s Commission on Accreditation, and is a CA BRN approved Continuing Education Provider.</p><p>Courses run in person, as live webinars and on demand, for individuals and groups.</p>',
  problem='<p>Nurse Approved had no website. Nurses had no single place to find the courses, sign up or get in touch, and running courses and certificates without a system meant manual admin for the team.</p>',
  objectives=['Give nurses one place to find courses and sign up.', 'Sell and run courses online.', 'Send certificates automatically when someone passes.', 'Cut the admin the team did by hand.'],
  approach='''<p>The site had to do more than describe courses: it had to sell them, run them and prove completion. Rather than build that from scratch, I integrated two proven WordPress plugins and connected them into one flow.</p>
  <ul><li><b>Tutor LMS</b> runs the courses, lessons, quizzes and student accounts.</li><li><b>Certify&#39;em</b> emails a certificate when someone passes a quiz, so no one has to send certificates by hand.</li></ul>
  <p>Using established plugins kept the build faster to deliver and easier for the team to manage after launch, while WordPress kept the rest of the site (sessions, FAQ, newsletter) easy to edit.</p>''',
  tech='<ul><li><b>WordPress</b> as the CMS.</li><li><b>PHP</b> for theme and integration work.</li><li><b>Tutor LMS</b> for courses, quizzes and accounts.</li><li><b>Certify&#39;em</b> for certificates on a passed quiz.</li></ul>',
  impl='<p>The site includes:</p><ul><li>Online courses run on Tutor LMS.</li><li>Certificates through Certify&#39;em, which emails a certificate when someone passes a quiz.</li><li>A courses page.</li><li>Sign-up, log-in and account pages, with "My Courses" and a cart.</li><li>Sign-ups for free critical thinking case study sessions.</li><li>Sections on education, learning activities, the webinar series and continuing education accreditation.</li><li>A list of organisations they have worked with.</li><li>A FAQ and a newsletter sign-up.</li></ul>',
  deliv=['A WordPress website with a courses section', 'Tutor LMS integration for courses, quizzes and accounts', 'Certify&#39;em integration for automatic certificates', 'Content setup, pre-launch QA and ongoing support'],
  cta=('Need courses, bookings or payments on your WordPress site?', 'I can integrate the right plugins and connect them so the admin runs itself.'),
 ),
}
def sec(id_, n, label, h2, body, after=''):
    return ('<section id="%s"><div class="wrap">\n <div class="sh"><span class="mono"><b>%02d</b> / %s</span><h2>%s</h2></div>\n'
            ' <div class="body"><span></span><div class="txt">%s</div></div>%s\n</div></section>\n') % (id_, n, label, h2, body, after)

for slug, name in CLIENTS:
    s = rd('work/%s/index.html' % slug); c = CL[slug]
    results = re.search(r'<section id="results">.*?<div class="txt">\s*(.*?)\s*</div></div>', s, re.S).group(1)
    figs = re.search(r'(<div class="duo">.*?</figure>\s*)(?=</div></section>)', s, re.S)
    figs = figs.group(1) if figs else ''
    stack = re.search(r'<dt>Stack</dt><dd>(.*?)</dd>', s).group(1)
    glance = ('<p class="mono glh">Project at a glance</p>\n <dl class="facts g">\n'
              '  <div><dt>Client</dt><dd>%s</dd></div>\n  <div><dt>Project type</dt><dd>%s</dd></div>\n'
              '  <div><dt>Team</dt><dd>Clottware (client project)</dd></div>\n'
              '  <div><dt>My role</dt><dd>Requirements, project management, design and front end, content, QA, support</dd></div>\n'
              '  <div><dt>Stack</dt><dd>%s</dd></div>\n  <div><dt>Key functionality</dt><dd>%s</dd></div>\n </dl>') % (esc(name), c['kind'], stack, c['func'])
    s = sub1(r'<dl class="facts">.*?</dl>', glance, s)
    body = ''
    body += sec('overview', 1, 'Overview', 'Background', c['overview'])
    body += sec('problem', 2, 'The problem', 'What they needed', c['problem'])
    body += sec('objectives', 3, 'Objectives', 'What the project had to do', '<ul>' + ''.join('<li>%s</li>' % o for o in c['objectives']) + '</ul>')
    body += sec('role', 4, 'My role', 'What I did', ROLE % c['extra_role'])
    body += sec('approach', 5, 'Approach', 'Approach and key decisions', c['approach'])
    body += sec('tech', 6, 'Technologies', 'What it is built with', c['tech'])
    body += sec('build', 7, 'Implementation', 'What the site includes', c['impl'], '\n ' + figs if figs else '')
    body += sec('deliverables', 8, 'Deliverables', 'What was handed over', '<ul>' + ''.join('<li>%s</li>' % d for d in c['deliv']) + '</ul>')
    out = sec('results', 9, 'Outcomes', 'After launch', '\n  ' + results + '\n ', '\n ' + (CTA_BAND % c['cta']) + '\n <nav class="pager"></nav>')
    body += out
    s = sub1(r'<section id="business">.*</section>\n', body, s)
    s = common_case(s, slug, name)
    s = set_head(s, c['title'], c['desc'], '/work/%s/' % slug)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CreativeWork", "name": "%s website" % name, "headline": c['title'].split(' · ')[0], "description": c['desc'],
         "url": SITE + '/work/%s/' % slug, "image": SITE + '/work/%s/og.jpg' % slug, "genre": "Case study",
         "creator": {"@type": "Person", "name": "Eustace Crentsil", "url": SITE + '/'},
         "contributor": {"@type": "Organization", "name": "Clottware"}, "about": {"@type": "Organization", "name": name}, "inLanguage": "en"},
        crumbs_ld([('Home', '/'), ('Work', '/work/'), (name, '/work/%s/' % slug)])]}
    s = sub1(r'<script type="application/ld\+json">.*?</script>', ld(graph), s)
    wr('work/%s/index.html' % slug, s)

# ---------- concept case studies ----------
for slug, name in CONCEPTS:
    s = rd('work/%s/index.html' % slug)
    s = sub1(r'(</p>\n <h1>)', '</p>\n <p class="cx">This is a self-initiated concept. I design and build sample sites like this to show how I would approach a real business problem through design, content and technology. The business did not commission it. <a href="/work/#samples">More about the concept sites</a>.</p>\n <h1>', s)
    prob = re.search(r'<section id="problem">.*?<h2>(.*?)</h2>', s, re.S).group(1)
    appr = re.search(r'<section id="approach">.*?<h2>(.*?)</h2>', s, re.S).group(1)
    s = sub1(r'<dl class="facts">', '<p class="mono glh">Project at a glance</p>\n <dl class="facts auto">\n  <div><dt>Project type</dt><dd>Concept / sample site</dd></div>', s)
    s = sub1(r'(<dl class="facts auto">.*?)(\n </dl>)', r'\1\n  <div><dt>The problem</dt><dd>%s</dd></div>\n  <div><dt>Design idea</dt><dd>%s</dd></div>\2' % (prob.replace('\\', r'\\'), appr.replace('\\', r'\\')), s)
    s = sub1(r'(\n <nav class="pager")', '\n ' + (CTA_BAND % ('Want a site like this for your business?', 'I design and build websites for small businesses in the US, Ghana and elsewhere. Tell me what you do and I\'ll suggest where to start.')).replace('\\', r'\\') + r'\1', s)
    s = common_case(s, slug, name)
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    title = '%s concept website: case study · Eustace Crentsil' % name
    s = set_head(s, title, d, '/work/%s/' % slug)
    old = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    old.pop('@context', None); old['url'] = SITE + '/work/%s/' % slug; old['description'] = d
    old['genre'] = 'Concept case study'; old['image'] = SITE + '/work/%s/og.jpg' % slug
    old['creator'] = old.pop('author')
    graph = {"@context": "https://schema.org", "@graph": [old, crumbs_ld([('Home', '/'), ('Work', '/work/'), (name, '/work/%s/' % slug)])]}
    s = sub1(r'<script type="application/ld\+json">.*?</script>', ld(graph), s)
    wr('work/%s/index.html' % slug, s)

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch4_pages.py')).read())
