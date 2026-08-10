"""Erzeugt vorschau/index.html aus index.html.

Warum eine echte Kopie und keine Weiterleitung: Beim Ablegen auf dem
Startbildschirm liest iOS das Manifest aus dem ausgelieferten HTML. Eine
per JavaScript nachtraeglich geaenderte Adresse kommt zu spaet — die App
startete deshalb immer auf der normalen Seite und der Vorschaumodus war
weg. Die Kopie bringt ihr eigenes Manifest mit start_url auf sich selbst
mit, damit startet die abgelegte App im Vorschau-Ordner.

Nach jeder Aenderung an index.html neu ausfuehren:

    python build-vorschau.py
"""
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).parent
QUELLE = WURZEL / "index.html"
ZIEL = WURZEL / "vorschau" / "index.html"

# Dateien, die eine Ebene hoeher liegen, sobald die Seite in /vorschau/ steht
MITGELIEFERT = ["apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon.svg"]

HINWEIS = ("<!-- Erzeugt von build-vorschau.py — nicht von Hand aendern.\n"
           "     Quelle ist index.html; nach jeder Aenderung dort neu erzeugen. -->\n")


def bauen(text):
    ersetzungen = 0

    # Vorschau fest einschalten, statt sie aus dem Speicher zu lesen
    alt = 'const VORSCHAU = speicher.get("vorschaumodus", false);'
    neu = 'const VORSCHAU = true;   // in dieser Kopie fest eingeschaltet'
    if alt not in text:
        sys.exit("Abbruch: Zeile fuer den Vorschaumodus nicht gefunden. "
                 "Wurde index.html umgebaut?")
    text = text.replace(alt, neu)
    ersetzungen += 1

    # Bilder liegen eine Ebene hoeher
    for datei in MITGELIEFERT:
        vorher = text
        text = text.replace(f'href="{datei}"', f'href="../{datei}"')
        if text != vorher:
            ersetzungen += 1

    # Eigener Name, damit die beiden Symbole unterscheidbar bleiben
    text = text.replace("<title>Vámonos —", "<title>Vámonos Test —")
    text = text.replace('content="Vámonos"', 'content="Vámonos Test"')

    # Suchmaschinen sollen die Kopie erst recht nicht aufnehmen
    text = text.replace('<link rel="canonical"', '<link rel="nofollow-platzhalter"')

    if not re.search(r'<link rel="manifest" href="manifest\.webmanifest">', text):
        sys.exit("Abbruch: Manifest-Verweis nicht gefunden.")

    return HINWEIS + text, ersetzungen


def main():
    if not QUELLE.exists():
        sys.exit(f"Abbruch: {QUELLE} fehlt.")
    text, n = bauen(QUELLE.read_text(encoding="utf-8"))
    ZIEL.parent.mkdir(exist_ok=True)
    ZIEL.write_text(text, encoding="utf-8")
    print(f"{ZIEL.relative_to(WURZEL)} geschrieben — {n} Stellen angepasst, "
          f"{len(text) // 1024} KB")


if __name__ == "__main__":
    main()
