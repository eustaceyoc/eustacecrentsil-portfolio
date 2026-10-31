# patch4 part 2: home, /work/, /services/, 404, sitemap, robots, vercel.json. Exec'd by patch4.py.
def home_nav():
    return ('<nav class="pill" aria-label="Main"><ul>\n'
            '<li><a href="#home" class="on">Home</a></li><li><a href="/services/" data-s="#services">Services</a></li>'
            '<li><a href="/work/" data-s="#portfolio">Work</a></li><li class="xs"><a href="#about">About</a></li>'
            '<li class="xs"><a href="#resume">Resume</a></li><li><a href="#contact" class="cta">Contact</a></li></ul></nav>')
def work_nav():
    return ('<nav class="pill" aria-label="Main"><ul>\n'
            '<li><a href="/">Home</a></li><li><a href="/services/">Services</a></li>'
            '<li><a href="/work/" class="on" aria-current="page">Work</a></li><li class="xs"><a href="/#resume">Resume</a></li>'
            '<li><a href="/#contact" class="cta">Contact</a></li></ul></nav>')
PERSON = {"@type": "Person", "@id": SITE + "/#person", "name": "Eustace Crentsil",
          "jobTitle": "Web developer and technical project manager", "url": SITE + "/", "image": SITE + "/me-800.webp",
          "email": "mailto:eustaceocrentsil@gmail.com",
          "address": {"@type": "PostalAddress", "addressLocality": "Accra", "addressCountry": "GH"},
          "knowsAbout": ["Web development", "WordPress", "Web applications", "Business automation", "Technical project management"],
          "sameAs": ["https://x.com/_yawofori", "https://www.linkedin.com/in/eustace-crentsil"]}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Eustace Crentsil", "inLanguage": "en", "publisher": {"@id": SITE + "/#person"}}
SERVICE_ORG = {"@type": "ProfessionalService", "@id": SITE + "/#service", "name": "Eustace Crentsil, web development and technical project management",
               "url": SITE + "/services/", "image": SITE + "/og.jpg", "email": "eustaceocrentsil@gmail.com", "telephone": "+233576564754",
               "founder": {"@id": SITE + "/#person"},
               "address": {"@type": "PostalAddress", "addressLocality": "Accra", "addressCountry": "GH"},
               "areaServed": [{"@type": "Country", "name": "Ghana"}, {"@type": "Country", "name": "United States"}, {"@type": "Place", "name": "Worldwide"}],
               "knowsAbout": ["Website development", "Web application development", "WordPress", "Business automation", "Technical project management"]}
