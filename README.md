# MarcLinkFinc

Ein interaktives Tool zur Visualisierung und Transformation von Marc21-Daten in validierte JSON-Strukturen.

## Projektbeschreibung

MarcLinkFinc ist ein Werkzeug, das den Prozess der Transformation von Marc21-Bibliotheksdaten in strukturierte JSON-Daten visualisiert und vereinfacht. Es nutzt LinkML für die Schemamodellierung und Pydantic für die Datenvalidierung.

### Hauptfunktionen

- Visualisierung von Marc21-Datensätzen
- Interaktive Transformation in JSON
- Schema-basierte Validierung
- Marimo-basierte Benutzeroberfläche

## Installation

1. Python 3.13 oder höher wird benötigt
2. Projekt klonen:
   ```bash
   git clone https://github.com/yourusername/MarcLinkFinc.git
   cd MarcLinkFinc
   ```
3. Abhängigkeiten installieren:
   ```bash
   uv pip install -e .
   uv pip install linkml pymarc marimo
   ```

## Entwicklungsstand

Das Projekt befindet sich in aktiver Entwicklung. Aktuell implementierte Funktionen:

- [x] Marc21 Beispiel-Record
- [x] LinkML Schema für Grunddaten
- [ ] Pydantic Modell-Integration
- [ ] Marimo Notebook-Interface
- [ ] Marc21-zu-JSON Transformation

Weitere Details zur technischen Implementierung finden Sie in der [technical.md](technical.md).

## Verwendung

Beispiel für die Erstellung eines Marc21-Records:
```python
from marc_example import create_example_record

record = create_example_record()
print(record)
```

## Lizenz

[Ihre gewählte Lizenz]
