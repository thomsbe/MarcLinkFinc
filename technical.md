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
- Permanente Modelle im Ordner `slubmodels`:
  - Generierte Python-Dataclass-Modelle in `slubmodels/dataclass_model.py`
  - Generierte Pydantic-Modelle in `slubmodels/pydantic_model.py`
  - Automatisch aus dem LinkML-Schema generiert
- Marimo Notebook in `notebook.py`
- Zentrale Logging-Konfiguration in `help/slublogging.py`
- Hilfsmodule:
  - `help/marc_utils.py`: Funktionen zur MARC21-Verarbeitung
  - `help/slublogging.py`: Zentrale Logging-Konfiguration
  - `help/linkml_generator.py`: Generierung von LinkML-Modellen

## Logging-Konfiguration
- Zentraler Logger über `getSlubLogger()` aus dem Modul `help.slublogging`
- Logger-Namenskonvention:
  - Immer explizite, aussagekräftige Namen verwenden
  - NICHT `__name__` verwenden
  - Hierarchisches Benennungsschema bevorzugt: `appname.module.submodule`
  - Beispiele: `marc2finc`, `help.marc_utils`, `process_marc_files`
- Konfiguration wird in folgender Reihenfolge geladen:
  1. Explizit angegebene TOML-Datei (wenn übergeben und vorhanden)
  2. Standarddatei `logging.toml` im aktuellen Verzeichnis (wenn vorhanden)
  3. Eingebettete Standard-Konfiguration
- Log-Level-Strategie:
  - Standard-Konfiguration: INFO-Level für übersichtliche Konsolenausgabe
  - DEBUG-Level nur bei expliziter Konfiguration über externe TOML-Dateien
- Zwei Handler (in expliziter Konfiguration):
  - Console-Handler (INFO-Level)
  - File-Handler (DEBUG-Level)
- Standardisiertes Logging-Format mit Zeitstempel, Logger-Name, Level und Nachricht
- Vermeidung von Namenskonflikten mit dem Standardmodul `logging`

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
- Bereinigung von leeren Werten:
  - Null-Werte (None) werden aus der Ausgabe entfernt
  - Leere Arrays werden nicht ausgegeben
  - Unbelegte optionale Felder erscheinen nicht im JSON
- Validierungsprüfung für required-Felder bleibt erhalten
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
  - `--schema`: Pfad zum LinkML-Schema (optional, Standard: schema/finc.yaml)
  - Automatische Hilfetexte und Fehlermeldungen
  - Farbige, formatierte Ausgabe im Terminal

## Schema-Design (LinkML)
- Basis-Schema in `schema/finc.yaml` implementiert
- Fokus auf bibliografische Felder für den Finc-Solr-Index:
  - Eindeutige Identifikatoren (`id`, `record_id`)
  - Bibliografische Grunddaten (`title`)
  - Beteiligte Personen/Körperschaften (`author`, `author2`, `author_corporate`)
  - Rollen der Beteiligten (`author_role`, `author2_role`, `author_corporate_role`)
  - Thematische Erschließung (`topic`)
  - Standardidentifikatoren (`isbn`) mit Validierungsmustern für korrekte Formatierung
  - Medientypen (`recordtype`)
- LinkML-Features im Einsatz:
  - Pflichtfelder mit `required: true`
  - Mehrwertige Felder mit `multivalued: true`
  - Feldvalidierung via regex-Patterns (z.B. für ISBN)
  - Umfangreiche Feldbeschreibungen
  - Annotationen für MARC21-Quellfelder (z.B. `source_marc: "001"`)
- Erweiterbar für zusätzliche Felder und komplexere Validierungsregeln

## Implementierungsstatus
- [x] Grundlegende Projektstruktur
- [x] LinkML Schema Definition (finc.yaml)
- [x] Dynamische Modellgenerierung aus LinkML-Schema
- [x] Marc21 Beispieldaten (samples/output.mrc)
- [ ] Marimo Notebook
- [ ] Dokumentation

## MARC21 Beispieldaten
- Demo-Datei `samples/output.mrc` im binären MARC21-Format vorhanden
- Enthält 13 Beispieldatensätze mit vielfältigen bibliografischen Informationen:
  - Bücher, Multimedia-Inhalte, wissenschaftliche Publikationen
  - Verschiedene Sprachen und Formate
  - Diverse Metadatenfelder (Autoren, Themen, Identifikatoren, etc.)
- Ideal für Demonstrationszwecke des Konvertierungsprozesses
- Kann mit `marc2finc.py` verarbeitet werden, um JSONL-Ausgabedateien zu erzeugen
- Demonstriert unterschiedliche MARC21-Feldtypen und deren Mapping zum LinkML-Schema

## MARC21 Feldextraktion

