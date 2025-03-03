#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Marc21 Utility-Funktionen für die Verarbeitung von Marc21-Datensätzen.

Diese Datei enthält Hilfsfunktionen zur effizienten Verarbeitung von Marc21-Datensätzen,
insbesondere für die Extraktion von Feldern und Subfeldern nach spezifischen Kriterien.
"""

from typing import List, Optional, Tuple
from help.logging import getSlubLogger

class MarcUtils:
    """
    Hilfsfunktionen für die Verarbeitung von Marc21-Datensätzen.
    
    Diese Klasse stellt statische Methoden bereit, die bei der Extraktion und Verarbeitung
    von MARC21-Daten helfen. Die Funktionen sind so konzipiert, dass sie flexibel
    mit verschiedenen MARC-Feldspezifikationen arbeiten können.
    """
    
    # Logger auf Klassenebene initialisieren
    log = getSlubLogger('help.marc_utils')
    
    @staticmethod
    def parse_marc_field_spec(spec: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Zerlegt eine MARC-Feldspezifikation in Feldnummer und Subfeldcodes.
        
        Args:
            spec: Eine Feldspezifikation im Format '600abcdefg' (Feldnummer + Subfeldcodes)
            
        Returns:
            Ein Tupel mit (Feldnummer, Subfeldcodes) oder (None, None) bei ungültiger Spezifikation
        """
        if len(spec) < 4 or not spec[:3].isdigit():
            MarcUtils.log.warning(f"Ungültige Feldnummer oder Subfeldcodes: {spec}")
            return None, None
        
        field_number = spec[:3]
        subfield_codes = spec[3:]
        
        return field_number, subfield_codes
    
    @staticmethod
    def extract_marc_subfields(record, *field_specs) -> List[str]:
        """
        Extrahiert die Inhalte der angegebenen MARC-Subfelder aus einem Record.
        
        Args:
            record: Ein pymarc.Record-Objekt
            *field_specs: Eine unbestimmte Anzahl von Strings im Format '600abcdefg' (Feldnummer + Subfeldcodes)
        
        Returns:
            Eine Liste der Inhalte aller angegebenen Subfelder
        """
        results = []
        
        for spec in field_specs:
            # Feldnummer und Subfeldcodes extrahieren
            field_number, subfield_codes = MarcUtils.parse_marc_field_spec(spec)
            if not field_number or not subfield_codes:
                continue
            
            # Hole alle passenden Felder aus dem Record
            fields = record.get_fields(field_number)
            
            # Debug-Information für die gefundenen Felder
            if not fields:
                MarcUtils.log.debug(f"Keine Felder mit Nummer {field_number} gefunden.")
            
            for field in fields:
                # Extrahiere die angeforderten Subfelder
                for code in subfield_codes:
                    # Hole alle Subfelder mit diesem Code
                    subfields = field.get_subfields(code)
                    for content in subfields:
                        if content and content.strip():
                            results.append(content.strip())
        
        MarcUtils.log.debug(f"Extrahierte {len(results)} Inhalte aus {len(field_specs)} Feldspezifikationen.")
        return results 

    @staticmethod
    def create_marc_field_spec(field_number: str, subfield_codes: str) -> str:
        """
        Erstellt eine MARC-Feldspezifikation aus Feldnummer und Subfeldcodes.
        
        Args:
            field_number: Eine 3-stellige MARC-Feldnummer (z.B. "600")
            subfield_codes: Eine Zeichenkette mit Subfeldcodes (z.B. "abcdefg")
            
        Returns:
            Eine gültige MARC-Feldspezifikation (z.B. "600abcdefg")
            
        Raises:
            ValueError: Wenn die Feldnummer ungültig ist
        """
        if len(field_number) != 3 or not field_number.isdigit():
            MarcUtils.log.error(f"Ungültige Feldnummer: {field_number}. Erwartet wird eine 3-stellige Zahl.")
            raise ValueError(f"Ungültige Feldnummer: {field_number}. Erwartet wird eine 3-stellige Zahl.")
        
        if not subfield_codes:
            MarcUtils.log.warning(f"Leere Subfeldcodes für Feld {field_number}.")
            return field_number
        
        return f"{field_number}{subfield_codes}"
    
    @staticmethod
    def parse_complex_field_spec(complex_spec: str) -> List[str]:
        """
        Zerlegt eine komplexe MARC-Feldspezifikation mit Trennzeichen.
        
        Diese Methode kann Spezifikationen wie "600abcdefg:610abc:650xyz" in
        einzelne Feldspezifikationen aufteilen.
        
        Args:
            complex_spec: Eine komplexe MARC-Feldspezifikation mit Trennzeichen
                          (typischerweise ":" oder ";")
            
        Returns:
            Eine Liste einzelner MARC-Feldspezifikationen
        """
        # Unterstütze verschiedene Trennzeichen (: oder ;)
        if ":" in complex_spec:
            specs = complex_spec.split(":")
        elif ";" in complex_spec:
            specs = complex_spec.split(";")
        else:
            # Falls kein Trennzeichen vorhanden ist, behandle als einzelne Spezifikation
            specs = [complex_spec]
        
        # Entferne Leerzeichen und leere Spezifikationen
        specs = [spec.strip() for spec in specs if spec.strip()]
        
        MarcUtils.log.debug(f"Komplexe Spezifikation '{complex_spec}' in {len(specs)} Einzelspezifikationen zerlegt.")
        return specs 