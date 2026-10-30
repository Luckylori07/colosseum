/* Segnala che JavaScript è attivo (serve a CSS per mostrare menu mobile e animazioni).
   File esterno, così la Content-Security-Policy non richiede script inline. */
document.documentElement.className += ' js';
