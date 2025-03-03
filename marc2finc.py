import click
from pymarc import MARCReader
import json
from pathlib import Path
import sys

# Lokale Importe
from help.marc_utils import MarcUtils
from help.slublogging import getSlubLogger
from help.linkml_generator import generate_models_from_schema

def process_marc_files(sourcefile, targetfile=None, models=None):
    """
    Verarbeite Marc21-Dateien und erstelle Pydantic- und Dataclass-Objekte
    
    Args:
        sourcefile: Pfad zur MARC21-Quelldatei
        targetfile: Optional. Pfad zur JSON-Zieldatei
        models: Optional. Dictionary mit den zu verwendenden Modellklassen
    
    Returns:
        Tuple aus (PydanticFinc-Liste, DataclassFinc-Liste)
    """
    log = getSlubLogger('process_marc_files')
    log.info(f"Verarbeite Datei: {sourcefile}")
    
    # Wenn keine Modelle übergeben wurden, verwende die Standardmodelle
    if models is None:
        log.info("Keine Modelle übergeben, generiere Modelle aus Schema")
        models = generate_models_from_schema("schema/finc.yaml")
    
    PydanticFinc = models["PydanticFinc"]
    DataclassFinc = models["DataclassFinc"]
    
    pydantics = []
    dataclasses = []
    # Marc21 Datei einlesen
    with open(sourcefile, 'rb') as f:
        reader = MARCReader(f)
        
        # PPN und Titel ausgeben zur Kontrolle
        for record in reader:
            log.info(f"PPN: {record['001'].data} - Titel: {record['245']['a']}")

            # PPN als ID verwenden
            id = f"0-{record['001'].data}"
            record_id = record['001'].data

            # title = 245ab, clean, join(": "), first
            titles = MarcUtils.extract_marc_subfields(record, "245ab", join=": ")
            # Nur ein Titel sollte verwendet werden, wenn mehrere vorhanden sind (ungewöhnlich)
            title = titles[0] if titles else ""
            
            # topic = 600abcdefghjklmnopqrstuvxyz:610abcdefghklmnoprstuvxyz:611acdefghjklnpqstuvxyz:630adefghklmnoprstvxyz:650abcdevxyz:689agxz:655abvxyz:651avxyz:648avxyz:970de:937abc:653a
            complex_topic_spec = "600abcdefghjklmnopqrstuvxyz:610abcdefghklmnoprstuvxyz:611acdefghjklnpqstuvxyz:630adefghklmnoprstvxyz:650abcdevxyz:689agxz:655abvxyz:651avxyz:648avxyz:970de:937abc:653a"
            
            # Verwende die parse_complex_field_spec Methode, um die komplexe Spezifikation zu zerlegen
            topic_specs = MarcUtils.parse_complex_field_spec(complex_topic_spec)
            
            log.debug(f"Verarbeite {len(topic_specs)} Themen-Feldspezifikationen")
            topics = MarcUtils.extract_marc_subfields(record, *topic_specs)
            log.debug(f"Extrahierte {len(topics)} Themen aus dem Record")

            # DEMO: recordtype ist Pflichtfeld und soll String sein!
            recordtype = "marc"

            # isbn = 020a:772z:773z
            complex_isbn_spec = "020a:772z:773z"
            isbn_specs = MarcUtils.parse_complex_field_spec(complex_isbn_spec)
            isbn = MarcUtils.extract_marc_subfields(record, *isbn_specs)

            # isbn liefert eine Liste, ist aber nicht Multi-Valued
            if isbn and isinstance(isbn, list) and len(isbn) == 1:
                isbn = isbn[0]
            else:
                isbn = None

            # DEMO: ISBN die nicht auf den RegEx passt
            # isbn = "DIESDAS112"

            try:
                pydantic_record = PydanticFinc(
                    id=id,
                    record_id=record_id,
                    title=title,
                    topic=topics,
                    recordtype=recordtype,
                    isbn=isbn
                )
                pydantics.append(pydantic_record)
            except Exception as e:
                log.error(f"Pydantic: Fehler beim Erstellen des PydanticFinc Objekts: {e}")

            try:
                dataclass_record = DataclassFinc(
                    id=id,
                    record_id=record_id,
                    title=title,
                    topic=topics,
                    recordtype=recordtype,
                    isbn=isbn
                )
                dataclasses.append(dataclass_record)
            except Exception as e:
                log.error(f"Dataclass: Fehler beim Erstellen des Dataclass Finc Objekts: {e}")

    # Anschließende Ausgabe oder Verarbeitung der erstellten Objekte, z.B. als JSON speichern
    if targetfile:
        output_path = Path(targetfile)
        # Stelle sicher, dass der Zielordner existiert
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Extrahiere den Basisnamen ohne Erweiterung
        base_name = output_path.stem
        base_dir = output_path.parent

        # Erzeuge die Dateinamen für die Ausgabedateien
        pydantic_file = base_dir / f"{base_name}.pydantic.jsonl"
        dataclass_file = base_dir / f"{base_name}.dataclass.jsonl"
        
        log.info(f"Speichere Pydantic-Modelle in {pydantic_file}")
        log.info(f"Speichere Dataclass-Modelle in {dataclass_file}")
        
        try:
            # Speichere Pydantic-Modelle im JsonL-Format (ein JSON pro Zeile)
            with open(pydantic_file, 'w', encoding='utf-8') as f:
                for model in pydantics:
                    # exclude_none=True entfernt alle None-Werte und exclude_unset=True entfernt ungesetzte Felder
                    model_dict = model.model_dump(exclude_none=True, exclude_defaults=True)
                    # Zusätzlich leere Listen entfernen
                    cleaned_dict = {k: v for k, v in model_dict.items() if not (isinstance(v, list) and len(v) == 0)}
                    f.write(json.dumps(cleaned_dict, ensure_ascii=False) + '\n')
            
            # Speichere Dataclass-Modelle im JsonL-Format (ein JSON pro Zeile)
            with open(dataclass_file, 'w', encoding='utf-8') as f:
                for model in dataclasses:
                    # Konvertiere Dataclass in Dict und entferne None-Werte und leere Listen
                    model_dict = model.__dict__.copy()
                    cleaned_dict = {k: v for k, v in model_dict.items() if v is not None and not (isinstance(v, list) and len(v) == 0)}
                    f.write(json.dumps(cleaned_dict, ensure_ascii=False) + '\n')
            
            log.info(f"Ergebnisse erfolgreich gespeichert: {len(pydantics)} Pydantic-Modelle, {len(dataclasses)} Dataclass-Modelle")
        except Exception as e:
            log.error(f"Fehler beim Speichern der Ergebnisse: {e}")
    
    return pydantics, dataclasses

