import logging
import click
from pymarc import MARCReader
import json
from pathlib import Path

# Importiere beide Finc-Modelle mit Aliase für eine eindeutige Unterscheidung
from slubmodels.pydantic import Finc as PydanticFinc  # Pydantic-Modell zur Validierung und JSON-Ausgabe
from slubmodels.dataclass import Finc as DataclassFinc  # Dataclass-Modell für alternative Zwecke
from help.marc_utils import MarcUtils
from help.logging import getSlubLogger

def process_marc_files(sourcefile, targetfile=None):
    """
    Verarbeite Marc21-Dateien und erstelle Pydantic- und Dataclass-Objekte
    
    Args:
        sourcefile: Pfad zur MARC21-Quelldatei
        targetfile: Optional. Pfad zur JSON-Zieldatei
    
    Returns:
        Tuple aus (PydanticFinc-Liste, DataclassFinc-Liste)
    """
    log = getSlubLogger(__name__)
    log.info(f"Verarbeite Datei: {sourcefile}")
    
    pydantics = []
    dataclasses = []
    # Marc21 Datei einlesen
    with open(sourcefile, 'rb') as f:
        reader = MARCReader(f)
        
        # PPN und Titel ausgeben zur Kontrolle
        for record in reader:
            log.info(f"PPN: {record['001']} - Titel: {record['245']['a']}")

            # PPN als ID verwenden
            id = f"0-{record['001'].data}"
            record_id = record['001'].data

            # title = 245ab, clean, join(": "), first
            titles = MarcUtils.extract_marc_subfields(record, "245ab")
            title = ": ".join(titles)
            
            # topic = 600abcdefghjklmnopqrstuvxyz:610abcdefghklmnoprstuvxyz:611acdefghjklnpqstuvxyz:630adefghklmnoprstvxyz:650abcdevxyz:689agxz:655abvxyz:651avxyz:648avxyz:970de:937abc:653a
            complex_topic_spec = "600abcdefghjklmnopqrstuvxyz:610abcdefghklmnoprstuvxyz:611acdefghjklnpqstuvxyz:630adefghklmnoprstvxyz:650abcdevxyz:689agxz:655abvxyz:651avxyz:648avxyz:970de:937abc:653a"
            
            # Verwende die parse_complex_field_spec Methode, um die komplexe Spezifikation zu zerlegen
            topic_specs = MarcUtils.parse_complex_field_spec(complex_topic_spec)
            
            log.debug(f"Verarbeite {len(topic_specs)} Themen-Feldspezifikationen")
            topics = MarcUtils.extract_marc_subfields(record, *topic_specs)
            log.debug(f"Extrahierte {len(topics)} Themen aus dem Record")
            
            try:
                pydantic_record = PydanticFinc(
                    id=id,
                    record_id=record_id,
                    title=title,
                    topic=topics
                )
                pydantics.append(pydantic_record)
            except Exception as e:
                log.error(f"Fehler beim Erstellen des PydanticFinc Objekts: {e}")

            try:
                dataclass_record = DataclassFinc(
                    id=id,
                    record_id=record_id,
                    title=title,
                    topic=topics
                )
                dataclasses.append(dataclass_record)
            except Exception as e:
                log.error(f"Fehler beim Erstellen des Dataclass Finc Objekts: {e}")

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
                    f.write(json.dumps(model.model_dump(), ensure_ascii=False) + '\n')
            
            # Speichere Dataclass-Modelle im JsonL-Format (ein JSON pro Zeile)
            with open(dataclass_file, 'w', encoding='utf-8') as f:
                for model in dataclasses:
                    f.write(json.dumps(model.__dict__, ensure_ascii=False) + '\n')
            
            log.info(f"Ergebnisse erfolgreich gespeichert: {len(pydantics)} Pydantic-Modelle, {len(dataclasses)} Dataclass-Modelle")
        except Exception as e:
            log.error(f"Fehler beim Speichern der Ergebnisse: {e}")
    
    return pydantics, dataclasses

@click.command()
@click.option('-s', '--source', required=True, help='Pfad zur MARC21 Quelldatei')
@click.option('-t', '--target', required=True, help='Pfad zur Ausgabedatei (ohne Erweiterung)')
def main(source, target):
    """Konvertiere MARC21 zu FINC JSON."""
    # Optional: Pfad zur Logging-Konfigurationsdatei angeben, falls gewünscht
    log = getSlubLogger('marc2finc')
    
    sourcefile = source
    targetfile = target

    log.info(f"Quelle: {sourcefile}")
    log.info(f"Ziel-Basis: {targetfile}")

    process_marc_files(sourcefile, targetfile)
    
    # Erstelle Dateinamen für die Ausgabe
    output_path = Path(targetfile)
    base_name = output_path.stem
    base_dir = output_path.parent
    pydantic_file = base_dir / f"{base_name}.pydantic.jsonl"
    dataclass_file = base_dir / f"{base_name}.dataclass.jsonl"
    
    click.echo("Verarbeitung abgeschlossen!")
    click.echo(f"Pydantic-Modelle wurden in {pydantic_file} gespeichert.")
    click.echo(f"Dataclass-Modelle wurden in {dataclass_file} gespeichert.")

if __name__ == "__main__":
    main()

            
            




            

