from __future__ import annotations

import re
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_prefix": "https://www.slub-dresden.de/linkml/finc/",
        "id": "https://www.slub-dresden.de/linkml/finc",
        "imports": ["linkml:types"],
        "name": "finc",
        "prefixes": {
            "finc": {
                "prefix_prefix": "finc",
                "prefix_reference": "https://www.slub-dresden.de/linkml/finc",
            },
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            },
        },
        "source_file": "schema/finc.yaml",
    }
)


class Finc(ConfiguredBaseModel):
    """
    Ein Datensatz für den Solr-Index
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://www.slub-dresden.de/linkml/finc"}
    )

    id: str = Field(
        default=...,
        description="""ID innerhalb eines Solr, zusammengesetzt aus einem Prefix mit der source_id und der record_id (teilweise encodiert)""",
        json_schema_extra={"linkml_meta": {"alias": "id", "domain_of": ["Finc"]}},
    )
    record_id: str = Field(
        default=...,
        description="""Lieferanten-Identifier (original ID aus der Quelle)""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "record_id",
                "annotations": {"source_marc": {"tag": "source_marc", "value": "001"}},
                "domain_of": ["Finc"],
            }
        },
    )
    title: str = Field(
        default=...,
        description="""Titel im Titeldatensatz""",
        json_schema_extra={"linkml_meta": {"alias": "title", "domain_of": ["Finc"]}},
    )
    topic: Optional[List[str]] = Field(
        default=None,
        description="""Schlagwörter""",
        json_schema_extra={"linkml_meta": {"alias": "topic", "domain_of": ["Finc"]}},
    )
    author: Optional[List[str]] = Field(
        default=None,
        description="""nur Hauptautoren, als Liste, die die gleiche Reihenfolge wie die Werte in author_role haben müssen""",
        json_schema_extra={"linkml_meta": {"alias": "author", "domain_of": ["Finc"]}},
    )
    author2: Optional[List[str]] = Field(
        default=None,
        description="""weitere Autorennamen(Nebenautoren bzw. Autoren mit Nebeneintragungen), als Liste, die die gleiche Reihenfolge wie die Werte in author2_role haben müssen""",
        json_schema_extra={"linkml_meta": {"alias": "author2", "domain_of": ["Finc"]}},
    )
    author_corporate: Optional[List[str]] = Field(
        default=None,
        description="""Körperschaft und Event als Autor""",
        json_schema_extra={
            "linkml_meta": {"alias": "author_corporate", "domain_of": ["Finc"]}
        },
    )
    author_role: Optional[List[str]] = Field(
        default=None,
        description="""Rollen der Hauptautoren der Veröffentlichung
Müssen in der gleichen Reihenfolge wie die Werte in author haben
Keine Angabe=leer, damit Anzahl Autoren=Anzahl Rollen""",
        json_schema_extra={
            "linkml_meta": {"alias": "author_role", "domain_of": ["Finc"]}
        },
    )
    author2_role: Optional[List[str]] = Field(
        default=None,
        description="""Rollen der weiteren Autoren""",
        json_schema_extra={
            "linkml_meta": {"alias": "author2_role", "domain_of": ["Finc"]}
        },
    )
    author_corporate_role: Optional[List[str]] = Field(
        default=None,
        description="""Rollen der Körperschaften und Events""",
        json_schema_extra={
            "linkml_meta": {"alias": "author_corporate_role", "domain_of": ["Finc"]}
        },
    )
    author_sort: Optional[str] = Field(
        default=None,
        description="""1. Autorenname für Sortierung in Ergebnisliste""",
        json_schema_extra={
            "linkml_meta": {"alias": "author_sort", "domain_of": ["Finc"]}
        },
    )
    isbn: Optional[str] = Field(
        default=None,
        description="""Internationale Standardbuchnummer (International Standard Book Number, ISBN)""",
        json_schema_extra={"linkml_meta": {"alias": "isbn", "domain_of": ["Finc"]}},
    )

    @field_validator("isbn")
    def pattern_isbn(cls, v):
        pattern = re.compile(
            r"^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$"
        )
        if isinstance(v, list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid isbn format: {element}")
        elif isinstance(v, str):
            if not pattern.match(v):
                raise ValueError(f"Invalid isbn format: {v}")
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Finc.model_rebuild()