Zur effizienten Extraktion von Daten aus MARC21-Datensätzen wurden verschiedene Hilfsfunktionen implementiert:

1. `extract_marc_subfields`: Extrahiert Inhalte aus spezifizierten MARC-Feldern und Subfeldern:
   - Unterstützt Extraktion mehrerer Felder in einem Aufruf
   - Parameter `join` ermöglicht die Verkettung von Subfeldern (z.B. Titel + Untertitel)
   - Parameter `clean` entfernt automatisch führende und abschließende Leerzeichen
   - Parameter `remove_patterns` erlaubt die Anwendung regulärer Ausdrücke zur Bereinigung der extrahierten Werte:
     - Entfernung von Klammern und deren Inhalt: `[r'\[.*?\]', r'\(.*?\)']`
     - Entfernung von Bindestrichen in ISBNs: `[r'-']`
     - Beliebige andere RegEx-Muster zur Bereinigung von Feldinhalten

2. **Hilfsmetoden zur Datenverarbeitung:**
   - `clean_field_content`: Bereinigt einen Feldinhalt durch Entfernen von Leerzeichen und/oder Anwenden von RegEx-Mustern
   - `join_field_values`: Verbindet mehrere Feldwerte mit einem Trennzeichen zu einem String
   - `compile_regex_patterns`: Kompiliert eine Liste von RegEx-Mustern für effiziente wiederholte Anwendung
   - `get_marc_field_value`: Vereinfachter Zugriff auf ein einzelnes Subfeld mit Standardwert-Option

3. **Methoden zur MARC-Feldspezifikation:**
   - `parse_marc_field_spec`: Zerlegt Spezifikationen wie "600abcdefg" in Feldnummer und Subfeldcodes
   - `create_marc_field_spec`: Erstellt eine gültige Feldspezifikation aus Feldnummer und Subfeldcodes
   - `parse_complex_field_spec`: Verarbeitet komplexe Spezifikationen mit mehreren Feldern (z.B. "600abc:650xyz")

Diese Funktionen ermöglichen eine präzise und flexible Extraktion von MARC21-Daten, die dann in Pydantic-Modelle oder andere Datenstrukturen übertragen werden können. Die modulare Struktur mit ausgelagerten Hilfsmethoden erlaubt die einfache Erweiterung und Wiederverwendung der Funktionalität.

## Dynamische Modellgenerierung
- Direkte Generierung von Pydantic- und Dataclass-Modellen aus dem LinkML-Schema
- Implementiert im Modul `help/linkml_generator.py`:
  - Zentrale Funktion `generate_models_from_schema()` übernimmt die gesamte Generierung
  - Saubere Trennung der Funktionalität von der Hauptanwendungslogik
- Permanente Speicherung der generierten Modelle im `slubmodels`-Ordner:
  - `slubmodels/pydantic_model.py`: Enthält das Pydantic-Modell
  - `slubmodels/dataclass_model.py`: Enthält das Dataclass-Modell
  - `slubmodels/__init__.py`: Macht das Paket importierbar
- Vorteile:
  - Version Control der Modelldateien möglich (Git)
  - Einfache Referenz für Demonstrationszwecke
  - Transparente Darstellung der generierten Datenstrukturen
  - Direktes Experimentieren mit verschiedenen Schemata über den `--schema`-Parameter

## Marimo Notebook (ausstehend)
- Geplante Implementierung in `notebook.py`
- Interaktives, zellbasiertes Interface zur Demonstration des kompletten Workflows
- Geplante Komponenten:
  1. Schema-Visualisierung: Zeigt die Struktur des LinkML-Schemas
  2. Marc21-Datenimport: Lädt und zeigt Beispieldaten aus `samples/output.mrc`
  3. Feldextraktion: Demonstriert die Extraktion von Feldern nach MARC21-Spezifikation
  4. Modellgenerierung: Erstellt Modelle direkt aus dem Schema
  5. Datenvalidierung: Zeigt Validierungsfunktionen und Fehlerbehandlung
  6. Datenkonvertierung: Transformiert MARC21 zu Pydantic/Dataclass-Objekten
  7. JSON-Ausgabe: Visualisiert die Daten im JSON-Format
- Nutzt interaktive UI-Elemente von Marimo:
  - Dropdowns für Datensatzauswahl
  - Code-Highlighting für Schemas und Modelle
  - Interaktive Diagramme für die Visualisierung der Datenstrukturen
  - Vergleichsansichten zwischen MARC21 und JSON-Ausgabe

## Nächste Schritte
1. Entwicklung des Marimo Notebooks
2. Erweitern der Dokumentation mit Anwendungsbeispielen
3. Bereitstellung zusätzlicher Beispiele für komplexere MARC21-Felder
