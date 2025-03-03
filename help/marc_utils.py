#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Marc21 Utility-Funktionen für die Verarbeitung von Marc21-Datensätzen.

Diese Datei enthält Hilfsfunktionen zur effizienten Verarbeitung von Marc21-Datensätzen,
insbesondere für die Extraktion von Feldern und Subfeldern nach spezifischen Kriterien.
"""

import logging
from typing import List, Optional, Tuple, Union, Pattern, Dict, Any
import re
from help.slublogging import getSlubLogger

class MarcUtils:
    """
    Hilfsfunktionen für die Verarbeitung von Marc21-Datensätzen.
    
    Diese Klasse stellt statische Methoden bereit, die bei der Extraktion und Verarbeitung
    von MARC21-Daten helfen. Die Funktionen sind so konzipiert, dass sie flexibel
    mit verschiedenen MARC-Feldspezifikationen arbeiten können.
    """
    
    # Logger auf Klassenebene initialisieren
    log = getSlubLogger('help.marc_utils')
    log.setLevel(logging.INFO)
    
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
    def compile_regex_patterns(patterns: List[str]) -> List[Pattern]:
        """
        Kompiliert eine Liste von RegEx-Mustern für effiziente wiederholte Anwendung.
        
        Args:
            patterns: Liste von regulären Ausdrücken als Strings
            
        Returns:
            Liste von kompilierten RegEx-Pattern-Objekten
            
        Example:
            >>> patterns = MarcUtils.compile_regex_patterns([r'\\[.*?\\]', r'\\(.*?\\)'])
            >>> # Patterns können nun für wiederholte Ersetzungen verwendet werden
        """
        compiled_patterns = []
        if not patterns:
            return compiled_patterns
            
        for pattern in patterns:
            try:
                compiled_patterns.append(re.compile(pattern))
            except re.error as e:
                MarcUtils.log.warning(f"Ungültiges RegEx-Muster: {pattern}, Fehler: {e}")
                
        return compiled_patterns
    
    @staticmethod
    def clean_field_content(content: str, clean: bool = True, patterns: List[Pattern] = None) -> str:
        """
        Bereinigt einen Feldinhalt durch Entfernen von Leerzeichen und/oder Anwenden von RegEx-Mustern.
        
        Diese Methode kann verwendet werden, um MARC-Feldinhalte zu normalisieren, indem:
        1. Führende und abschließende Leerzeichen entfernt werden (wenn clean=True)
        2. RegEx-Muster angewendet werden, um unerwünschte Teile zu entfernen
        
        Args:
            content: Der zu bereinigende Feldinhalt
            clean: Wenn True, werden führende und abschließende Leerzeichen entfernt
            patterns: Liste von kompilierten RegEx-Pattern-Objekten zum Entfernen von Mustern
            
        Returns:
            Der bereinigte Feldinhalt oder ein leerer String, wenn nach der Bereinigung nichts übrig bleibt
            
        Example:
            >>> patterns = MarcUtils.compile_regex_patterns([r'\\[.*?\\]'])
            >>> MarcUtils.clean_field_content("  Titel [Elektronische Ressource]  ", True, patterns)
            'Titel'
        """
        if not content:
            return ""
            
        # Entferne führende und abschließende Leerzeichen, wenn gewünscht
        if clean:
            content = content.strip()
            
        # Wende RegEx-Muster an, falls vorhanden
        if patterns:
            for pattern in patterns:
                content = pattern.sub('', content)
                
        return content
    
    @staticmethod
    def join_field_values(values: List[str], separator: str) -> str:
        """
        Verbindet eine Liste von Feldwerten mit einem Trennzeichen.
        
        Diese Methode ist nützlich, um mehrere Subfeldwerte eines MARC-Feldes
        zu einem einzigen String zusammenzuführen.
        
        Args:
            values: Liste der zu verbindenden Werte
            separator: Das Trennzeichen zwischen den Werten (z.B. " " oder ": ")
            
        Returns:
            Ein zusammengeführter String oder ein leerer String, wenn keine Werte übergeben wurden
            
        Example:
            >>> MarcUtils.join_field_values(["Titel", "Untertitel"], ": ")
            'Titel: Untertitel'
        """
        if not values:
            return ""
            
        return separator.join(values)
    
    @staticmethod
    def extract_marc_subfields(record, *field_specs, join=None, clean=True, remove_patterns=None) -> List[str]:
        """
        Extrahiert die Inhalte der angegebenen MARC-Subfelder aus einem Record.
        
        Args:
            record: Ein pymarc.Record-Objekt
            *field_specs: Eine unbestimmte Anzahl von Strings im Format '600abcdefg' (Feldnummer + Subfeldcodes)
            join: Optional. Wenn angegeben, werden die Subfelder eines Feldes mit diesem String verbunden
                 (z.B. join=": " -> "Titel: Untertitel"). Jedes Feld bleibt separat.
            clean: Optional. Wenn True, werden Leerzeichen am Anfang und Ende jedes Wertes entfernt.
            remove_patterns: Optional. Liste von RegEx-Mustern, die aus den Werten entfernt werden sollen.
                           Z.B. ['\\d', '\\W'] würde alle Ziffern und Nicht-Wortzeichen entfernen.
        
        Returns:
            Eine Liste der Inhalte aller angegebenen Subfelder. Wenn join angegeben ist, enthält die Liste
            für jedes Feld einen zusammengesetzten String, andernfalls alle einzelnen Subfeldwerte.
        """
        results = []
        
        # RegEx-Muster kompilieren, wenn vorhanden
        compiled_patterns = MarcUtils.compile_regex_patterns(remove_patterns) if remove_patterns else []
        
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
            
            # Wenn join angegeben ist, fasse Subfelder pro Feld zusammen
            if join is not None:
                for field in fields:
                    field_values = []
                    for code in subfield_codes:
                        for content in field.get_subfields(code):
                            if content:
                                # Bereinige den Inhalt mit der Helper-Methode
                                cleaned_content = MarcUtils.clean_field_content(
                                    content, 
                                    clean=clean, 
                                    patterns=compiled_patterns
                                )
                                
                                if cleaned_content:  # Prüfen, ob nach Bereinigung noch Inhalt übrig ist
                                    field_values.append(cleaned_content)
                    
                    if field_values:
                        # Verwende die join_field_values Helper-Methode
                        joined_value = MarcUtils.join_field_values(field_values, join)
                        results.append(joined_value)
            else:
                # Ursprüngliches Verhalten: Flache Liste aller Subfeldwerte
                for field in fields:
                    for code in subfield_codes:
                        subfields = field.get_subfields(code)
                        for content in subfields:
                            if content:
                                # Bereinige den Inhalt mit der Helper-Methode
                                cleaned_content = MarcUtils.clean_field_content(
                                    content, 
                                    clean=clean, 
                                    patterns=compiled_patterns
                                )
                                
                                if cleaned_content:  # Prüfen, ob nach Bereinigung noch Inhalt übrig ist
                                    results.append(cleaned_content)
        
        MarcUtils.log.debug(f"Extrahierte {len(results)} Inhalte aus {len(field_specs)} Feldspezifikationen.")
        return results
    
    @staticmethod
    def get_marc_field_value(record, field_number: str, subfield_code: str, default: str = "") -> str:
        """
        Extrahiert den Wert aus einem spezifischen MARC-Feld und Subfeld.
        
        Diese Methode ist eine Kurzform für den Zugriff auf ein einzelnes Subfeld,
        wenn nur der erste Wert benötigt wird.
        
        Args:
            record: Ein pymarc.Record-Objekt
            field_number: Die MARC-Feldnummer (z.B. "245")
            subfield_code: Der Subfeldcode (z.B. "a")
            default: Der Standardwert, der zurückgegeben wird, wenn das Feld/Subfeld nicht existiert
            
        Returns:
            Der Inhalt des ersten entsprechenden Subfelds oder der default-Wert
            
        Example:
            >>> # Extrahiert den Haupttitel (Feld 245, Subfeld a)
            >>> title = MarcUtils.get_marc_field_value(record, "245", "a", "Kein Titel vorhanden")
        """
        field = record.get_fields(field_number)
        if not field:
            return default
            
        # Nehme das erste Feld
        first_field = field[0]
        subfields = first_field.get_subfields(subfield_code)
        
        if not subfields:
            return default
            
        # Gib den ersten Subfeldwert zurück
        return subfields[0].strip()

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