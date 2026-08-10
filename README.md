# Vámonos — Sieben Türchen bis Lateinamerika

Ein Countdown-Kalender mit sieben Türchen, die sich vom 10. bis 16. August 2026
täglich freischalten. Eine einzelne, in sich geschlossene HTML-Datei: keine
externen Abhängigkeiten, kein Build-Werkzeug, kein Framework.

## Adressen

| Zweck | Adresse |
|---|---|
| Für Katharina — es gilt das Datum | `https://jasperukert-code.github.io/reise-countdown/` |
| Zum Prüfen — alle Türchen offen | `https://jasperukert-code.github.io/reise-countdown/vorschau/` |

Ein einzelnes Türchen lässt sich direkt ansteuern, etwa
`…/vorschau/#t13` für den 13. August.

## Dateien

- `index.html` — die komplette Seite, Inhalt und Technik
- `vorschau/index.html` — **erzeugt**, nicht von Hand ändern
- `build-vorschau.py` — erzeugt die Vorschau aus `index.html`
- `icon.svg` — Quelle des App-Symbols (Gaucho zu Pferd)
- `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` — daraus gerenderte Symbole
- `manifest.webmanifest`, `vorschau/manifest.webmanifest` — je eines pro Variante

## Nach jeder Änderung an index.html

```bash
python build-vorschau.py
```

Sonst bleibt die Vorschau auf dem alten Stand.

**Warum eine Kopie und keine Weiterleitung:** Beim Ablegen auf dem
Startbildschirm liest iOS das Manifest aus dem ausgelieferten HTML. Eine per
JavaScript nachträglich gesetzte Adresse kommt zu spät — die abgelegte App
startete deshalb immer auf der normalen Seite, und der Vorschaumodus war weg.
Die Kopie bringt ihr eigenes Manifest mit `start_url` auf sich selbst mit.

## Symbole neu erzeugen

Nach Änderungen an `icon.svg` müssen die PNG-Dateien neu gerendert werden. Auf
dem Rechner ist kein SVG-Renderer installiert, das Skript zeichnet die Form
deshalb mit Pillow nach — beide Fassungen müssen zusammenpassen.
