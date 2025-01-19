from pymarc import Record, Field, Subfield

def create_example_record() -> Record:
    """
    Erstellt einen Beispiel-Marc21-Record mit Testdaten.
    
    Returns:
        Record: Ein pymarc Record-Objekt mit Beispieldaten
    """
    # Erstellen eines neuen Marc21-Records
    record = Record()

    # Hinzufügen von Kontrollfeldern
    record.add_field(
        Field(tag='008', data='220504s2022    gw            000 0 ger d')
    )

    # Hinzufügen von Datenfeldern
    # Titel
    record.add_field(
        Field(
            tag = '245',
            indicators = ['1', '0'],
            subfields = [
                Subfield('a', 'Ein Beispielbuch:'),
                Subfield('b', 'Eine Einführung in Marc21'),
                Subfield('c', 'von Max Mustermann')
            ]
        )
    )

    # Autor
    record.add_field(
        Field(
            tag = '100',
            indicators = ['1', ' '],
            subfields = [
                Subfield('a', 'Mustermann, Max'),
                Subfield('d', '1980-'),
                Subfield('e', 'Verfasser'),
                Subfield('4', 'aut')
            ]
        )
    )

    # ISBN
    record.add_field(
        Field(
            tag = '020',
            indicators = [' ', ' '],
            subfields = [
                Subfield('a', '978-3-123456-78-9')
            ]
        )
    )
    
    return record

if __name__ == "__main__":
    # Beispielausgabe wenn die Datei direkt ausgeführt wird
    record = create_example_record()
    print("Marc21-Record Beispiel:")
    print(record) 