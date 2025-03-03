# Auto generated from finc.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-03-03T11:32:04
# Schema: finc
#
# id: https://www.slub-dresden.de/linkml/finc
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
FINC = CurieNamespace('finc', 'https://www.slub-dresden.de/linkml/finc')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://www.slub-dresden.de/linkml/finc/')


# Types

# Class references
class FincId(extended_str):
    pass


@dataclass(repr=False)
class Finc(YAMLRoot):
    """
    Ein Datensatz für den Solr-Index
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FINC["/Finc"]
    class_class_curie: ClassVar[str] = "finc:/Finc"
    class_name: ClassVar[str] = "Finc"
    class_model_uri: ClassVar[URIRef] = URIRef("https://www.slub-dresden.de/linkml/finc/Finc")

    id: Union[str, FincId] = None
    record_id: str = None
    title: str = None
    recordtype: str = None
    topic: Optional[Union[str, List[str]]] = empty_list()
    author: Optional[Union[str, List[str]]] = empty_list()
    author2: Optional[Union[str, List[str]]] = empty_list()
    author_corporate: Optional[Union[str, List[str]]] = empty_list()
    author_role: Optional[Union[str, List[str]]] = empty_list()
    author2_role: Optional[Union[str, List[str]]] = empty_list()
    author_corporate_role: Optional[Union[str, List[str]]] = empty_list()
    author_sort: Optional[str] = None
    isbn: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FincId):
            self.id = FincId(self.id)

        if self._is_empty(self.record_id):
            self.MissingRequiredField("record_id")
        if not isinstance(self.record_id, str):
            self.record_id = str(self.record_id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.recordtype):
            self.MissingRequiredField("recordtype")
        if not isinstance(self.recordtype, str):
            self.recordtype = str(self.recordtype)

        if not isinstance(self.topic, list):
            self.topic = [self.topic] if self.topic is not None else []
        self.topic = [v if isinstance(v, str) else str(v) for v in self.topic]

        if not isinstance(self.author, list):
            self.author = [self.author] if self.author is not None else []
        self.author = [v if isinstance(v, str) else str(v) for v in self.author]

        if not isinstance(self.author2, list):
            self.author2 = [self.author2] if self.author2 is not None else []
        self.author2 = [v if isinstance(v, str) else str(v) for v in self.author2]

        if not isinstance(self.author_corporate, list):
            self.author_corporate = [self.author_corporate] if self.author_corporate is not None else []
        self.author_corporate = [v if isinstance(v, str) else str(v) for v in self.author_corporate]

        if not isinstance(self.author_role, list):
            self.author_role = [self.author_role] if self.author_role is not None else []
        self.author_role = [v if isinstance(v, str) else str(v) for v in self.author_role]

        if not isinstance(self.author2_role, list):
            self.author2_role = [self.author2_role] if self.author2_role is not None else []
        self.author2_role = [v if isinstance(v, str) else str(v) for v in self.author2_role]

        if not isinstance(self.author_corporate_role, list):
            self.author_corporate_role = [self.author_corporate_role] if self.author_corporate_role is not None else []
        self.author_corporate_role = [v if isinstance(v, str) else str(v) for v in self.author_corporate_role]

        if self.author_sort is not None and not isinstance(self.author_sort, str):
            self.author_sort = str(self.author_sort)

        if self.isbn is not None and not isinstance(self.isbn, str):
            self.isbn = str(self.isbn)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.finc__id = Slot(uri=DEFAULT_.id, name="finc__id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.finc__id, domain=None, range=URIRef)

slots.finc__record_id = Slot(uri=DEFAULT_.record_id, name="finc__record_id", curie=DEFAULT_.curie('record_id'),
                   model_uri=DEFAULT_.finc__record_id, domain=None, range=str)

slots.finc__title = Slot(uri=DEFAULT_.title, name="finc__title", curie=DEFAULT_.curie('title'),
                   model_uri=DEFAULT_.finc__title, domain=None, range=str)

slots.finc__topic = Slot(uri=DEFAULT_.topic, name="finc__topic", curie=DEFAULT_.curie('topic'),
                   model_uri=DEFAULT_.finc__topic, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author = Slot(uri=DEFAULT_.author, name="finc__author", curie=DEFAULT_.curie('author'),
                   model_uri=DEFAULT_.finc__author, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author2 = Slot(uri=DEFAULT_.author2, name="finc__author2", curie=DEFAULT_.curie('author2'),
                   model_uri=DEFAULT_.finc__author2, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author_corporate = Slot(uri=DEFAULT_.author_corporate, name="finc__author_corporate", curie=DEFAULT_.curie('author_corporate'),
                   model_uri=DEFAULT_.finc__author_corporate, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author_role = Slot(uri=DEFAULT_.author_role, name="finc__author_role", curie=DEFAULT_.curie('author_role'),
                   model_uri=DEFAULT_.finc__author_role, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author2_role = Slot(uri=DEFAULT_.author2_role, name="finc__author2_role", curie=DEFAULT_.curie('author2_role'),
                   model_uri=DEFAULT_.finc__author2_role, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author_corporate_role = Slot(uri=DEFAULT_.author_corporate_role, name="finc__author_corporate_role", curie=DEFAULT_.curie('author_corporate_role'),
                   model_uri=DEFAULT_.finc__author_corporate_role, domain=None, range=Optional[Union[str, List[str]]])

slots.finc__author_sort = Slot(uri=DEFAULT_.author_sort, name="finc__author_sort", curie=DEFAULT_.curie('author_sort'),
                   model_uri=DEFAULT_.finc__author_sort, domain=None, range=Optional[str])

slots.finc__isbn = Slot(uri=DEFAULT_.isbn, name="finc__isbn", curie=DEFAULT_.curie('isbn'),
                   model_uri=DEFAULT_.finc__isbn, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$'))

slots.finc__recordtype = Slot(uri=DEFAULT_.recordtype, name="finc__recordtype", curie=DEFAULT_.curie('recordtype'),
                   model_uri=DEFAULT_.finc__recordtype, domain=None, range=str)