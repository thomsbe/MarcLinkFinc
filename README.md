# MarcLinkFinc

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

## Übersicht

MarcLinkFinc ist ein Tool zur Demonstration der Umwandlung von Marc21-Datensätzen in strukturierte JSON-Objekte mithilfe von LinkML und Pydantic. Es dient als Showcase für die Integration von Marc21-Bibliotheksdaten mit modernen Datenmodellierungstechniken.

Das Projekt hilft dabei, den Weg der Daten aus binären Marc21-Dateien in validierte, strukturierte Datenmodelle visuell darzustellen und zu verstehen, wie Bibliotheksdaten mit modernen Python-Tools verarbeitet werden können.

## Features

- **Marc21-Feldextraktion**: Flexible Extraktion von Feldern und Unterfeldern aus Marc21-Datensätzen
- **LinkML-Schemamodellierung**: Definition von Datenmodellen in YAML mit LinkML
- **Dynamische Modellgenerierung**: Automatische Generierung von Pydantic- und Dataclass-Modellen aus dem Schema
- **Datenvalidierung**: Validierung der extrahierten Daten gegen das definierte Schema
- **Modulare Struktur**: Erweiterbare Komponenten für anpassbare Datenverarbeitungspipelines
- **Marimo-Integration**: Interaktive Visualisierung der Datenverarbeitung mit Marimo-Notebooks

## Voraussetzungen

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (moderner Python-Paketmanager)

## Installation

### Installation von uv

Für Linux oder MacOS:

```bash
curl -sSf https://astral.sh/uv/install.sh | sh
```

Für Windows (mit PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Installation von MarcLinkFinc

```bash
# Repository klonen
git clone https://github.com/thomsbe/MarcLinkFinc.git
cd MarcLinkFinc

# Virtuelle Umgebung erstellen und Abhängigkeiten installieren
uv venv
source .venv/bin/activate  # Unter Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Verwendung

### Command-Line-Tool

Das Haupttool `marc2finc.py` konvertiert Marc21-Dateien in JSON:

```bash
python marc2finc.py --input samples/output.mrc --output result.jsonl
```

Optionen:
- `--input`: Pfad zur Marc21-Eingabedatei
- `--output`: Pfad zur JSON-Ausgabedatei
- `--format`: Ausgabeformat (pydantic oder dataclass)
- `--schema`: Pfad zur LinkML-Schemadatei (Standard: schema/finc.yaml)

### Marimo-Notebook

Das interaktive Marimo-Notebook bietet eine visuelle Demonstration:

```bash
marimo edit notebook.py
```

## Projektstruktur

```
MarcLinkFinc/
├── help/                    # Hilfsmodule
│   ├── marc_utils.py        # Marc21-Verarbeitungsklassen
│   ├── slublogging.py       # Logging-Konfiguration
│   └── linkml_generator.py  # LinkML-Modellgenerator
├── slubmodels/              # Generierte Datenmodelle
│   ├── __init__.py
│   ├── pydantic_model.py    # Pydantic-Klassen (generiert)
│   └── dataclass_model.py   # Dataclass-Klassen (generiert)
├── samples/                 # Beispieldateien
│   └── output.mrc           # Beispiel-Marc21-Datei
├── schema/                  # LinkML-Schemadefinitionen
│   └── finc.yaml            # Haupt-Schema
├── marc2finc.py             # Hauptprogramm
├── notebook.py              # Marimo-Notebook
├── [technical.md](technical.md)             # Technische Dokumentation
└── [user.md](user.md)                  # Benutzervisualisierungen
```

## Visualisierungen

Diagramme und Visualisierungen des Datenflusses sind in der [user.md](user.md)-Datei verfügbar, die den gesamten Prozess von der Schema-Definition bis zur JSON-Generierung darstellt.

## Dokumentation

Das Projekt enthält zwei primäre Dokumentationsdateien:

- [user.md](user.md) - Enthält Mermaid-Diagramme und visuelle Darstellungen des Datenflusses für Endbenutzer
- [technical.md](technical.md) - Detaillierte technische Dokumentation über Architekturentscheidungen, Implementierungsdetails und Projektstruktur

Die technische Dokumentation erläutert die verwendeten Bibliotheken, Logging-Konfiguration, Datenfluss und Marc21-Feldextraktion im Detail.

## Aktueller Entwicklungsstand

- ✅ Marc21-Feldextraktion mit Musterentfernung
- ✅ LinkML-Schemamodellierung
- ✅ Automatische Modellgenerierung
- ✅ Marimo-Notebook-Grundstruktur
- ✅ Kommandozeileninterface
- ✅ Testdateien und Beispiele
- 🔄 Erweiterte Marimo-Visualisierungen
- 🔄 Vollständige Testabdeckung

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Siehe die LICENSE-Datei für Details.