HEAD_NOTES = '''<!-- Google Search Console: after verifying with the HTML-tag method, paste the meta tag Google gives you on the next line, then redeploy.
<meta name="google-site-verification" content="PASTE-YOUR-CODE-HERE">
-->
<!-- Google Analytics 4 (optional, not active). Create a GA4 web stream, replace G-XXXXXXXXXX with your Measurement ID, remove this comment wrapper, and update your privacy notice.
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-XXXXXXXXXX');</script>
-->
'''
HOME_CSS = '''
.hello{font-size:clamp(40px,5.6vw,74px);line-height:1.02}
.kick{margin:0 0 20px}
.hero .bio{font-size:18px;max-width:600px;margin-top:22px}
.typed{margin:18px 0 0;font-size:clamp(20px,2.2vw,26px)}
.svc.three div:nth-child(4){padding-left:24px}
.svc.three ul{margin:12px 0 0;padding-left:1.1em;color:var(--mut);font-size:14.5px}.svc.three li{margin:.2em 0}
.svc.three a.go{display:inline-block;margin-top:14px;font:500 13px var(--mono);color:var(--acc);text-decoration:none;border-bottom:1px solid currentColor}
.svc.three a.go:hover{color:var(--ink)}
.qa{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 28px}
.cform .f.h{grid-column:auto}
@media (max-width:899px){.svc.three div:nth-child(4){padding-left:0}}
'''
def build_home():
    s = rd('index.html')
    s = set_head(s, 'Eustace Crentsil · Web Developer & Technical Project Manager in Accra',
                 'Freelance web developer and technical project manager based in Accra, Ghana. I build websites, web apps and business automations for small businesses in Ghana, the US and worldwide.',
                 '/', 'Eustace Crentsil · Web developer & technical project manager',
                 'I turn business ideas into digital solutions that work: websites, web apps and automation, planned and delivered properly.')
    s = sub1(r'<script type="application/ld\+json">.*?</script>', ld({"@context": "https://schema.org", "@graph": [PERSON, WEBSITE, SERVICE_ORG]}), s)
    s = rep1('<meta name="theme-color"', HEAD_NOTES + '<meta name="theme-color"', s)
    s = rep1('</style>', HOME_CSS + NAV_CSS + FOOT_CSS + '\n</style>', s)
    s = sub1(r'<nav class="pill".*?</nav>', home_nav(), s)
    hero_txt = '''<div>
   <p class="mono kick">Eustace Crentsil · Accra, Ghana · Remote worldwide</p>
   <h1 class="hello">I turn business ideas into digital solutions <em>that work.</em></h1>
   <p class="bio">I'm Eustace, a web developer and technical project manager. I help businesses build websites, develop digital products and automate their operations, and I run the project properly from the first call to launch and beyond.</p>
   <p class="typed" aria-label="Web developer, technical project manager and automation builder"><span class="t" id="typed" aria-hidden="true">web developer</span></p>
   <div class="btns"><a class="btn solid" href="#contact">Start a project</a><a class="btn ghost" href="/work/">View my work</a></div>
   <div class="soc"><a href="https://x.com/_yawofori" rel="me noopener" target="_blank">X / Twitter</a><a href="https://www.linkedin.com/in/eustace-crentsil" rel="me noopener" target="_blank">LinkedIn</a><a href="https://wa.me/233546496092" rel="noopener" target="_blank">WhatsApp</a></div>
  </div>'''
    s = sub1(r'<div>\n   <p class="mono">Accra, Ghana</p>.*?</div>\n  </div>', hero_txt.replace('\\', r'\\'), s)
    s = rep1('<img src="/me-400.webp"', '<img fetchpriority="high" src="/me-400.webp"', s)
    s = s.replace("const words=['web developer','project manager','problem solver']", "const words=['web developer','technical project manager','automation builder']")
    s = s.replace("map={services:'portfolio',automation:'portfolio',concepts:'portfolio'}", "map={automation:'services',concepts:'portfolio'}")
    # services teaser
    teaser = '''<section id="services"><div class="wrap">
 <div class="sh rv"><span class="mono"><b>02</b> / Services</span><div><h2>How I can help.</h2><p class="lead" style="margin-top:16px">Three things I do well, for small businesses in Ghana, the US and anywhere else I can work remotely.</p></div></div>
 <div class="svc three rv">
  <div><span class="mono">i.</span><h3>Websites &amp; web apps</h3><p>Business websites, online stores, WordPress builds, portals and custom web apps, plus care after launch.</p><a class="go" href="/services/#web">Website &amp; web app development →</a></div>
  <div><span class="mono">ii.</span><h3>Business automation</h3><p>Connect your tools and take repetitive work off your plate: lead handling, follow-ups, workflows and integrations.</p><a class="go" href="/services/#automation">Business automation →</a></div>
  <div><span class="mono">iii.</span><h3>Technical project management</h3><p>Requirements, planning, coordination and QA, so a digital project gets delivered on time and as agreed.</p><a class="go" href="/services/#pm">Technical project management →</a></div>
 </div>
 <div class="more rv"><span class="mono">Also: UI/UX design · hosting &amp; cloud · digital marketing basics</span><a class="btn ghost" href="/services/">All services →</a></div>
</div></section>
'''
    def grab(sid):
        m = re.search(r'<section[^>]*id="%s".*?</section>\n' % sid, s, re.S); return m.group(0)
    parts = {k: grab(k) for k in ['about', 'resume', 'portfolio', 'services', 'automation', 'concepts']}
    block_start = s.index(parts['about']); block_end = s.index(parts['concepts']) + len(parts['concepts'])
    pf = parts['portfolio'].replace('<b>04</b> / Portfolio', '<b>03</b> / Work').replace('A few recent projects. The full list, with the sample sites, is on the work page.', 'Client projects I helped deliver, from first requirements to launch. The full list, with the concept sites, is on the work page.')
    au = parts['automation'].replace('\n</div></section>', '\n <div class="more rv"><span class="mono">Want something like this for your business?</span><a class="btn ghost" href="/services/#automation">Business automation service →</a></div>\n</div></section>', 1)
    au = au.replace('<span class="mono">Try an automation</span>', '<span class="mono">Try an automation</span>')
    cc = parts['concepts'].replace('On the side, I build sample sites for small US service businesses that don\'t have one yet, so the owner can see what theirs could look like. Drag the handle.',
                                   'Self-initiated concept sites: I pick a real small business with no website and build a sample to show how I\'d solve it. Drag the handle to compare.')
    ab = parts['about'].replace('<b>02</b> / About', '<b>04</b> / About')
    rs = parts['resume'].replace('<b>03</b> / Resume', '<b>05</b> / Resume')
    s = s[:block_start] + teaser + '\n' + pf + '\n' + au + '\n' + cc + '\n' + ab + '\n' + rs + s[block_end:]
    # contact
    s = rep1('<div class="sh rv"><span class="mono"><b>05</b> / Contact</span><p class="lead" style="margin:0">Got a question or a proposal, or just want to say hello? Go ahead.</p></div>',
             '<div class="sh rv"><span class="mono"><b>06</b> / Contact</span><div><h2>Let\'s talk about your project.</h2><p class="lead" style="margin-top:16px">Tell me what you\'re working on. A few lines is enough to start, and I usually reply within a day. I work with clients in Ghana, the US and worldwide.</p></div></div>\n <div class="qa rv"><a class="btn solid" href="#brief">Send a project brief</a><a class="btn ghost" href="https://wa.me/233546496092" target="_blank" rel="noopener">Message me on WhatsApp</a></div>', s)
    s = rep1('<p class="mono">Or send a short brief</p><h3>Tell me what you need.</h3><p>A few lines is enough. I\'ll reply by email, usually the same day.</p>',
             '<p class="mono">Project brief</p><h3>Tell me what you need.</h3><p>A few lines is enough. Budget and timeline are optional; "not sure yet" is a fine answer. I\'ll reply by email, usually the same day.</p>', s)
    s = rep1('<label for="cf-need">What do you need?</label><select id="cf-need" name="need" required aria-describedby="cf-need-e"><option value="">Choose one</option><option>Website</option><option>AI automation</option><option>Website care</option><option>Something else</option></select>',
             '<label for="cf-need">Project type</label><select id="cf-need" name="need" required aria-describedby="cf-need-e"><option value="">Choose one</option><option>New website</option><option>Web app or portal</option><option>WordPress site or plugin work</option><option>Business automation</option><option>Technical project management</option><option>Website care or fixes</option><option>Something else</option></select>', s)
    s = rep1('<div class="f w"><label for="cf-budget">Budget <i>(optional)</i></label><select id="cf-budget" name="budget"><option value="">Prefer not to say</option><option>Under $500</option><option>$500 – $1,500</option><option>$1,500 – $5,000</option><option>Over $5,000</option><option>Not sure yet</option></select></div>',
             '<div class="f h"><label for="cf-budget">Budget <i>(optional)</i></label><select id="cf-budget" name="budget"><option value="">Prefer not to say</option><option>Not sure yet</option><option>Under $500</option><option>$500 – $1,500</option><option>$1,500 – $5,000</option><option>Over $5,000</option></select></div>\n'
             '   <div class="f h"><label for="cf-time">Timeline <i>(optional)</i></label><select id="cf-time" name="timeline"><option value="">Not sure yet</option><option>As soon as possible</option><option>Within a month</option><option>1 – 3 months</option><option>More than 3 months</option></select></div>', s)
    s = rep1('<div class="f w"><label for="cf-msg">Message</label>', '<div class="f w"><label for="cf-msg">About the project</label>', s)
    s = rep1("if(r.ok){f.reset();", "if(r.ok){const nd=f.elements.need.value;try{window.va&&window.va('event',{name:'Enquiry submitted',data:{type:nd}})}catch(_){}f.reset();", s)
    s = sub1(r'<footer>.*?</footer>', footer(home=True), s)
    s = slashlinks(s)
    wr('index.html', s)

