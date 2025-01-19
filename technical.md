# Technische Entscheidungen

## Bibliotheken
- Python 3.13 als Basis
- pymarc für Marc21 Verarbeitung
- marimo für die interaktive Notebook-Umgebung
- pydantic für Datenvalidierung
- linkml für Schemamodellierung

## Projektstruktur
- Verwendung von `uv` als Paketmanager
- Installation als editierbares Paket (`pip install -e .`)
- Schema-Definitionen in `schema/*.yaml`
- Beispiel-Marc21-Record in `marc_example.py`

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

## Offene Punkte
- Integration der generierten Pydantic-Modelle
- Implementierung der Marc21-zu-Pydantic Transformation
- Entwicklung der Marimo-Notebook-Oberfläche
- Erweiterung des Schemas um weitere Marc21-Felder
