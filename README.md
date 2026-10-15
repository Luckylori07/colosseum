# Colosseum Azzate – proposta di sito (DEMO)

Sito statico multipagina (HTML + CSS + JS, nessun framework, nessuna dipendenza a runtime, nessun cookie, nessun tracking) per la palestra **Colosseum Azzate**, Via 1 Maggio 8, Azzate (VA).
Proposta realizzata da [Tramontis](https://tramontis.netlify.app/). **È una demo non ancora attiva.**

```
index.html            Home: hero, "Perché allenarti da noi", indice delle pagine
la-palestra.html      La palestra (testo, foto, corsi)
abbonamenti.html      Abbonamenti e ingressi
orari.html            Orari e indicatore "Aperto ora"
gallery.html          Gallery con lightbox
come-iniziare.html    Come iniziare (3 passi)
dove-siamo.html       Indirizzo, come arrivare, contatti
faq.html              Domande frequenti
privacy.html          Informativa privacy
assets/css/style.css  stile (colori e font in :root / @font-face)
assets/js/main.js     menu mobile, "Aperto ora", lightbox, reveal
assets/img/           logo, foto (WebP), favicon, og-image
assets/fonts/         Big Shoulders Display e Figtree (OFL), self-hosted
robots.txt  sitemap.xml  .nojekyll  go-live.sh
```

Per vederlo in locale: `python3 -m http.server 8000` nella cartella, poi <http://localhost:8000>.

## Modificare i dati

Header, footer e barra DEMO sono **ripetuti identici in ogni pagina** (nessun build): se cambi un contatto o una voce del menu, fai cerca-e-sostituisci su tutti i file `*.html`.

| Cosa | Dove |
| --- | --- |
| Telefono | cerca `0332` e `390332457667` (link `tel:`) in tutti i file `.html` |
| Email | cerca `club@colosseumazzate.it` |
| Indirizzo, P.IVA | `dove-siamo.html`, footer di ogni pagina, `privacy.html`, JSON-LD in `<head>` di `index.html` |
| Orari (testo) | `orari.html`, `faq.html`, footer, JSON-LD (`openingHoursSpecification`) |
| Orari (indicatore "Aperto ora") | oggetto `SCHEDULE` in `assets/js/main.js` (minuti dalla mezzanotte, `0` = domenica) |
| **Prezzi** | in `abbonamenti.html` cerca `data-price-slot`: sostituisci "Chiedi il prezzo in reception" con la cifra. Per gli ingressi, aggiungi il prezzo nel blocco `.entries__list` |
| **Corsi** | blocco `.corsi` in `la-palestra.html` e FAQ "Ci sono corsi?": ora dice "Chiedi in reception i corsi attivi" |
| Social | non inseriti (vedi report): aggiungi i link nella colonna "Contatti e orari" del footer |
| Colori | variabili in `:root` di `style.css`. Sfondo sempre scuro (`--ink`, `--ink-2`). `--green: #004723` è il verde del logo (footer e fasce); `--lit: #3bcb83` è la stessa tonalità più chiara, usata per CTA, numeri e linee su fondo scuro |
| Filtro sulle foto | classe `.tone` in `style.css` (scurisce e desatura leggermente + velo verde-grafite). Per una foto senza filtro togli `tone` dall'elemento. Il lightbox mostra la foto originale |

## Aggiungere o cambiare foto

1. Metti l'immagine in `assets/img/` in **WebP** (qualità ~84). Non ingrandirla oltre la sua risoluzione: le foto attuali sono 828–838 px di larghezza.
2. In `gallery.html` copia un blocco `<li class="g">…</li>` e cambia `data-full`, `data-w`, `data-h` (dimensioni reali), `data-caption`, `src`, `width`, `height` e il testo del `.g__cap`.
3. Le immagini sotto la prima schermata usano `loading="lazy"`; l'hero (`colosseum-04.webp`) no.
4. Se aggiungi/rimuovi foto, ricontrolla la griglia (classi `g--a`, `g--tall`, `g--b` in `style.css`).

Il logo (`logo.png`) è l'originale del sito vecchio (312×103): se hanno una versione vettoriale (SVG) o più grande, sostituiscilo.

## Come funziona la modalità DEMO e come toglierla

L'unico punto di controllo è l'attributo **`data-demo` sul `<body>`** (in tutte le pagine `.html`).

* `data-demo="on"` (attuale): sottile barra gialla fissa in alto (non chiudibile) e riga "Proposta di sito realizzata da Tramontis" e nota demo nel footer.
* `data-demo="off"`: tutto questo scompare (CSS) e `main.js` rimuove anche il `noindex` e il prefisso `[DEMO]` dal titolo.

**Per pubblicare la versione definitiva, in una sola mossa:**

```sh
./go-live.sh https://www.dominio-del-cliente.it
```

Lo script (su tutte le pagine `.html`): imposta `data-demo="off"`, elimina `<meta name="robots" content="noindex, nofollow">`, toglie `[DEMO] ` dal `<title>` e sostituisce il dominio (`og:image`, JSON-LD, `robots.txt`, `sitemap.xml`). Senza argomento spegne solo la demo e lascia `https://www.colosseumazzate.it` come dominio.

Se vuoi mantenere un credito all'agenzia dopo la vendita, rimetti nel footer un paragrafo normale (senza classe `demo-only`) con il link a Tramontis; altrimenti puoi cancellare i due `<p class="demo-only">`, la barra `.demo-bar` dall'HTML.

> Nota: finché la demo è attiva il `noindex` è nel codice HTML e i motori di ricerca non indicizzano la pagina. `robots.txt` permette la scansione apposta, altrimenti i crawler non potrebbero leggere il `noindex`.
>
> Le immagini `og:image`, il JSON-LD e `sitemap.xml` puntano già al dominio definitivo `https://www.colosseumazzate.it`: finché la demo sta su un altro dominio, l'anteprima social dell'immagine non si vedrà.

## Pubblicare

Sono solo file statici, con percorsi relativi:

* **GitHub Pages**: Settings → Pages → Deploy from a branch → `main` / root (c'è già `.nojekyll`).
* **Netlify / Cloudflare Pages / qualunque hosting**: carica la cartella così com'è (nessuna build). Con Netlify: "publish directory" = `.`, nessun build command.
* Hosting tradizionale (FTP): copia tutti i file nella root del dominio.

## Note tecniche

* Font self-hosted in `assets/fonts/` (licenza OFL inclusa): nessuna chiamata a Google Fonts.
* Nessuno script di terze parti, nessun cookie, nessun tracking → nessun cookie banner.
* La mappa è un **link** a Google Maps, non un iframe.
* "Aperto ora" usa il fuso `Europe/Rome` (anche se il visitatore è in un altro fuso) e gli orari ordinari.
* Animazioni (titolo, reveal, nastro) disattivate con `prefers-reduced-motion`.