def build_work():
    s = rd('work/index.html')
    s = set_head(s, 'Web Development Portfolio & Case Studies · Eustace Crentsil',
                 'Client case studies and self-initiated concept sites by Eustace Crentsil, a freelance web developer in Accra: WordPress sites, web apps and small business websites for US and Ghanaian businesses.',
                 '/work/', 'Work · Eustace Crentsil', 'Client case studies and self-initiated concept websites.')
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Work · Eustace Crentsil", "url": SITE + "/work/", "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}},
        crumbs_ld([('Home', '/'), ('Work', '/work/')])]}
    s = rep1('<link rel="preconnect"', ld(graph) + '\n<link rel="preconnect"', s)
    s = rep1('</style>', NAV_CSS + FOOT_CSS + '.cnote{max-width:760px;margin:18px 0 0;color:#3d3a33;border-left:3px solid #ecc9a0;padding:2px 0 2px 14px}\n</style>', s)
    s = sub1(r'<nav class="pill".*?</nav>', work_nav(), s)
    s = rep1('<span class="mono"><b>04</b> / Portfolio</span><div><h1 class="h2">Selected work.</h1><p class="lead" style="margin-top:16px">Work I\'ve done across web development, project management and digital products.</p></div>',
             '<span class="mono">Work</span><div><h1 class="h2">Selected work.</h1><p class="lead" style="margin-top:16px">Client projects I helped deliver as a web developer and project manager, and other builds across WordPress, PHP and React. The first three have full case studies.</p></div>', s)
    s = rep1('<h2>Sample sites / concepts.</h2><p class="lead" style="margin-top:16px">On the side, I build sample sites for small US service businesses that don\'t have one yet, so the owner can see what theirs could look like. Each one has a short case study.</p>',
             '<h2>Concept sites.</h2><p class="lead" style="margin-top:16px">These are self-initiated concept sites. I pick a real small business that doesn\'t have a website yet, look at the problem it faces online, and design and build a sample to show how I would solve it. Each one has a short case study on the problem, the design reasoning and the build.</p><p class="cnote">None of these businesses commissioned or endorsed the work. Each sample site says so, is hidden from search engines, and uses only facts from the business\'s public listings.</p>', s)
    s = rep1('<p class="lead" style="margin:0">Have a project in mind?</p><a class="btn solid" href="/#contact">Get in touch →</a>',
             '<p class="lead" style="margin:0">Have a project in mind? Tell me about it, or see what I offer first.</p><span style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn ghost" href="/services/">Services</a><a class="btn solid" href="/#contact">Start a project →</a></span>', s)
    s = sub1(r'<footer>.*?</footer>', footer(), s)
    s = slashlinks(s)
    wr('work/index.html', s)

