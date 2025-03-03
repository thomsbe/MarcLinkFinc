"""
LinkML Modellgenerator-Funktionalität.

Dieses Modul bietet Funktionen zum Generieren von Pydantic- und Dataclass-Modellen
aus LinkML-Schemas. Die generierten Modelle werden im slubmodels-Ordner gespeichert
und können dynamisch geladen werden.
"""

import importlib
import sys
from pathlib import Path
from typing import Dict, Type

# LinkML-Importe für die Modellerzeugung
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from linkml_runtime.utils.schemaview import SchemaView

# Lokale Importe
from help.slublogging import getSlubLogger

def generate_models_from_schema(schema_path: str) -> Dict[str, Type]:
    """
    Generiert Pydantic- und Dataclass-Modelle direkt aus dem LinkML-Schema und speichert sie im slubmodels-Ordner.
    
    Args:
        schema_path: Pfad zur LinkML-Schema-Datei (YAML)
    
    Returns:
        Dictionary mit Modellklassen: {"PydanticFinc": PydanticClass, "DataclassFinc": DataclassClass}
    """
    log = getSlubLogger('help.linkml_generator')
    log.info(f"Generiere Modelle aus Schema: {schema_path}")
    
    try:
        # Stelle sicher, dass der slubmodels-Ordner existiert
        models_dir = Path("slubmodels")
        models_dir.mkdir(exist_ok=True)
        
        # Initialisiere die __init__.py Datei, falls sie nicht existiert
        init_file = models_dir / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write("# Generierte LinkML Modelle für FINC\n")
        
        # Lade das Schema
        schema_view = SchemaView(schema_path)
        
        # Generiere Pydantic-Modell
        pydantic_gen = PydanticGenerator(schema=schema_path)
        pydantic_output = pydantic_gen.serialize()
        
        # Speichere Pydantic-Modell im slubmodels-Ordner
        pydantic_path = models_dir / "pydantic_model.py"
        with open(pydantic_path, 'w') as f:
            f.write(pydantic_output)
        log.info(f"Pydantic-Modell in {pydantic_path} gespeichert")
        
        # Generiere Python Dataclass-Modell
        python_gen = PythonGenerator(schema=schema_path)
        python_output = python_gen.serialize()
        
        # Speichere Dataclass-Modell im slubmodels-Ordner
        python_path = models_dir / "dataclass_model.py"
        with open(python_path, 'w') as f:
            f.write(python_output)
        log.info(f"Dataclass-Modell in {python_path} gespeichert")
        
        # Dynamisch die Klassen aus den erzeugten Modulen importieren
        # (erfordert einen sys.path.append, falls der slubmodels-Ordner nicht im Pythonpath ist)
        if str(models_dir.absolute()) not in sys.path:
            sys.path.append(str(models_dir.absolute()))
        
        # Dynamisches Importieren der generierten Module
        pydantic_module = importlib.import_module("slubmodels.pydantic_model")
        python_module = importlib.import_module("slubmodels.dataclass_model")
        
        # Schema-Name extrahieren
        schema_name = schema_view.schema.name
        if not schema_name:
            schema_name = "Finc"  # Fallback, falls kein Name im Schema definiert ist
        
        schema_name = schema_name.capitalize()
        
        # Klassen aus den Modulen bekommen
        # In Pydantic-Modellen wird kein Prefix verwendet
        PydanticClass = getattr(pydantic_module, schema_name)
        DataclassClass = getattr(python_module, schema_name)
        
        log.info(f"Modelle erfolgreich geladen: {PydanticClass.__name__} und {DataclassClass.__name__}")
        
        # Rückgabe der Klassen als Dictionary
        return {
            "PydanticFinc": PydanticClass,
            "DataclassFinc": DataclassClass
        }
            
    except Exception as e:
        log.error(f"Fehler bei der Modellgenerierung: {e}")
        raise 