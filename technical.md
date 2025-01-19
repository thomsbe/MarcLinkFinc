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

## Datenfluss
1. Einlesen der Marc21 Daten mit pymarc
2. Visualisierung der Rohdaten
3. Transformation in Pydantic-Modelle
4. Validierung durch LinkML-Schema