@click.command()
@click.option('-s', '--source', required=True, help='Pfad zur MARC21 Quelldatei')
@click.option('-t', '--target', required=True, help='Pfad zur Ausgabedatei (ohne Erweiterung)')
@click.option('--schema', default='schema/finc.yaml', help='Pfad zum LinkML-Schema (default: schema/finc.yaml)')
def main(source, target, schema):
    """Konvertiere MARC21 zu FINC JSON."""
    # Optional: Pfad zur Logging-Konfigurationsdatei angeben, falls gewünscht
    log = getSlubLogger('marc2finc')
    
    sourcefile = source
    targetfile = target
    schema_file = schema

    log.info(f"Quelle: {sourcefile}")
    log.info(f"Ziel-Basis: {targetfile}")
    log.info(f"Schema: {schema_file}")
    
    # Generiere die Modelle aus dem Schema
    try:
        models = generate_models_from_schema(schema_file)
        process_marc_files(sourcefile, targetfile, models)
        
        # Erstelle Dateinamen für die Ausgabe
        output_path = Path(targetfile)
        base_name = output_path.stem
        base_dir = output_path.parent
        pydantic_file = base_dir / f"{base_name}.pydantic.jsonl"
        dataclass_file = base_dir / f"{base_name}.dataclass.jsonl"
        
        click.echo("Verarbeitung abgeschlossen!")
        click.echo(f"Pydantic-Modelle wurden in {pydantic_file} gespeichert.")
        click.echo(f"Dataclass-Modelle wurden in {dataclass_file} gespeichert.")
    except Exception as e:
        log.error(f"Fehler bei der Verarbeitung: {e}")
        click.echo(f"Fehler: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()