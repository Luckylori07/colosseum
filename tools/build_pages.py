# Genera le pagine statiche del sito (header/footer condivisi, immagini responsive, 404).
# Uso (dalla root della repo):  python3 -I tools/build_pages.py .
# ATTENZIONE: sovrascrive i file .html. Se modifichi un HTML a mano, riporta la modifica anche qui,
# altrimenti la prossima generazione la cancella. Non serve per pubblicare: il sito è già generato.
import sys, json, re
R = sys.argv[1]
SITE = "https://www.colosseumazzate.it/"

NAV = [("index.html","Home"),("la-palestra.html","La palestra"),("abbonamenti.html","Abbonamenti"),("orari.html","Orari"),("dove-siamo.html","Dove siamo")]
PHONE = '<svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>'
TEL = 'tel:+390332457667'
IG = 'https://www.instagram.com/colosseum_azzate/'
FB = 'https://www.facebook.com/colosseumazzate/?locale=it_IT'
def ico(n): return f'<svg class="ico" aria-hidden="true"><use href="#i-{n}"/></svg>'
EXT = 'target="_blank" rel="noopener noreferrer"'
BTN_IG = f'<a class="btn btn--ghost" href="{IG}" {EXT}>{ico("instagram")}Instagram</a>'
BTN_FB = f'<a class="btn btn--ghost" href="{FB}" {EXT}>{ico("facebook")}Facebook</a>'
MAIL = 'mailto:club@colosseumazzate.it?subject=Richiesta%20informazioni'

SPRITE = '''<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false">
  <defs>
    <symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></symbol>
    <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
    <symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 7l9 6 9-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"/></symbol>
    <symbol id="i-close" viewBox="0 0 24 24"><path d="M5 5l14 14M19 5L5 19" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"/></symbol>
    <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"/></symbol>
    <symbol id="i-instagram" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></symbol>
    <symbol id="i-facebook" viewBox="0 0 24 24"><path d="M17 3h-3a4 4 0 0 0-4 4v3H7v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></symbol>
  </defs>
</svg>'''

