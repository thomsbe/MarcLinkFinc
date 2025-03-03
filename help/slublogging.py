import logging
import logging.config
from pathlib import Path
from typing import Optional

# Für Python 3.12 steht das eingebaute Modul "tomllib" zur Verfügung.
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib

# Standard TOML-Konfiguration als Fallback
DEFAULT_LOGGING_CONFIG = '''
version = 1
disable_existing_loggers = false

[root]
level = "INFO"
handlers = ["console"]

[handlers]
[handlers.console]
class = "logging.StreamHandler"
formatter = "standard"
level = "INFO"
stream = "ext://sys.stdout"

[formatters]
[formatters.standard]
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
'''

def convert_log_level(level_str: str) -> int:
    """
    Wandelt einen String-Log-Level in den entsprechenden Logging-Level um.
    """
    try:
        return getattr(logging, level_str.upper())
    except AttributeError as e:
        raise ValueError(f"Ungültiger Log-Level: {level_str}") from e

def load_logging_config(config_file: Optional[Path] = None) -> dict:
    """
    Lädt die Logging-Konfiguration aus einer TOML-Datei oder verwendet die Standardkonfiguration.
    
    Die Konfiguration wird in folgender Reihenfolge geladen:
    1. Aus der explizit angegebenen Datei (wenn config_file gesetzt und die Datei existiert)
    2. Aus der Standarddatei "logging.toml" im aktuellen Verzeichnis (wenn vorhanden)
    3. Aus der eingebetteten Standardkonfiguration (DEFAULT_LOGGING_CONFIG)
    
    Args:
        config_file: Optionaler Pfad zur TOML-Konfigurationsdatei.
    
    Returns:
        dict: Das geladene Konfigurations-Dictionary.
    """
    # Wenn eine Konfigurationsdatei explizit angegeben wurde und existiert
    if config_file and config_file.exists():
        with open(config_file, 'rb') as f:
            config = tomllib.load(f)
    else:
        # Wenn keine Datei angegeben wurde, suche nach "logging.toml" im aktuellen Verzeichnis
        default_config_file = Path("logging.toml")
        if default_config_file.exists():
            with open(default_config_file, 'rb') as f:
                config = tomllib.load(f)
            log = logging.getLogger('help.slublogging')
            log.info(f"Logging-Konfiguration aus {default_config_file} geladen")
        else:
            # Als letzten Ausweg die eingebaute Standardkonfiguration verwenden
            config = tomllib.loads(DEFAULT_LOGGING_CONFIG)
    
    # Konvertiere die String-Log-Level in numerische Werte
    if 'root' in config and 'level' in config['root']:
        config['root']['level'] = convert_log_level(config['root']['level'])
    
    if 'handlers' in config:
        for handler in config['handlers'].values():
            if 'level' in handler:
                handler['level'] = convert_log_level(handler['level'])
    
    return config

def getSlubLogger(name: str, config_file: Optional[Path] = None) -> logging.Logger:
    """
    Erstellt und konfiguriert einen Logger für SLUB-Anwendungen.
    
    Verwende immer explizite, aussagekräftige Namen für Logger, NICHT __name__.
    Empfohlen ist ein hierarchisches Benennungsschema wie 'appname.module.submodule'.
    
    Args:
        name: Name des Loggers (expliziter Name, NICHT __name__)
        config_file: Optionaler Pfad zur TOML-Konfigurationsdatei
    
    Returns:
        logging.Logger: Die konfigurierte Logger-Instanz.
    """
    try:
        # Lade die Logging-Konfiguration und wende sie an
        config = load_logging_config(config_file)
        logging.config.dictConfig(config)
        logger = logging.getLogger(name)
        logger.debug(f"Logger '{name}' wurde erfolgreich konfiguriert")
    except Exception as e:
        # Im Fehlerfall: Fallback-Konfiguration, aber vermeide doppelte Handler
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.warning(f"Fehler beim Konfigurieren des Loggers: {str(e)}. Verwende Basic-Konfiguration.")
    return logger 