from pymarc import Record, Field, Subfield
from typing import Optional, List, Union, Dict
import re
from dataclasses import dataclass


@dataclass
class SubSpec:
    """Repräsentiert eine Sub-Specification in MARCspec."""

    operator: str  # '=' oder '!=' oder '~' oder '!~'
    comparison: str


@dataclass
class MARCSpec:
    """Repräsentiert eine vollständige MARCspec."""

    field_tag: str
    index: Optional[str] = None
    indicators: Optional[List[str]] = None  # [ind1, ind2]
    char_positions: Optional[List[str]] = None  # Für Positionen wie /0-2
    subfields: Optional[List[str]] = None
    subspecs: Optional[Dict[str, SubSpec]] = None


class MARCSpecParser:
    def __init__(self):
        # Grundlegende Patterns
        self.field_tag_pattern = r"^([0-9a-zA-Z]{3})"
        self.index_pattern = r"\[([0-9#\-]+)\]"
        self.indicator_pattern = r"\^([12])([\S])"
        self.char_position_pattern = r"\/([0-9#\-]+)"
        self.subfield_pattern = r"\$([a-z0-9])"
        self.subspec_pattern = r"\{(.+?)\}"

        # Subspec Operator Patterns
        self.subspec_operators = {"=": r"=", "!=": r"!=", "~": r"~", "!~": r"!~"}

    def parse(self, spec_string: str) -> MARCSpec:
        """Parse einen MARCspec String in seine Komponenten."""
        # Basis-Spec initialisieren
        spec = MARCSpec(field_tag="")

        # Field Tag extrahieren (obligatorisch)
        field_match = re.match(self.field_tag_pattern, spec_string)
        if not field_match:
            raise ValueError(f"Ungültiger MARCspec String: {spec_string}")
        spec.field_tag = field_match.group(1)

        # Position nach dem Field Tag
        pos = 3
        remaining = spec_string[pos:]

        # Index extrahieren
        if remaining and remaining.startswith("["):
            index_match = re.match(self.index_pattern, remaining)
            if index_match:
                spec.index = index_match.group(1)
                pos += len(index_match.group(0))
                remaining = spec_string[pos:]

        # Indikatoren extrahieren
        indicators = []
        while remaining and remaining.startswith("^"):
            ind_match = re.match(self.indicator_pattern, remaining)
            if ind_match:
                position, value = ind_match.groups()
                indicators.append((position, value))
                pos += len(ind_match.group(0))
                remaining = spec_string[pos:]
        if indicators:
            spec.indicators = indicators

        # Character Positions extrahieren
        if remaining and remaining.startswith("/"):
            char_match = re.match(self.char_position_pattern, remaining)
            if char_match:
                spec.char_positions = [char_match.group(1)]
                pos += len(char_match.group(0))
                remaining = spec_string[pos:]

        # Subfields extrahieren
        subfields = []
        while remaining and remaining.startswith("$"):
            subfield_match = re.match(self.subfield_pattern, remaining)
            if subfield_match:
                subfields.append(subfield_match.group(1))
                pos += len(subfield_match.group(0))
                remaining = spec_string[pos:]
        if subfields:
            spec.subfields = subfields

        # SubSpecs extrahieren
        subspecs = {}
        while remaining and remaining.startswith("{"):
            subspec_match = re.match(self.subspec_pattern, remaining)
            if subspec_match:
                subspec_content = subspec_match.group(1)
                operator = None
                for op, pattern in self.subspec_operators.items():
                    if op in subspec_content:
                        operator = op
                        left, right = subspec_content.split(op)
                        subspecs[left.strip()] = SubSpec(
                            operator=op, comparison=right.strip()
                        )
                        break
                pos += len(subspec_match.group(0))
                remaining = spec_string[pos:]
        if subspecs:
            spec.subspecs = subspecs

        return spec