def skeleton(title, desc, url, robots=None):
    base = rd('work/ttg-staffing/index.html')
    head = base[:base.index('</style>')] + CASE_CSS + NAV_CSS + FOOT_CSS + '%%CSS%%\n</style>\n</head>\n'
    head = set_head(head, title, desc, url)
    head = sub1(r'<script type="application/ld\+json">.*?</script>', '%%LD%%', head)
    head = head.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    head = head.replace('/work/ttg-staffing/og.jpg', '/og.jpg')
    if robots:
        head = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="%s">' % robots, head)
    return head

SVC = [
 dict(id='web', n='A', name='Website &amp; web app development',
  who='Small businesses that need a first website or a better one, and teams that need a custom web app, portal or online store built around how they work.',
  probs=['No website, or one that doesn\'t explain what you do or bring in enquiries.', 'A site you can\'t update without calling a developer.', 'Work that runs on spreadsheets and messages and needs a proper web app.', 'An online store or booking flow that\'s clumsy on a phone.'],
  inc=['Business websites and landing pages', 'E-commerce stores', 'Custom web applications and client or member portals', 'WordPress sites, themes and plugin integrations (for example LMS and certificates)', 'UI/UX design: mobile-first layouts and clear page structure', 'Hosting and cloud setup: domains, email, AWS, cPanel or Vercel, backups', 'Search-friendly pages and analytics basics', 'Maintenance, updates and small fixes after launch'],
  deliv=['A site or app that works on phones and desktops', 'Content set up and checked', 'Hosting, domain and analytics in place', 'A short handover so you can update content yourself'],
  ex='See <a href="/work/ttg-staffing/">TTG Staffing</a> (a marketplace web app), <a href="/work/iamnurseapproved/">Nurse Approved</a> (WordPress with Tutor LMS and Certify\'em) and <a href="/work/edu3dgh/">Edu3dcation Ghana</a> (a WordPress site).',
  kw='custom website development, WordPress developer, web application developer'),
 dict(id='automation', n='B', name='Business automation',
  who='Owners and small teams who lose hours to the same manual steps every week, or who miss leads because nobody replies fast enough.',
  probs=['Leads that arrive by phone, form or WhatsApp and go cold before anyone replies.', 'Copying the same data between tools by hand.', 'Follow-ups and reminders that depend on someone remembering.', 'Tools that don\'t talk to each other.'],
  inc=['Workflow automation for repetitive tasks', 'Integrations between the tools you already use (forms, email, sheets, CRM, website)', 'Lead capture, routing and follow-up', 'Process mapping before anything is automated', 'Simple dashboards or summaries so you can see what\'s happening'],
  deliv=['A map of the process, before and after', 'The working automation, tested with real cases', 'Notes on how it works and what to do if something changes'],
  ex='Try the <a href="/#automation">missed-call demo</a> on the home page: it shows how an automatic reply can turn a missed call into a tidy lead summary.',
  kw='business automation specialist'),
 dict(id='pm', n='C', name='Technical project management',
  who='Businesses running a website, app or software project that has several people or vendors involved, and founders who need someone to turn an idea into a plan the developers can build.',
  probs=['Unclear requirements, so the build keeps changing.', 'No timeline, or one nobody trusts.', 'Developers, designers and the client working from different pictures of the project.', 'Launch day surprises because nothing was tested properly.'],
  inc=['Requirements gathering and client interviews', 'Scoping, planning and timelines', 'Coordinating designers, developers and vendors', 'Regular updates to you and the team', 'Quality assurance and testing before launch', 'Delivery, handover and support planning'],
  deliv=['A written scope and plan', 'A timeline with milestones', 'Regular status updates', 'A QA checklist and test results before launch'],
  ex='On all three <a href="/work/">client projects</a> I ran requirements, planning, client updates and QA alongside the build. I use tools like Asana, Trello, Notion and GitHub, and hold an Asana Workflow Specialist certificate.',
  kw='technical project manager, freelance technical project manager'),
]
def build_services():
    title = 'Services: Websites, Web Apps, Automation & Project Management · Eustace Crentsil'
    desc = 'Website and web app development, WordPress, business automation and technical project management for small businesses. Based in Accra, Ghana, working remotely with US and worldwide clients.'
    head = skeleton(title, desc, '/services/')
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": "Services · Eustace Crentsil", "url": SITE + "/services/", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#service"}},
        dict(SERVICE_ORG, **{"hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": html.unescape(x['name']), "url": SITE + "/services/#" + x['id']}} for x in SVC]}}),
        crumbs_ld([('Home', '/'), ('Services', '/services/')])]}
    css = '''
.svcnav{display:flex;flex-wrap:wrap;gap:10px;margin:30px 0 0}.svcnav a{text-decoration:none;font:500 13px var(--mono);border:1px solid var(--rule);border-radius:999px;padding:8px 14px;background:var(--card)}.svcnav a:hover{border-color:var(--ink)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px 40px}.cols h3{font-size:22px;margin:0 0 8px!important}
.cols ul{padding-left:1.1em;margin:0}.cols li{margin:.25em 0}
.ex{background:var(--card);border:1px solid var(--rule);border-left:3px solid var(--acc);border-radius:8px;padding:14px 16px;margin:24px 0 0;font-size:15.5px}.ex a{color:var(--acc)}
.steps4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;list-style:none;padding:0;margin:0;counter-reset:s}
.steps4 li{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:18px;counter-increment:s}
.steps4 li:before{content:"0" counter(s);display:block;font:500 12px var(--mono);color:var(--acc);margin-bottom:8px}.steps4 b{display:block;font:400 21px/1.2 var(--serif);margin-bottom:6px}
.steps4 p{margin:0;font-size:15px;color:#3d3a33}
.also{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.also div{border-top:1px solid var(--ink);padding-top:12px}.also h3{font-size:22px;margin:0 0 6px}.also p{margin:0;color:var(--mut);font-size:15px}
@media(max-width:900px){.cols,.also{grid-template-columns:1fr}.steps4{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.steps4{grid-template-columns:1fr}}
'''
    head = head.replace('%%CSS%%', css).replace('%%LD%%', ld(graph))
    body = ['<body>\n<a class="skip" href="#main">Skip to content</a>\n<div class="mast"><div class="wrap mono"><span>Eustace Crentsil</span><span>Services</span><span>Web developer · Accra</span></div></div>\n',
            nav('services'), '\n<main id="main">\n<header class="top"><div class="wrap">\n <p class="crumb mono"><a href="/">Home</a><span>/</span><span>Services</span></p>\n',
            ' <h1>Websites, web apps and automation, <em>delivered properly.</em></h1>\n',
            ' <p class="dek">I\'m a web developer and technical project manager based in Accra, Ghana. I work remotely with small businesses in Ghana, the US and worldwide: building the site or app, automating the busywork around it, and managing the project so it lands on time.</p>\n',
            ' <div class="actions"><a class="btn solid" href="/#contact">Start a project</a><a class="btn ghost" href="/work/">See my work</a></div>\n',
            ' <nav class="svcnav" aria-label="Services on this page">' + ''.join('<a href="#%s">%s. %s</a>' % (x['id'], x['n'], x['name']) for x in SVC) + '<a href="#start">How to start</a></nav>\n</div></header>\n']
    for x in SVC:
        li = lambda L: '<ul>' + ''.join('<li>%s</li>' % i for i in L) + '</ul>'
        body.append('''<section id="%s"><div class="wrap">
 <div class="sh"><span class="mono"><b>%s</b> / Service</span><h2>%s</h2></div>
 <div class="body"><span></span><div class="txt" style="max-width:none">
  <p style="max-width:680px"><b>Who it's for.</b> %s</p>
  <div class="cols">
   <div><h3>Problems it solves</h3>%s</div>
   <div><h3>What's included</h3>%s</div>
   <div><h3>What you get</h3>%s</div>
   <div><h3>How to start</h3><p>Send a short brief with what you need and, if you know it, your timeline. I'll reply with questions or a suggested first step, usually within a day.</p><p><a class="btn ghost" href="/#contact">Send a brief</a></p></div>
  </div>
  <p class="ex">%s</p>
 </div></div>
</div></section>
''' % (x['id'], x['n'], x['name'], x['who'], li(x['probs']), li(x['inc']), li(x['deliv']), x['ex']))
    body.append('''<section id="also"><div class="wrap">
 <div class="sh"><span class="mono">Alongside</span><h2>Also part of the work</h2></div>
 <div class="also">
  <div><h3>UI/UX design</h3><p>Clear, mobile-first pages that make it easy for visitors to find what they need and get in touch.</p></div>
  <div><h3>Hosting and cloud</h3><p>Setup on AWS, cPanel or Vercel, plus domains, email and backups.</p></div>
  <div><h3>Digital marketing basics</h3><p>Search-friendly pages, Google Business profile help and the analytics to see what works.</p></div>
 </div>
</div></section>
<section id="start"><div class="wrap">
 <div class="sh"><span class="mono">Process</span><h2>How a project starts</h2></div>
 <ol class="steps4">
  <li><b>Brief</b><p>You send a few lines about the business and what you need, through the form, email or WhatsApp.</p></li>
  <li><b>Call</b><p>We talk through goals, users and constraints. I ask a lot of questions here so nothing is guessed later.</p></li>
  <li><b>Scope and plan</b><p>I write down what will be built, what won't, and a timeline you can hold me to.</p></li>
  <li><b>Build, test, launch</b><p>Regular updates while I build, testing before launch, then support afterwards.</p></li>
 </ol>
 <aside class="ctab" aria-label="Start a project"><div><p class="mono">Based in Accra · working remotely with US and worldwide clients</p><h2 class="h3">Have a project in mind?</h2><p>Tell me what you're working on. "Not sure yet" is a fine answer for budget and timeline.</p></div><div class="b"><a class="btn solid" href="/#contact">Start a project</a><a class="btn ghost" href="https://wa.me/233546496092" target="_blank" rel="noopener">WhatsApp</a></div></aside>
</div></section>
</main>
''', )
    body.append(footer() + '\n</body>\n</html>\n')
    wr('services/index.html', head + ''.join(body))

