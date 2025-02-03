# Technische Entscheidungen

## Bibliotheken
- Python 3.12 als Basis
- pymarc für Marc21 Verarbeitung
- marimo für die interaktive Notebook-Umgebung
- pydantic für Datenvalidierung
- linkml für Schemamodellierung

## Projektstruktur
- Verwendung von `uv` als Paketmanager
- Installation als editierbares Paket (`pip install -e .`)
- Schema-Definitionen in `schema/*.yaml`
- Marimo Notebooks in `notebooks/`:
  1. `01_marc21_to_json.py`: Marc21 Import und JSON Konvertierung
  2. `02_linkml_schema.py`: LinkML Schema und Pydantic Klassen
  3. `03_json_to_pydantic.py`: Validierung und Konvertierung

## Datenfluss
1. Einlesen der Marc21 Daten mit pymarc
2. Visualisierung der Rohdaten
3. Transformation in Pydantic-Modelle
4. Validierung durch LinkML-Schema

## Schema-Design (LinkML)
- Basis-Schema für Buchmetadaten in `schema/book.yaml`
- Mapping von Marc21-Feldern:
  - 245$a → title (Pflichtfeld)
  - 245$b → subtitle (Optional)
  - 100$a → author (Pflichtfeld, Format: "Nachname, Vorname")
  - 100$d → author_dates (Optional)
  - 020$a → isbn (Pflichtfeld, ISBN-13 Format)

## Generierung der Modelle
- Verwendung von `linkml-data-model` für die Generierung der Pydantic-Klassen
- Befehl: `linkml-data-model --output-formats pydantic schema/book.yaml > models.py`

## Implementierungsstatus
- [x] Grundlegende Projektstruktur
- [x] LinkML Schema Definition
- [x] Marimo Notebooks erstellt
- [ ] Marc21 Beispieldaten integriert
- [ ] Vollständige Validierung implementiert
- [ ] UI/UX Optimierung
- [ ] Dokumentation vervollständigt
