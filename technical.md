# Technische Entscheidungen

## Bibliotheken
- Python 3.12 als Basis
- pymarc für Marc21 Verarbeitung
- marimo für die interaktive Notebook-Umgebung
- pydantic für Datenvalidierung
- linkml für Schemamodellierung und Generierung der Modelle

## Projektstruktur
- Verwendung von `uv` als Paketmanager
- Schema-Definition in `schema/finc.yaml`
- Generierte Modelle in `models/`:
  - `pydantic.py`: Generierte Pydantic-Klassen
  - `dataclass.py`: Generierte Dataclasses
- Marimo Notebook in `notebook.py`

## Datenfluss
1. Einlesen oder Erstellen eines Marc21 Records
2. Visualisierung der Marc21 Daten
3. Umwandlung in JSON
4. Validierung und Mapping in Pydantic/Dataclass Modelle
5. Ausgabe als JSON

## Schema-Design (LinkML)
- Basis-Schema in `schema/finc.yaml`
- Fokus auf grundlegende Felder für den Showcase
- Validierungsregeln für Datenfelder

## Implementierungsstatus
- [ ] Grundlegende Projektstruktur
- [ ] LinkML Schema Definition
- [ ] Marc21 Beispieldaten
- [ ] Marimo Notebook
- [ ] Dokumentation

## Nächste Schritte
1. Erstellung des LinkML Schemas
2. Generierung der Modelle
3. Entwicklung des Marimo Notebooks
4. Dokumentation der Beispiele
