# MarcLinkFinc: Dokumentation und Visualisierung

Diese Dokumentation enthält Visualisierungen des Datenflusses und der Prozesse im MarcLinkFinc-Projekt.

## 1. Vom Schema zur JSON-Datei: Der Gesamtprozess

Das folgende Diagramm zeigt den Gesamtprozess von der Definition des LinkML-Schemas bis zur Erzeugung der JsonL-Dateien:

```mermaid
flowchart TB
    subgraph "Schemadefinition"
        A[LinkML Schema\nfinc.yaml] --> |Generator-API| B1[Pydantic-Modell\nGenerierung]
        A --> |Generator-API| B2[Dataclass-Modell\nGenerierung]
    end
    
    subgraph "Modellgenerierung & Speicherung"
        B1 --> C1[Pydantic-Modell\nslubmodels/pydantic_model.py]
        B2 --> C2[Dataclass-Modell\nslubmodels/dataclass_model.py]
    end
    
    subgraph "Datenverarbeitung"
        D[MARC21-Daten\nsamples/output.mrc] --> |Extraktion| E[Extrahierte\nMARC21-Felder]
        E --> F1[Pydantic-Objekte]
        E --> F2[Dataclass-Objekte]
        C1 -.-> |validiert| F1
        C2 -.-> |validiert| F2
    end
    
    subgraph "Datenausgabe"
        F1 --> G1[JsonL-Datei\npydantic.jsonl]
        F2 --> G2[JsonL-Datei\ndataclass.jsonl]
    end
    
    style A fill:#f9d5e5,stroke:#333,stroke-width:2px
    style C1 fill:#eeeeee,stroke:#333,stroke-width:2px
    style C2 fill:#eeeeee,stroke:#333,stroke-width:2px
    style D fill:#d5f9e5,stroke:#333,stroke-width:2px
    style G1 fill:#d5e5f9,stroke:#333,stroke-width:2px
    style G2 fill:#d5e5f9,stroke:#333,stroke-width:2px
```

## 2. Der Ablauf von marc2finc.py

Das folgende Diagramm zeigt den detaillierten Ablauf der Datenverarbeitung in `marc2finc.py`:

```mermaid
sequenceDiagram
    participant User as Benutzer
    participant CLI as Kommandozeile
    participant Marc2Finc as marc2finc.py
    participant Generator as LinkML-Generator
    participant MarcUtils as MarcUtils-Klasse
    participant Models as Generierte Modelle
    participant Storage as Datei-System
    
    User->>CLI: Aufruf mit Optionen<br/>(-s, -t, --schema)
    CLI->>Marc2Finc: Parameter übergeben
    Marc2Finc->>Generator: generate_models_from_schema(schema_path)
    Generator->>Models: Erzeugt Pydantic-Modell
    Generator->>Models: Erzeugt Dataclass-Modell
    Generator->>Storage: Speichert Modelle in slubmodels/
    Generator-->>Marc2Finc: Gibt Modell-Klassen zurück
    
    Marc2Finc->>Storage: Öffnet MARC21-Datei
    
    loop Für jeden MARC21-Datensatz
        Storage-->>Marc2Finc: Liefert nächsten Datensatz
        Marc2Finc->>MarcUtils: extract_marc_subfields(record, ...)
        MarcUtils-->>Marc2Finc: Extrahierte Feldinhalte
        
        Marc2Finc->>Models: Erstellt Pydantic-Objekt
        Models-->>Marc2Finc: Validiertes Pydantic-Objekt
        
        Marc2Finc->>Models: Erstellt Dataclass-Objekt
        Models-->>Marc2Finc: Validiertes Dataclass-Objekt
        
        Marc2Finc->>Storage: Speichert Pydantic-Objekt als JSON
        Marc2Finc->>Storage: Speichert Dataclass-Objekt als JSON
    end
    
    Marc2Finc-->>CLI: Verarbeitungsstatistik
    CLI-->>User: Erfolgsmeldung und Statistik
```

## 3. Die MarcUtils-Klasse im Detail

Die zentrale Komponente für die MARC21-Datenextraktion ist die `MarcUtils`-Klasse. Sie bietet folgende Funktionalitäten:

```mermaid
classDiagram
    class MarcUtils {
        +log: Logger
        +parse_marc_field_spec(spec) Tuple
        +compile_regex_patterns(patterns) List
        +clean_field_content(content, clean, patterns) str
        +join_field_values(values, separator) str
        +extract_marc_subfields(record, *field_specs, join, clean, remove_patterns) List
        +get_marc_field_value(record, field_number, subfield_code, default) str
        +create_marc_field_spec(field_number, subfield_codes) str
        +parse_complex_field_spec(complex_spec) List
    }
    
    MarcUtils ..> "1" Logger : verwendet
    
    note for MarcUtils "Alle Methoden sind statisch und können\nohne Instanziierung verwendet werden."
```

## 4. Typischer Anwendungsfall

Ein typischer Anwendungsfall für die Verarbeitung von MARC21-Daten zu JSON:

```mermaid
flowchart LR
    A[MARC21-Datensatz] -->|MarcUtils.extract_marc_subfields| B[Extrahierte Feldinhalte]
    B -->|Mapping zu Modellfeldern| C[Pydantic/Dataclass-Objekt]
    C -->|json.dumps| D[JSON-Darstellung]
    
    subgraph "Beispiel"
        E["MARC Feld 245a:
        'Die Flora Deutschlands'"]
        F["Extrahierter Inhalt:
        title = 'Die Flora Deutschlands'"]
        G["Pydantic-Objekt:
        Finc(title='Die Flora Deutschlands')"]
        H["{
            'title': 'Die Flora Deutschlands'
        }"]
        
        E --> F --> G --> H
    end 