def build_404():
    head = skeleton('Page not found · Eustace Crentsil', 'This page doesn\'t exist. Try the home page, services or work.', '/404', robots='noindex')
    head = head.replace('%%CSS%%', '.nf{padding:120px 0 40px}.nf .links{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}').replace('%%LD%%', '')
    head = re.sub(r'<meta property="og:url"[^>]*>', '', head)
    body = ('<body>\n<a class="skip" href="#main">Skip to content</a>\n<div class="mast"><div class="wrap mono"><span>Eustace Crentsil</span><span>404</span><span>Web developer</span></div></div>\n'
            + nav('') + '\n<main id="main"><div class="wrap nf">\n <p class="mono">Error 404</p>\n <h1>This page <em>doesn\'t exist.</em></h1>\n'
            ' <p class="dek">The link may be old or mistyped. Here are the main pages instead.</p>\n'
            ' <div class="links"><a class="btn solid" href="/">Home</a><a class="btn ghost" href="/services/">Services</a><a class="btn ghost" href="/work/">Work</a><a class="btn ghost" href="/#contact">Contact</a></div>\n</div></main>\n'
            + footer() + '\n</body>\n</html>\n')
    wr('404.html', head + body)

def build_seo():
    urls = ['/', '/services/', '/work/'] + ['/work/%s/' % x for x in SLUGS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        '  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, u, TODAY) for u in urls) + '</urlset>\n'
    wr('sitemap.xml', sm)
    wr('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)
    wr('vercel.json', json.dumps({"trailingSlash": True}, indent=2) + '\n')

build_home(); build_work(); build_services(); build_404(); build_seo()
print('patch4 done:', len(SLUGS), 'case pages')