IG0 = "https://www.instagram.com/colosseum_azzate/"
FB0 = "https://www.facebook.com/colosseumazzate/?locale=it_IT"
JSONLD = json.dumps({
  "@context":"https://schema.org","@type":"HealthClub","name":"Colosseum Azzate","legalName":"Colosseum s.r.l.",
  "description":"Palestra ad Azzate con sala fitness ampia e luminosa, macchinari aerobici e isotonici, istruttori e programmi di allenamento personalizzati.",
  "url":SITE,"image":SITE+"assets/img/og-image.jpg","logo":SITE+"assets/img/logo.png",
  "telephone":"+39 0332 457667","email":"club@colosseumazzate.it","vatID":"IT03154860120",
  "address":{"@type":"PostalAddress","streetAddress":"Via 1 Maggio 8","postalCode":"21022","addressLocality":"Azzate","addressRegion":"VA","addressCountry":"IT"},
  "sameAs":[IG0,FB0],
  "hasMap":"https://maps.app.goo.gl/W76t9FUFrZ8XkWFo9",
  "openingHoursSpecification":[
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"22:00"},
    {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"18:00"},
    {"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"09:00","closes":"13:00"}]
}, ensure_ascii=False, indent=2)

def head(p):
    if p.get('noindex_always'):
        canon = '<meta name="robots" content="noindex">'
    else:
        canon = f'<link rel="canonical" href="{SITE}{"" if p["file"] == "index.html" else p["file"]}">'
    t = p["title"]
    og_title = p.get("og_title", t)
    extra = ""
    if p["file"] == "index.html":
        extra += '<link rel="preload" href="assets/img/sala-4.webp" as="image" type="image/webp">\n'
        extra += '<script type="application/ld+json">\n'+JSONLD+'\n</script>\n'
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="assets/js/init.js"></script>
<title>[DEMO] {t}</title>
<meta name="description" content="{p["desc"]}">
<!-- DEMO: rimuovere con go-live.sh (vedi README) -->
<meta name="robots" content="noindex, nofollow" id="demo-robots">
{canon}
<meta name="theme-color" content="#004723">

<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Colosseum Azzate">
<meta property="og:url" content="{SITE}{'' if p["file"] == 'index.html' else p["file"]}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:image" content="{SITE}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="La sala fitness di Colosseum Azzate">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">

<link rel="preload" href="assets/fonts/big-shoulders-display-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/figtree-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra}<link rel="stylesheet" href="assets/css/style.css">
</head>

<!-- DEMO: unico punto di controllo = attributo data-demo del body (on: demo visibile; off: sito definitivo). Vedi README. -->
<body data-demo="on" id="top">

{SPRITE}

<a class="skip" href="#contenuto">Vai al contenuto</a>

<div class="top">
  <div class="demo-bar" role="region" aria-label="Avviso versione demo">
    <p><strong>VERSIONE DEMO - Proposta di sito non ancora attiva.</strong> Per averla online sul vostro dominio contatta <a href="mailto:lorenzo.giarnetti@gmail.com?subject=Sito%20Colosseum%20Azzate">Lorenzo Giarnetti</a></p>
  </div>

  <header class="header">
    <div class="wrap header__row">
      <a class="header__logo" href="index.html" aria-label="Colosseum Azzate – home">
        <img src="assets/img/logo.png" width="312" height="103" alt="Colosseum Fitness &amp; Wellness">
      </a>
      <nav class="nav" id="menu" aria-label="Principale">
        <ul class="nav__list">
{chr(10).join(f'          <li><a href="{h}"' + (' aria-current="page"' if h == p["file"] else '') + f'>{l}</a></li>' for h,l in NAV)}
        </ul>
      </nav>
      <div class="header__social">
        <a href="{IG}" {EXT} aria-label="Instagram (si apre in una nuova scheda)">{ico("instagram")}</a>
        <a href="{FB}" {EXT} aria-label="Facebook (si apre in una nuova scheda)">{ico("facebook")}</a>
      </div>
      <button class="header__burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Apri il menu">
        <svg class="ico ico--lg" aria-hidden="true"><use href="#i-menu"/></svg>
      </button>
    </div>
  </header>
</div>

<main id="contenuto">
'''

def cta_band(title="Vieni a trovarci.", text="Via 1 Maggio 8, Azzate (VA) – ampio parcheggio.", second=None):
    second = second or '<a class="btn btn--ghost btn--lg" href="dove-siamo.html">Come arrivare</a>'
    return f'''
  <section class="cta s-ink2" aria-labelledby="cta-title">
    <div class="wrap cta__row">
      <div>
        <h2 id="cta-title">{title}</h2>
        <p>{text}</p>
      </div>
      <div class="cta__btns">
        <a class="btn btn--primary btn--lg" href="{TEL}">{PHONE}Chiama 0332 457667</a>
        {second}
      </div>
    </div>
  </section>
'''

def foot(p):
    return f'''</main>

<footer class="footer s-green">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="assets/img/logo.png" width="312" height="103" loading="lazy" alt="Colosseum Fitness &amp; Wellness">
        <p>La tua palestra ad Azzate. Aperti 365 giorni l'anno.</p>
      </div>
      <nav aria-label="Navigazione nel footer">
        <h2 class="footer__h">Navigazione</h2>
        <ul>
{chr(10).join(f'          <li><a href="{h}">{l}</a></li>' for h,l in NAV)}
          <li><a href="come-iniziare.html">Come iniziare</a></li>
          <li><a href="faq.html">Domande frequenti</a></li>
        </ul>
      </nav>
      <div>
        <h2 class="footer__h">Contatti e orari</h2>
        <ul>
          <li><a href="{TEL}">0332 457667</a></li>
          <li><a href="{MAIL}">club@colosseumazzate.it</a></li>
          <li><a href="{IG}" {EXT}>{ico("instagram")}Instagram</a></li>
          <li><a href="{FB}" {EXT}>{ico("facebook")}Facebook</a></li>
          <li>Lun-Ven 7:00-22:00</li>
          <li>Sabato 9:00-18:00</li>
          <li>Domenica 9:00-13:00</li>
        </ul>
      </div>
      <div>
        <h2 class="footer__h">Dati societari</h2>
        <ul>
          <li>Colosseum s.r.l.</li>
          <li>Via 1 Maggio 8, 21022 Azzate (VA)</li>
          <li>P.IVA 03154860120</li>
          <!-- TODO-LEGALE: aggiungere da visura camerale: Registro Imprese di Varese, n. REA, capitale sociale (i.v.), eventuale socio unico / stato di liquidazione (art. 2250 c.c.; art. 7 D.Lgs. 70/2003). go-live.sh si ferma finché questo commento è presente. -->
          <li><a href="privacy.html">Informativa sulla privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__legal">
      <p class="demo-only">Proposta di sito realizzata da <a href="mailto:lorenzo.giarnetti@gmail.com?subject=Sito%20Colosseum%20Azzate">Lorenzo Giarnetti</a></p>
      <p class="demo-only">Questa è una demo dimostrativa: il sito definitivo è disponibile su richiesta</p>
    </div>
  </div>
</footer>

<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def page_head(h1, lede=None, surf="s-ink"):
    lede_html = f'\n        <p class="sec__lede">{lede}</p>' if lede else ''
    return f'''  <section class="sec pagehead {surf}" aria-labelledby="page-title">
    <div class="wrap">
      <div class="sec__head">
        <h1 class="display" id="page-title">{h1}</h1>{lede_html}
      </div>
'''

STATUS = '''<div class="status status--big" data-status>
          <span class="status__dot" aria-hidden="true"></span>
          <span class="status__text"><strong data-status-label>Orari di apertura</strong><span data-status-detail>Lun-Ven 7:00-22:00</span></span>
        </div>'''

pages = []

# ---------------- HOME ----------------
home = {"file":"index.html","title":"Palestra ad Azzate (VA) – Colosseum Azzate",
        "og_title":"Colosseum Azzate – La tua palestra ad Azzate",
        "desc":"Colosseum Azzate: palestra ad Azzate (VA) con sala fitness ampia e luminosa, macchinari aerobici e isotonici, istruttori e programmi personalizzati. Aperti 365 giorni l'anno."}
home["body"] = f'''
  <section class="hero s-ink" aria-labelledby="hero-title">
    <div class="wrap hero__grid">
      <div class="hero__copy">
        <h1 class="hero__title" id="hero-title">
          <span>La tua</span>
          <span>palestra</span>
          <span>ad Azzate.</span>
        </h1>
        <p class="hero__lede">Aperta 365 giorni l'anno. <br> Sala fitness ampia e luminosa, macchinari aerobici e isotonici. Istruttori professionisti creano il tuo allenamento personalizzato.</p>
        <div class="hero__cta">
          <a class="btn btn--primary btn--lg" href="{TEL}">{PHONE}Chiama 0332 457667</a>
          <a class="btn btn--ghost btn--lg" href="abbonamenti.html">Vedi gli abbonamenti</a>
        </div>
      </div>
      <figure class="hero__photo">
        <img src="assets/img/sala-4.webp" width="1400" height="934" alt="La sala fitness di Colosseum Azzate: macchinari isotonici sul parquet, con le pareti verdi e le grandi vetrate">
        <div class="status status--on-photo" data-status>
          <span class="status__dot" aria-hidden="true"></span>
          <span class="status__text"><strong data-status-label>Orari di apertura</strong><span data-status-detail>Lun-Ven 7:00-22:00</span></span>
        </div>
      </figure>
    </div>
  </section>

  <div class="marquee s-green" role="group" aria-label="In breve">
    <div class="marquee__track">
''' + "".join(f'''      <ul class="marquee__group"{' aria-hidden="true"' if i else ''}>
        <li>Aperti 365 giorni l'anno</li>
        <li>Ampio parcheggio</li>
        <li>Programmi personalizzati</li>
        <li>Macchinari aerobici e isotonici</li>
        <li>Sala ampia e luminosa</li>
        <li>Istruttori che ti consigliano</li>
      </ul>
''' for i in range(2)) + f'''    </div>
  </div>

  <section class="sec s-ink2" aria-labelledby="perche-title">
    <div class="wrap">
      <div class="sec__head">
        <h2 class="display" id="perche-title">Perché allenarti<br>da noi?</h2>
      </div>
      <ol class="reasons" data-reveal>
        <li class="reason"><span class="num" aria-hidden="true">01</span><h3>Aperti 365 giorni l'anno</h3><p>Anche la domenica e nei giorni festivi: la palestra è sempre aperta.</p></li>
        <li class="reason"><span class="num" aria-hidden="true">02</span><h3>Sala ampia e luminosa</h3><p>Uno spazio ampio, con tanta luce, in cui allenarti bene.</p></li>
        <li class="reason"><span class="num" aria-hidden="true">03</span><h3>Macchinari aerobici e isotonici</h3><p>Hai a disposizione tutti i macchinari per gli allenamenti di forza e il cardio</p></li>
        <li class="reason"><span class="num" aria-hidden="true">04</span><h3>Istruttori che ti consigliano</h3><p>Sempre a tua disposizione per aiutarti a raggiungere i tuoi obiettivi.</p></li>
        <li class="reason"><span class="num" aria-hidden="true">05</span><h3>Programmi personalizzati</h3><p>Allenamenti studiati e personalizzati in base alle tue esigenze.</p></li>
        <li class="reason"><span class="num" aria-hidden="true">06</span><h3>Ampio parcheggio</h3><p>La palestra è circondata da un ampio parcheggio: arrivi e parcheggi senza pensieri.</p></li>
      </ol>
    </div>
  </section>

  <section class="sec s-ink" aria-labelledby="hub-title">
    <div class="wrap">
      <div class="sec__head">
        <h2 class="display" id="hub-title">Scopri<br>Colosseum.</h2>
      </div>
      <ul class="hub" data-reveal>
        <li><a class="hub__item" href="la-palestra.html"><h3>La palestra<svg class="hub__arrow" aria-hidden="true"><use href="#i-arrow"/></svg></h3><p>La sala fitness, i macchinari e gli istruttori.</p></a></li>
        <li><a class="hub__item" href="abbonamenti.html"><h3>Abbonamenti<svg class="hub__arrow" aria-hidden="true"><use href="#i-arrow"/></svg></h3><p>Full-time, Part-time e formula a ingressi.</p></a></li>
        <li><a class="hub__item" href="orari.html"><h3>Orari<svg class="hub__arrow" aria-hidden="true"><use href="#i-arrow"/></svg></h3><p>Aperti 365 giorni l'anno. Controlla se siamo aperti ora.</p></a></li>
        <li><a class="hub__item" href="come-iniziare.html"><h3>Come iniziare<svg class="hub__arrow" aria-hidden="true"><use href="#i-arrow"/></svg></h3><p>Tre passi per cominciare ad allenarti.</p></a></li>
        <li><a class="hub__item" href="dove-siamo.html"><h3>Dove siamo<svg class="hub__arrow" aria-hidden="true"><use href="#i-arrow"/></svg></h3><p>Via 1 Maggio 8, Azzate, con ampio parcheggio.</p></a></li>
        <li><div class="hub__item"><h3>Seguici</h3><p>Ci trovi su <a href="{IG}" {EXT}>Instagram</a> e su <a href="{FB}" {EXT}>Facebook</a>.</p></div></li>
      </ul>
    </div>
  </section>
'''
pages.append(home)

# ---------------- LA PALESTRA ----------------
pal = {"file":"la-palestra.html","title":"La palestra – Colosseum Azzate",
       "desc":"La sala fitness di Colosseum Azzate: area pesi con rack, panche e manubri, macchine isotoniche, saletta per il corpo libero, spogliatoi con docce calde. Aperti 365 giorni l'anno."}
pal["body"] = page_head("Una sala ampia e luminosa.") + f'''      <div class="palestra">
        <div class="palestra__text">
          <p>Un'<strong>area pesi</strong> ben fornita: rack per i pesi, panche, bilancieri e dischi, manubri e un'ampia selezione di <strong>macchine isotoniche</strong> per ogni gruppo muscolare. Attrezzi di alta qualità, robusti e affidabili, con prese e corde per esercizi diversi.</p>
          <p>Diversi macchinari per il <strong>cardio</strong> e una <strong>saletta dedicata per il corpo libero</strong>, con tappetini e attrezzi. Gli istruttori sono sempre a tua disposizione per consigli e spiegazioni sugli esercizi. </p>
          <p>Dopo l'allenamento ti aspettano spogliatoi con armadietti a chiusura automatica e docce calde.</p>
        </div>
        <figure class="ph"><img src="assets/img/sala-1.webp" width="1400" height="934" alt="La sala pesi: il rack dei manubri, le panche e la parete a specchio con la fascia verde"></figure>
      </div>
      <div class="palestra__row">
        <figure class="ph"><img src="assets/img/sala-2.webp" width="1400" height="934" loading="lazy" alt="Una zona con il rack per i pesi liberi, i dischi e le pareti verdi"></figure>
        <figure class="ph"><img src="assets/img/sala-3.webp" width="1400" height="938" loading="lazy" alt="Macchinari per la forza sul parquet, sotto le finestre della sala"></figure>
        <figure class="ph"><img src="assets/img/sala-4.webp" width="1400" height="934" loading="lazy" alt="Macchinari isotonici, con un grande disco in primo piano, e le vetrate sul verde"></figure>
        <figure class="ph"><img src="assets/img/sala-5.webp" width="1400" height="934" loading="lazy" alt="Le macchine isotoniche in fila, con le colonne verdi e le finestre"></figure>
        <figure class="ph"><img src="assets/img/sala-6.webp" width="1400" height="934" loading="lazy" alt="La leg press e gli altri macchinari della sala, con il parquet"></figure>
        <figure class="ph"><img src="assets/img/spogliatoi.webp" width="838" height="557" loading="lazy" alt="Gli spogliatoi con gli armadietti e le panche"></figure>
      </div>
    </div>
  </section>
''' + cta_band(text="Via 1 Maggio 8, Azzate (VA)")
pages.append(pal)

# ---------------- ORARI ----------------
ora = {"file":"orari.html","title":"Orari di apertura – Colosseum Azzate",
       "desc":"Orari della palestra Colosseum Azzate, aperta 365 giorni l'anno: lunedì-venerdì 7:00-22:00, sabato 9:00-18:00, domenica 9:00-13:00."}
ora["body"] = f'''  <section class="sec pagehead s-ink" aria-labelledby="page-title">
    <div class="wrap">
      <div class="sec__head sec__head--split">
        <h1 class="display" id="page-title">Aperti 365<br>giorni l'anno.</h1>
        {STATUS}
      </div>
      <ul class="hours" data-reveal>
        <li class="hours__item" data-days="1,2,3,4,5"><h2 class="hours__day">Lunedì – Venerdì</h2><p class="hours__time"><time datetime="07:00">7:00</time>–<time datetime="22:00">22:00</time></p></li>
        <li class="hours__item" data-days="6"><h2 class="hours__day">Sabato</h2><p class="hours__time"><time datetime="09:00">9:00</time>–<time datetime="18:00">18:00</time></p></li>
        <li class="hours__item" data-days="0"><h2 class="hours__day">Domenica</h2><p class="hours__time"><time datetime="09:00">9:00</time>–<time datetime="13:00">13:00</time></p></li>
      </ul>
      <p class="note"><strong>Aperti 365 giorni l'anno</strong>, domeniche e festivi compresi.</p>
    </div>
  </section>
''' + cta_band()
pages.append(ora)

# ---------------- ABBONAMENTI ----------------
TBD = '<dd class="prices__tbd" data-price-slot><span aria-hidden="true">€ ––</span><span class="sr-only">prezzo in definizione</span></dd>'
def price_dd(v):
    return TBD if v is None else f'<dd class="prices__set"><span class="amt">{v}</span><span class="cur"> €</span></dd>'
def plan(name, desc, img, alt, key, prices):
    rows = "\n".join(f'              <div class="prices__row"><dt>{lab}</dt>{price_dd(v)}</div>' for lab, v in prices)
    return f'''        <article class="plan">
          <div class="plan__media"><img src="assets/img/{img}" width="1400" height="934" alt="{alt}"></div>
          <div class="plan__body">
            <h2 class="plan__name">{name}</h2>
            <p class="plan__desc">{desc}</p>
            <div role="group" aria-label="Prezzi {name}"><dl class="prices">
{rows}
            </dl></div>
            <div class="plan__price">
              <a class="btn btn--primary" href="{TEL}">{PHONE}Chiama 0332 457667</a>
            </div>
          </div>
        </article>
'''
abb = {"file":"abbonamenti.html","title":"Abbonamenti – Colosseum Azzate",
       "desc":"Abbonamenti Full-time e Part-time da 1, 3, 6 o 12 mesi (Full-time 12 mesi: 330 €), ingresso singolo e pacchetti da 10, 20 e 50 ingressi."}
abb["body"] = page_head("Scegli come<br>allenarti.", "Due tipi di abbonamento per la sala fitness, in base ai tuoi orari. Poi scegli tra la formula ad abbonamento o quella ad ingressi.") + '''      <div class="plans">
''' + plan("Full-time","Accesso libero alla sala fitness, senza vincoli di orario.","sala-5.webp","Le macchine isotoniche della sala fitness, con le colonne verdi e le finestre","full",[("1 mese",None),("3 mesi",None),("6 mesi",None),("12 mesi",330)]) \
 + plan("Part-time","Fascia ridotta: accesso alla sala fitness dalle 9:00 alle 15:30.","sala-3.webp","Macchinari per la forza sul parquet, illuminati dalla luce delle finestre","pt",[("1 mese",None),("3 mesi",None),("6 mesi",None),("12 mesi",None)]) + '''      </div>

      <div class="entries">
        <div class="entries__intro">
          <h2>Preferisci gli ingressi?</h2>
          <p>Puoi scegliere un ingresso singolo oppure un pacchetto, con validità diversa.</p>
        </div>
        <ul class="entries__list">
          <li><span class="num" aria-hidden="true">1</span><strong>Ingresso singolo</strong><span class="entries__price" data-price-slot><span aria-hidden="true">€ ––</span><span class="sr-only">prezzo in definizione</span></span></li>
          <li><span class="num" aria-hidden="true">10</span><strong>10 ingressi</strong><span>validità 4 mesi</span><span class="entries__price" data-price-slot><span aria-hidden="true">€ ––</span><span class="sr-only">prezzo in definizione</span></span></li>
          <li><span class="num" aria-hidden="true">20</span><strong>20 ingressi</strong><span>validità 6 mesi</span><span class="entries__price" data-price-slot><span aria-hidden="true">€ ––</span><span class="sr-only">prezzo in definizione</span></span></li>
          <li><span class="num" aria-hidden="true">50</span><strong>50 ingressi</strong><span>validità 12 mesi</span><span class="entries__price" data-price-slot><span aria-hidden="true">€ ––</span><span class="sr-only">prezzo in definizione</span></span></li>
        </ul>
      </div>
    </div>
  </section>
''' + cta_band("Parlane con noi.", "Chiamaci o passa in reception per scegliere l'abbonamento giusto.")
pages.append(abb)

# ---------------- COME INIZIARE ----------------
com = {"file":"come-iniziare.html","title":"Come iniziare – Colosseum Azzate",
       "desc":"Come iniziare in palestra a Colosseum Azzate in tre passi: chiamaci o passa a trovarci, parla con un istruttore, scegli l'abbonamento."}
com["body"] = page_head("Come iniziare.") + f'''      <ol class="steps" data-reveal>
        <li class="step"><span class="num" aria-hidden="true">01</span><h2>Chiamaci o passa a trovarci</h2><p>Telefona allo 0332 457667 oppure vieni in Via 1 Maggio 8, negli orari di apertura.</p></li>
        <li class="step"><span class="num" aria-hidden="true">02</span><h2>Parli con un istruttore</h2><p>Gli racconti i tuoi obiettivi: ti consiglia come raggiungerli e studia un programma su misura.</p></li>
        <li class="step"><span class="num" aria-hidden="true">03</span><h2>Scegli l'abbonamento</h2><p>Full-time o Part-time, a mesi oppure a ingressi: scegli la formula adatta ai tuoi orari.</p></li>
      </ol>
      <div class="start__cta">
        <a class="btn btn--primary btn--lg" href="{TEL}">{PHONE}Chiama 0332 457667</a>
        <a class="btn btn--ghost btn--lg" href="{IG}" {EXT}>{ico("instagram")}Instagram</a>
        <a class="btn btn--ghost btn--lg" href="{FB}" {EXT}>{ico("facebook")}Facebook</a>
      </div>
    </div>
  </section>
'''
pages.append(com)

# ---------------- DOVE SIAMO ----------------
dov = {"file":"dove-siamo.html","title":"Dove siamo – Colosseum Azzate",
       "desc":"Colosseum Azzate si trova in Via 1 Maggio 8, Azzate (VA), con ampio parcheggio. Telefono 0332 457667."}
dov["body"] = page_head("Dove siamo.", surf="s-ink pagehead--flush") + f'''    </div>
  </section>

  <figure class="outside tone">
    <img src="assets/img/esterno.webp" width="1797" height="401" alt="L'esterno della palestra: l'edificio con le vetrate, il giardino recintato e l'insegna Colosseum Fitness &amp; Wellness">
  </figure>

  <section class="sec s-ink" aria-label="Indirizzo e contatti">
    <div class="wrap">
      <div class="where">
        <div class="where__block">
          <h2>Indirizzo</h2>
          <address><strong>Colosseum s.r.l.</strong><br>Via 1 Maggio 8<br>21022 Azzate (VA)</address>
          <a class="btn btn--primary" href="https://maps.app.goo.gl/W76t9FUFrZ8XkWFo9" target="_blank" rel="noopener"><svg class="ico" aria-hidden="true"><use href="#i-pin"/></svg>Apri in Google Maps</a>
        </div>
        <div class="where__block">
          <h2>Come arrivare</h2>
          <p>Ti consigliamo di utilizzare l'ingresso su Via Piave, la provinciale per Daverio. Ci trovi alla fine di Azzate, subito prima della rotonda per Daverio.</p>
          <p>La palestra è circondata da un ampio parcheggio.</p>
        </div>
        <div class="where__block">
          <h2>Contatti</h2>
          <ul class="contacts">
            <li><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg><a href="{TEL}">0332 457667</a></li>
            <li><svg class="ico" aria-hidden="true"><use href="#i-mail"/></svg><a href="{MAIL}">club@colosseumazzate.it</a></li>
            <li>{ico("instagram")}<a href="{IG}" {EXT}>Instagram</a></li>
            <li>{ico("facebook")}<a href="{FB}" {EXT}>Facebook</a></li>
          </ul>
        </div>
      </div>
    </div>
  </section>
'''
pages.append(dov)

# ---------------- FAQ ----------------
faqs = [
 ("Quali sono gli orari di apertura?","Dal lunedì al venerdì dalle 7:00 alle 22:00, il sabato dalle 9:00 alle 18:00, la domenica dalle 9:00 alle 13:00."),
 ("Siete aperti anche nei giorni festivi?","Sì, siamo aperti 365 giorni l'anno."),
 ("Che tipi di abbonamento ci sono?","Per la sala fitness puoi scegliere tra Full-time, con ingresso libero senza vincoli di orario, e Part-time, con ingresso dalle 9:00 alle 15:30. Entrambi sono disponibili da 1, 3, 6 o 12 mesi."),
 ("Posso venire senza abbonamento?","Sì, esiste la formula ad ingressi: ingresso singolo, oppure pacchetto da 10 ingressi (validità 4 mesi), da 20 (6 mesi) o da 50 (12 mesi)."),
 ("Quanto costa?",f'L\'abbonamento Full-time da 12 mesi costa 330 €. Per gli altri abbonamenti e per gli ingressi chiedi i prezzi in reception: <a href="{TEL}">0332 457667</a>.'),
 ("C'è parcheggio?","Sì, la palestra è circondata da un ampio parcheggio."),
 ("Posso avere un programma di allenamento personalizzato?","Sì, gli istruttori ti consigliano e studiano programmi di allenamento personalizzati, mirati alle tue esigenze. Per i dettagli contattaci in reception."),
]
faq = {"file":"faq.html","title":"Domande frequenti – Colosseum Azzate",
       "desc":"Domande frequenti su orari, abbonamenti, ingressi, parcheggio e programmi personalizzati di Colosseum Azzate."}
faq["body"] = page_head("Domande<br>frequenti.") + '      <div class="faq__list">\n' + "".join(f'        <details><summary>{q}</summary><p>{a}</p></details>\n' for q,a in faqs) + '''      </div>
    </div>
  </section>
''' + cta_band("Altre domande?", "Chiamaci, passa a trovarci o scrivici sui social.", second=BTN_IG.replace("btn btn--ghost","btn btn--ghost btn--lg")+BTN_FB.replace("btn btn--ghost","btn btn--ghost btn--lg"))
pages.append(faq)

# ---------------- 404 ----------------
nf = {"file":"404.html","title":"Pagina non trovata – Colosseum Azzate","desc":"La pagina che cerchi non esiste o è stata spostata.","noindex_always":True}
nf["body"] = page_head("Pagina non<br>trovata.", "Il link che hai seguito non esiste più o è stato spostato. Puoi tornare alla home o scegliere una delle pagine del menu.") + f'''      <div class="start__cta">
        <a class="btn btn--primary btn--lg" href="index.html">Torna alla home</a>
        <a class="btn btn--ghost btn--lg" href="{TEL}">Chiama 0332 457667</a>
      </div>
    </div>
  </section>
'''
pages.append(nf)

# ---------------- PRIVACY ----------------
pri = {"file":"privacy.html","title":"Informativa sulla privacy – Colosseum Azzate",
       "desc":"Informativa sulla privacy del sito di Colosseum Azzate: nessun cookie, nessun tracciamento, nessun dato personale raccolto dal sito."}
pri["body"] = f'''  <section class="doc s-ink">
    <div class="wrap">
      <div class="doc__body">
      <h1>Informativa sulla privacy</h1>
      <p>Questa informativa spiega in modo semplice come questo sito tratta i tuoi dati. Ultimo aggiornamento: ottobre 2026.</p>

      <h2>Titolare del trattamento</h2>
      <p>Colosseum s.r.l.<br>Via 1 Maggio 8, 21022 Azzate (VA)<br>P.IVA 03154860120<br>Telefono: <a href="{TEL}">0332 457667</a><br>E-mail: <a href="mailto:club@colosseumazzate.it">club@colosseumazzate.it</a></p>

      <h2>Cosa raccoglie il sito</h2>
      <p>Il sito non raccoglie dati personali. Non ha moduli da compilare, non ha aree riservate, non usa cookie, non usa strumenti di analisi o di tracciamento e non mostra pubblicità. Per questo non c'è nessun banner dei cookie.</p>
      <p>I caratteri tipografici sono ospitati sul sito stesso: aprendo le pagine il tuo browser non contatta servizi di terze parti per scaricarli.</p>

      <h2>Se ci contatti</h2>
      <p>Se ci scrivi un'e-mail o ci chiami con i link "Chiama" e "Scrivici" presenti nel sito, i dati che ci comunichi (ad esempio nome, numero di telefono, indirizzo e-mail e contenuto del messaggio) sono usati solo per rispondere alla tua richiesta. Il trattamento si basa sulla tua richiesta di contatto (art. 6, par. 1, lett. b e f del Regolamento UE 2016/679, "GDPR"). Non li cediamo a terzi per finalità di marketing.</p>

      <h2>Link verso altri siti</h2>
      <p>Il sito contiene link a Google Maps, Instagram e Facebook. Non incorpora né la mappa né i social: se clicchi su uno di questi link, lasci questo sito e si applicano le regole sulla privacy del servizio scelto.</p>

      <h2>Server e registri tecnici</h2>
      <p>Come ogni sito, il servizio che lo ospita può registrare per breve tempo dati tecnici di navigazione (ad esempio l'indirizzo IP) per garantire sicurezza e funzionamento. Il titolare non li usa per identificarti.</p>

      <h2>I tuoi diritti</h2>
      <p>Puoi chiedere al titolare l'accesso ai tuoi dati, la rettifica, la cancellazione, la limitazione o l'opposizione al trattamento (artt. 15-22 GDPR) scrivendo a <a href="mailto:club@colosseumazzate.it">club@colosseumazzate.it</a>. Puoi inoltre presentare reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it/" target="_blank" rel="noopener">garanteprivacy.it</a>).</p>

      <p><a class="back" href="index.html">Torna alla home</a></p>
      </div>
    </div>
  </section>
'''
pages.append(pri)

SIZES = {"hero__photo": "(min-width: 960px) 494px, 100vw",
         "palestra": "(min-width: 960px) 640px, 100vw",
         "palestra__row": "(min-width: 640px) 33vw, 100vw",
         "plan__media": "(min-width: 960px) 570px, 100vw"}
def responsive(html):
    def sub(m):
        pre = html[:m.start()]
        ctx = max(SIZES, key=lambda k: pre.rfind('class="'+k) if pre.rfind('class="'+k) >= 0 else -1)
        n = m.group(1)
        extra = ' fetchpriority="high"' if ctx == "hero__photo" else ''
        return f'<img src="assets/img/sala-{n}.webp" srcset="assets/img/sala-{n}-800.webp 800w, assets/img/sala-{n}.webp 1400w" sizes="{SIZES[ctx]}"{extra} width="1400"'
    return re.sub(r'<img src="assets/img/sala-(\d)\.webp" width="1400"', sub, html)
def nbsp_phone(html):
    parts = re.split(r'(<script type="application/ld\+json">.*?</script>)', html, flags=re.S)
    return "".join(p if p.startswith('<script type="application/ld+json">') else re.sub(r'(?<![+\d])0332 457667(?![^<]*"\s*>)', '0332&nbsp;457667', p) for p in parts)
for p in pages:
    html = head(p)+p["body"]+foot(p)
    html = nbsp_phone(responsive(html))
    open(f'{R}/{p["file"]}','w',encoding='utf8').write(html)
    print('scritto', p["file"])
