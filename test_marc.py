#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testskript für die MarcUtils-Funktionen mit einem echten MARC21-Datensatz.
"""

from pymarc import MARCReader
from help.marc_utils import MarcUtils
import re

# MarcUtils-Instanz erstellen
utils = MarcUtils()

# MARC21-Datei öffnen und ersten Datensatz lesen
with open('samples/output.mrc', 'rb') as marc_file:
    reader = MARCReader(marc_file)
    record = next(reader)
    
    print("=" * 60)
    print("TEIL 1: BASIS-TESTS")
    print("=" * 60)
    
    # Originaltitel mit pymarc-Eigenschaft
    print("Original Titel (pymarc-Eigenschaft):")
    print(record.title)
    print()
    
    # Titel mit extract_marc_subfields ohne join
    print("Titel mit extract_marc_subfields (ohne join):")
    title_parts = utils.extract_marc_subfields(record, '245ab')
    print(title_parts)
    print()
    
    # Titel mit extract_marc_subfields mit join
    print("Titel mit extract_marc_subfields (mit join=' '):")
    title_combined = utils.extract_marc_subfields(record, '245ab', join=' ')
    print(title_combined)
    print()
    
    # Simulierter Titel mit Klammern für Testdatenentfernung
    original_title = record.title
    test_title = f"{original_title} [Elektronische Ressource] (3. Auflage)"
    print("Simulierter Titel mit Klammern:")
    print(test_title)
    print()
    
    # Anwenden der RegEx-Muster auf den simulierten Titel
    print("Klammern mit RegEx entfernt:")
    cleaned_title = re.sub(r'\[.*?\]', '', test_title)  # Entferne eckige Klammern
    cleaned_title = re.sub(r'\(.*?\)', '', cleaned_title)  # Entferne runde Klammern
    print(cleaned_title)
    print()
    
    # Modifikation eines MARC-Felds zum Testen von remove_patterns
    # Wir erstellen ein temporäres Feld mit Klammern
    from pymarc import Field, Subfield
    test_field = Field(
        tag='999',
        indicators=['0', '0'],
        subfields=[
            Subfield('a', 'Test mit [eckigen] Klammern'),
            Subfield('b', 'und (runden) Klammern')
        ]
    )
    record.add_field(test_field)
    
    # Test der extract_marc_subfields Methode mit remove_patterns
    print("Test von extract_marc_subfields mit remove_patterns:")
    test_extracted = utils.extract_marc_subfields(
        record,
        '999ab',
        join=' ',
        remove_patterns=[r'\[.*?\]', r'\(.*?\)']
    )
    print(test_extracted)
    print()
    
    # ISBN mit und ohne Bindestriche
    print("ISBN mit extract_marc_subfields:")
    isbn = utils.extract_marc_subfields(record, '020a')
    print(isbn)
    print()
    
    # Modifikation eines MARC-Felds für ISBN mit Bindestrichen
    test_isbn_field = Field(
        tag='901',
        indicators=['0', '0'],
        subfields=[
            Subfield('a', '978-3-494-01943-7'),
            Subfield('b', '3-494-01943-2')
        ]
    )
    record.add_field(test_isbn_field)
    
    # Test der extract_marc_subfields Methode für ISBN mit remove_patterns
    print("ISBN mit extract_marc_subfields und remove_patterns für Bindestriche:")
    isbn_cleaned = utils.extract_marc_subfields(
        record,
        '901ab',
        remove_patterns=[r'-']
    )
    print(isbn_cleaned)
    print()
    
    # Simulierte ISBN mit Bindestrich
    test_isbn = '978-3-494-01943-7'
    print("Simulierte ISBN mit Bindestrichen:")
    print(test_isbn)
    print()
    
    # ISBN mit Entfernung der Bindestriche
    print("ISBN mit Entfernung der Bindestriche (RegEx):")
    cleaned_isbn = re.sub(r'-', '', test_isbn)
    print(cleaned_isbn)
    print()
    
    # Komplexeres Beispiel: Entfernen mehrerer Muster
    test_complex = f"Titel [Info] mit (Zusatz) und ISBN 978-3-494-01943-7 und {original_title}"
    print("Komplexer Test-String:")
    print(test_complex)
    print()
    
    print("Nach Anwendung mehrerer RegEx-Muster:")
    # Entferne eckige Klammern, runde Klammern und Bindestriche
    patterns = [r'\[.*?\]', r'\(.*?\)', r'-']
    cleaned_complex = test_complex
    for pattern in patterns:
        cleaned_complex = re.sub(pattern, '', cleaned_complex)
    print(cleaned_complex)
    print()
    
    # Mehrere Felder auf einmal extrahieren
    print("Mehrere Felder (Titel und ISBN):")
    multiple_fields = utils.extract_marc_subfields(record, '245ab', '020a', join=' ')
    print(multiple_fields)
    print()
    
    print("=" * 60)
    print("TEIL 2: TESTS FÜR DIE NEUEN HILFSMETHODEN")
    print("=" * 60)
    
    # Test der compile_regex_patterns Methode
    print("Test der compile_regex_patterns Methode:")
    patterns_list = [r'\[.*?\]', r'\(.*?\)', r'-']
    compiled_patterns = utils.compile_regex_patterns(patterns_list)
    print(f"Anzahl kompilierter RegEx-Muster: {len(compiled_patterns)}")
    print(f"Typen der Muster: {[type(p).__name__ for p in compiled_patterns]}")
    print()
    
    # Test der clean_field_content Methode
    print("Test der clean_field_content Methode:")
    print("1. Nur Leerzeichen entfernen:")
    print(f"  Original: '  Test mit Leerzeichen  '")
    print(f"  Bereinigt: '{utils.clean_field_content('  Test mit Leerzeichen  ', clean=True)}'")
    print("2. Mit RegEx-Mustern:")
    print(f"  Original: 'Test [zu entfernen] und (auch zu entfernen)'")
    clean_result = utils.clean_field_content(
        'Test [zu entfernen] und (auch zu entfernen)',
        clean=True,
        patterns=compiled_patterns[:2]  # Verwende nur die ersten beiden Muster ([ ] und ( ))
    )
    print(f"  Bereinigt: '{clean_result}'")
    print()
    
    # Test der join_field_values Methode
    print("Test der join_field_values Methode:")
    values = ["Titel", "Untertitel", "Weitere Informationen"]
    print(f"Original-Werte: {values}")
    print(f"Mit Leerzeichen verbunden: '{utils.join_field_values(values, ' ')}'")
    print(f"Mit Doppelpunkt verbunden: '{utils.join_field_values(values, ': ')}'")
    print(f"Mit Komma und Leerzeichen verbunden: '{utils.join_field_values(values, ', ')}'")
    print()
    
    # Test der get_marc_field_value Methode
    print("Test der get_marc_field_value Methode:")
    title_a = utils.get_marc_field_value(record, "245", "a")
    title_b = utils.get_marc_field_value(record, "245", "b")
    nonexistent = utils.get_marc_field_value(record, "999", "z", "Nicht vorhanden")
    print(f"Titel (245a): '{title_a}'")
    print(f"Untertitel (245b): '{title_b}'")
    print(f"Nicht existierendes Feld (999z): '{nonexistent}'")
    print() 