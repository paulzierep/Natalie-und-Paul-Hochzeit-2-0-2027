# Natalie & Paul · Hochzeit 2.0 · 2027

Unsere deutschsprachige Hochzeitswebsite mit Informationen zur Feier auf Pfarrers Älpele, zur Anreise und zum Übernachten.

**Website:** https://paulzierep.github.io/Natalie-und-Paul-Hochzeit-2-0-2027/

## Informationen ergänzen

1. [`index.html`](index.html) öffnen und auf das Stiftsymbol klicken.
2. Die gewünschten Texte ändern, z. B. Datum, Ablauf oder Unterkünfte. Die Bereiche sind nach ihren Überschriften gegliedert.
3. Änderung auf `main` speichern. Unter **Actions** lässt sich die automatische Prüfung und Veröffentlichung verfolgen.

Unbekannte Angaben sind ausdrücklich als offen beschrieben. Verlinkt sind der Ort der Feier auf Pfarrers Älpele, der Ausgangspunkt für den gemeinsamen Aufstieg sowie das Kolping-Feriendorf Ebnit als Übernachtungsmöglichkeit (Website und Google Maps). Verfügbarkeit und Konditionen müssen direkt mit der Unterkunft geklärt werden.

Farben und Gestaltung stehen in [`style.css`](style.css). Die Website verwendet lokale Systemschriften, keine externen Bilder, keine eingebetteten Karten und keine Analysewerkzeuge. Beim Aufruf gelten die technischen Datenverarbeitungsbedingungen von GitHub Pages; der Kartenlink führt erst nach Anklicken zu Google Maps.

**Datenschutz:** Dieses Repository und die Website sind öffentlich. Private Telefonnummern, Gästelisten oder vertrauliche Informationen nicht hier veröffentlichen.

## Automatische Veröffentlichung

Der Workflow [„Website prüfen und veröffentlichen“](.github/workflows/pages.yml) prüft jede Änderung und jeden Pull Request. Änderungen auf `main` werden anschließend automatisch über GitHub Pages veröffentlicht. Pull Requests veröffentlichen nichts.

Unter **Settings → Pages → Build and deployment → Source** muss **GitHub Actions** ausgewählt sein.

## Lokal ansehen und prüfen

```bash
python3 scripts/check_site.py
python3 -m http.server 8000
```

Danach http://localhost:8000 öffnen. Für die Website sind weder ein Paketmanager noch zusätzliche Bibliotheken erforderlich.
