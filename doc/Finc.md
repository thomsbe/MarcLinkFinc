
# Class: Finc

Ein Datensatz für den Solr-Index

URI: [https://www.slub-dresden.de/linkml/finc/Finc](https://www.slub-dresden.de/linkml/finc/Finc)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Finc&#124;id:string;record_id:string;title:string;topic:string%20*;author:string%20*;author2:string%20*;author_corporate:string%20*;author_role:string%20*;author2_role:string%20*;author_corporate_role:string%20*;author_sort:string%20%3F;isbn:string%20%3F;recordtype:string])](https://yuml.me/diagram/nofunky;dir:TB/class/[Finc&#124;id:string;record_id:string;title:string;topic:string%20*;author:string%20*;author2:string%20*;author_corporate:string%20*;author_role:string%20*;author2_role:string%20*;author_corporate_role:string%20*;author_sort:string%20%3F;isbn:string%20%3F;recordtype:string])

## Attributes


### Own

 * [➞id](finc__id.md)  <sub>1..1</sub>
     * Description: ID innerhalb eines Solr, zusammengesetzt aus einem Prefix mit der source_id und der record_id (teilweise encodiert)
     * Range: [String](types/String.md)
 * [➞record_id](finc__record_id.md)  <sub>1..1</sub>
     * Description: Lieferanten-Identifier (original ID aus der Quelle)
     * Range: [String](types/String.md)
 * [➞title](finc__title.md)  <sub>1..1</sub>
     * Description: Titel im Titeldatensatz
     * Range: [String](types/String.md)
 * [➞topic](finc__topic.md)  <sub>0..\*</sub>
     * Description: Schlagwörter
     * Range: [String](types/String.md)
 * [➞author](finc__author.md)  <sub>0..\*</sub>
     * Description: nur Hauptautoren, als Liste, die die gleiche Reihenfolge wie die Werte in author_role haben müssen
     * Range: [String](types/String.md)
 * [➞author2](finc__author2.md)  <sub>0..\*</sub>
     * Description: weitere Autorennamen(Nebenautoren bzw. Autoren mit Nebeneintragungen), als Liste, die die gleiche Reihenfolge wie die Werte in author2_role haben müssen
     * Range: [String](types/String.md)
 * [➞author_corporate](finc__author_corporate.md)  <sub>0..\*</sub>
     * Description: Körperschaft und Event als Autor
     * Range: [String](types/String.md)
 * [➞author_role](finc__author_role.md)  <sub>0..\*</sub>
     * Description: Rollen der Hauptautoren der Veröffentlichung
Müssen in der gleichen Reihenfolge wie die Werte in author haben
Keine Angabe=leer, damit Anzahl Autoren=Anzahl Rollen
     * Range: [String](types/String.md)
 * [➞author2_role](finc__author2_role.md)  <sub>0..\*</sub>
     * Description: Rollen der weiteren Autoren
     * Range: [String](types/String.md)
 * [➞author_corporate_role](finc__author_corporate_role.md)  <sub>0..\*</sub>
     * Description: Rollen der Körperschaften und Events
     * Range: [String](types/String.md)
 * [➞author_sort](finc__author_sort.md)  <sub>0..1</sub>
     * Description: 1. Autorenname für Sortierung in Ergebnisliste
     * Range: [String](types/String.md)
 * [➞isbn](finc__isbn.md)  <sub>0..1</sub>
     * Description: Internationale Standardbuchnummer (International Standard Book Number, ISBN)
     * Range: [String](types/String.md)
 * [➞recordtype](finc__recordtype.md)  <sub>1..1</sub>
     * Description: Typ der Quelle
     * Range: [String](types/String.md)