class MARCSpecExecutor:
    def __init__(self, record: Record):
        self.record = record
        self.parser = MARCSpecParser()

    def execute(self, spec_string: str) -> List[str]:
        """Führt eine MARCspec-Abfrage auf dem Record aus."""
        spec = self.parser.parse(spec_string)
        results = []

        # Felder holen
        fields = self.record.get_fields(spec.field_tag)

        # Index anwenden
        if spec.index is not None:
            fields = self._apply_index(fields, spec.index)

        # Durch Felder iterieren
        for field in fields:
            # Indikatoren prüfen
            if spec.indicators and not self._check_indicators(field, spec.indicators):
                continue

            # Subfields verarbeiten
            if spec.subfields:
                for subfield_code in spec.subfields:
                    subfield_values = field.get_subfields(subfield_code)
                    # SubSpecs prüfen
                    if spec.subspecs:
                        subfield_values = [
                            v
                            for v in subfield_values
                            if self._check_subspecs(v, spec.subspecs)
                        ]
                    results.extend(subfield_values)
            else:
                value = field.value()
                if spec.subspecs and not self._check_subspecs(value, spec.subspecs):
                    continue
                results.append(value)

            # Character Positions anwenden
            if spec.char_positions:
                results = self._apply_char_positions(results, spec.char_positions[0])

        return results

    def _check_indicators(self, field: Field, indicators: List[tuple]) -> bool:
        """Prüft, ob ein Feld die spezifizierten Indikatoren erfüllt."""
        for position, value in indicators:
            indicator = field.indicators[int(position) - 1]
            if indicator != value:
                return False
        return True

    def _check_subspecs(self, value: str, subspecs: Dict[str, SubSpec]) -> bool:
        """Prüft, ob ein Wert die SubSpecs erfüllt."""
        for field_spec, subspec in subspecs.items():
            if subspec.operator == "=":
                if value != subspec.comparison:
                    return False
            elif subspec.operator == "!=":
                if value == subspec.comparison:
                    return False
            elif subspec.operator == "~":
                if not re.search(subspec.comparison, value):
                    return False
            elif subspec.operator == "!~":
                if re.search(subspec.comparison, value):
                    return False
        return True

    def _apply_index(self, fields: List, index_spec: str) -> List:
        """Wendet eine Index-Spezifikation auf die Felder an."""
        if "-" in index_spec:
            start, end = index_spec.split("-")
            start = 0 if start == "#" else int(start)
            end = len(fields) if end == "#" else int(end) + 1
            return fields[start:end]
        else:
            index = -1 if index_spec == "#" else int(index_spec)
            return [fields[index]]

    def _apply_char_positions(self, values: List[str], char_spec: str) -> List[str]:
        """Wendet Character-Position-Spezifikationen auf die Werte an."""
        results = []
        for value in values:
            if "-" in char_spec:
                start, end = char_spec.split("-")
                start = 0 if start == "#" else int(start)
                end = len(value) if end == "#" else int(end) + 1
                results.append(value[start:end])
            else:
                pos = -1 if char_spec == "#" else int(char_spec)
                results.append(value[pos])
        return results


def create_example_record() -> Record:
    """
    Erstellt einen Beispiel-Marc21-Record mit Testdaten.

    Returns:
        Record: Ein pymarc Record-Objekt mit Beispieldaten
    """
    # Erstellen eines neuen Marc21-Records
    record = Record()

    # Hinzufügen von Kontrollfeldern
    record.add_field(Field(tag="008", data="220504s2022    gw            000 0 ger d"))

    # Hinzufügen von Datenfeldern
    # Titel
    record.add_field(
        Field(
            tag="245",
            indicators=["1", "0"],
            subfields=[
                Subfield("a", "Ein Beispielbuch:"),
                Subfield("b", "Eine Einführung in Marc21"),
                Subfield("c", "von Max Mustermann"),
            ],
        )
    )

    # Autor
    record.add_field(
        Field(
            tag="100",
            indicators=["1", " "],
            subfields=[
                Subfield("a", "Mustermann, Max"),
                Subfield("d", "1980-"),
                Subfield("e", "Verfasser"),
                Subfield("4", "aut"),
            ],
        )
    )

    # ISBN
    record.add_field(
        Field(
            tag="020",
            indicators=[" ", " "],
            subfields=[Subfield("a", "978-3-123456-78-9")],
        )
    )

    return record


if __name__ == "__main__":
    # Beispielausgabe wenn die Datei direkt ausgeführt wird
    record = create_example_record()
    print("Marc21-Record Beispiel:")
    print(record)
