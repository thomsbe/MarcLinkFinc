# Technische Entscheidungen

## Bibliotheken
- Python 3.12 als Basis
- pymarc für Marc21 Verarbeitung
- marimo für die interaktive Notebook-Umgebung
- pydantic für Datenvalidierung
- linkml für Schemamodellierung und Generierung der Modelle
- click für moderne Kommandozeilen-Interfaces
- tomlkit für TOML-Konfigurationen

## Projektstruktur
- Verwendung von `uv` als Paketmanager
- Schema-Definition in `schema/finc.yaml`
- Generierte Modelle in `models/`:
  - `pydantic.py`: Generierte Pydantic-Klassen
  - `dataclass.py`: Generierte Dataclasses
- Marimo Notebook in `notebook.py`
- Zentrale Logging-Konfiguration in `help/logging.py`

## Logging-Konfiguration
- Zentraler Logger über `getSlubLogger()`
- Konfiguration via TOML-Datei oder eingebetteter Standard-Konfiguration
- Zwei Handler:
  - Console-Handler (INFO-Level)
  - File-Handler (DEBUG-Level)
- Standardisiertes Logging-Format mit Zeitstempel, Logger-Name, Level und Nachricht

## Datenfluss
1. Einlesen oder Erstellen eines Marc21 Records
2. Visualisierung der Marc21 Daten
3. Umwandlung in JSON
4. Validierung und Mapping in Pydantic/Dataclass Modelle
5. Ausgabe in separaten JsonL-Dateien:
   - `{basename}.pydantic.jsonl`: Enthält die validierten Pydantic-Modelle
   - `{basename}.dataclass.jsonl`: Enthält die entsprechenden Dataclass-Modelle

## Ausgabeformat
- Verwendung von JsonL (JSON Lines) für die Ausgabe
- Ein JSON-Objekt pro Zeile ohne umschließendes Array
- Einfache Weiterverarbeitung in Big-Data-Anwendungen
- Getrennte Dateien für Pydantic- und Dataclass-Modelle
- Dateinamen werden vom Basis-Zielpfad abgeleitet

## Kommandozeilenoptionen
- Moderne Kommandozeilenschnittstelle mit Click
- Folgende Optionen:
  - `-s, --source`: Pfad zur MARC21-Quelldatei (erforderlich)
  - `-t, --target`: Basis-Pfad für die Ausgabedateien (erforderlich)
    - Daraus werden die Pfade für die JsonL-Dateien abgeleitet:
      - `{target_basename}.pydantic.jsonl`
      - `{target_basename}.dataclass.jsonl`
  - Automatische Hilfetexte und Fehlermeldungen
  - Farbige, formatierte Ausgabe im Terminal

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

## MARC21 Feldextraktion
- Implementierung der `MarcUtils`-Klasse in `help/marc_utils.py` mit MARC21-Hilfsfunktionen
- Statische Methode `extract_marc_subfields` für Datenextraktion nach MARC21-Feldspezifikation (z.B. "600abcdefg")
- Unterstützung für Multiple-Field-Extraktion mit variablen Subfeldcodes
- Vorverarbeitung und Bereinigung der extrahierten Daten
- Automatische Verarbeitung von Topics aus verschiedenen Themenfeldern wie 600, 610, 650 etc.
- Modularer Aufbau für einfache Wiederverwendung und Erweiterung
- Umfangreiche Logging-Funktionalität mit Klassenlogger über `getSlubLogger`
- Zusätzliche Hilfsmethoden:
  - `parse_marc_field_spec`: Zerlegt MARC-Feldspezifikationen in Feldnummer und Subfeldcodes
  - `create_marc_field_spec`: Erstellt gültige MARC-Feldspezifikationen aus Komponenten
  - `parse_complex_field_spec`: Verarbeitet komplexe Spezifikationen mit Trennzeichen (z.B. "600abc:610abc")

## Nächste Schritte
1. Erstellung des LinkML Schemas
2. Generierung der Modelle
3. Entwicklung des Marimo Notebooks
4. Dokumentation der Beispiele
