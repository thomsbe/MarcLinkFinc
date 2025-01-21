from __future__ import annotations

import re
from typing import Any, ClassVar, Dict, Optional

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
        "default_prefix": "marc",
        "description": "Ein Schema für Marc21-Daten zur Verwendung in Solr",
        "id": "https://w3id.org/marc-linkml",
        "imports": ["linkml:types"],
        "name": "marc-linkml",
        "prefixes": {
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            },
            "marc": {
                "prefix_prefix": "marc",
                "prefix_reference": "https://w3id.org/marc-linkml/",
            },
        },
        "source_file": "schema/book.yaml",
    }
)


class Book(ConfiguredBaseModel):
    """
    Eine Klasse zur Repräsentation von Buchdaten aus Marc21
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/marc-linkml"}
    )

    title: str = Field(
        default=...,
        description="""Der Haupttitel des Buches (Marc21 245$a)""",
        json_schema_extra={"linkml_meta": {"alias": "title", "domain_of": ["Book"]}},
    )
    subtitle: Optional[str] = Field(
        default=None,
        description="""Der Untertitel des Buches (Marc21 245$b)""",
        json_schema_extra={"linkml_meta": {"alias": "subtitle", "domain_of": ["Book"]}},
    )
    author: str = Field(
        default=...,
        description="""Der Name des Autors (Marc21 100$a)""",
        json_schema_extra={"linkml_meta": {"alias": "author", "domain_of": ["Book"]}},
    )
    author_dates: Optional[str] = Field(
        default=None,
        description="""Lebensdaten des Autors (Marc21 100$d)""",
        json_schema_extra={
            "linkml_meta": {"alias": "author_dates", "domain_of": ["Book"]}
        },
    )
    isbn: str = Field(
        default=...,
        description="""Die ISBN des Buches (Marc21 020$a)""",
        json_schema_extra={"linkml_meta": {"alias": "isbn", "domain_of": ["Book"]}},
    )

    @field_validator("author")
    def pattern_author(cls, v):
        pattern = re.compile(r"^[^,]+, [^,]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid author format: {element}")
        elif isinstance(v, str):
            if not pattern.match(v):
                raise ValueError(f"Invalid author format: {v}")
        return v

    @field_validator("isbn")
    def pattern_isbn(cls, v):
        pattern = re.compile(r"^[0-9-]{13,17}$")
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
Book.model_rebuild()
