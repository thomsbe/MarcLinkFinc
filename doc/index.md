
# finc


**metamodel version:** 1.7.0

**version:** None





### Classes

 * [Finc](Finc.md) - Ein Datensatz für den Solr-Index

### Mixins


### Slots

 * [➞author](finc__author.md) - nur Hauptautoren, als Liste, die die gleiche Reihenfolge wie die Werte in author_role haben müssen
 * [➞author2](finc__author2.md) - weitere Autorennamen(Nebenautoren bzw. Autoren mit Nebeneintragungen), als Liste, die die gleiche Reihenfolge wie die Werte in author2_role haben müssen
 * [➞author2_role](finc__author2_role.md) - Rollen der weiteren Autoren
 * [➞author_corporate](finc__author_corporate.md) - Körperschaft und Event als Autor
 * [➞author_corporate_role](finc__author_corporate_role.md) - Rollen der Körperschaften und Events
 * [➞author_role](finc__author_role.md) - Rollen der Hauptautoren der Veröffentlichung
 * [➞author_sort](finc__author_sort.md) - 1. Autorenname für Sortierung in Ergebnisliste
 * [➞id](finc__id.md) - ID innerhalb eines Solr, zusammengesetzt aus einem Prefix mit der source_id und der record_id (teilweise encodiert)
 * [➞isbn](finc__isbn.md) - Internationale Standardbuchnummer (International Standard Book Number, ISBN)
 * [➞record_id](finc__record_id.md) - Lieferanten-Identifier (original ID aus der Quelle)
 * [➞title](finc__title.md) - Titel im Titeldatensatz
 * [➞topic](finc__topic.md) - Schlagwörter

### Enums


### Subsets


### Types


#### Built in

 * **Bool**
 * **Curie**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Curie](types/Curie.md)  (**Curie**)  - a compact URI
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Jsonpath](types/Jsonpath.md)  (**str**)  - A string encoding a JSON Path. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded in tree form.
 * [Jsonpointer](types/Jsonpointer.md)  (**str**)  - A string encoding a JSON Pointer. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to a valid object within the current instance document when encoded in tree form.
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [Sparqlpath](types/Sparqlpath.md)  (**str**)  - A string encoding a SPARQL Property Path. The value of the string MUST conform to SPARQL syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded as RDF.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
