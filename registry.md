# Registry and data origin

Expected metadata (VOResource) with their equivalent in Datacite schema
to provide Data Origin in the registry:

|VOResource |Datacite  | Level | Explain|
|---      |:-:  |:-: |:-: |
|identifier    |Identifier (1) |M | ivoid of resource(s) hosted by the service|
|title         |Title (3) |M  | resource title|
|shortName     ||| Resource short name|
|altIdentifier | AlternateIdentifier (11)| R | Alternate identifier accepts bibcode, DOI or URL. DOI should be privileged to facilitate citation and link with DataCite or Crossref..eg: DOI |
|**Curation** |
|.publisher     | Publisher (4) | M |publisher|
|.creator       | Creator (2) | M | author(s)|
|.contributor   | Contributor | | |
|.date [Created]| Dates [created] (8)| M | creation date (in data center)|
|.date [Updated]| Dates [updated] (8)| M | last modification|
|  ?            | PublicationYear (5) | | publication year in data center|
|.version       | Version (15) | R ||
|.contact       | |||
|**Content** ||| |
|.source        | RelatedIdentifier (12) (type=bibcode, relationType=IsSupplementTo) | R | bibcode|
|.referenceURL  | | R | landing page|
|.type          | ResourceType (10)| | Resource type (catalog, etc)|
|.description   | Description (17)| | abstract|
|.contentLevel  | | ||
|.relationShip  | RelatedIdentifiers (12) | R |link to remote resource (Recomended to link Original Data Center) |
|..relatedResource | RelatedIdentifier (12) | R ||
|**Rights** ||| |
|rights   | Rights (16)| R|  The right element accepts free text. However, it is preferable to provide a machine-readable Licence. See the list https://spdx.org/licenses/.|         
|.URI     | rightsURI | R| licence URL|
|         | rightsIdentifier | | standard licence name .ex CC-by. Copyright is accepted by FAIR principle. But copyright is only a link to the data producer. It gives the contact point to any users who would like to use data. Copyright is more simple to implement for data-center that provides a copy of original resource, but its use is not well integrated in an interoperable workflow.



## Example of rights serialization
```xml
<rights rightsURI="https://spdx.org/licenses/CC-BY-4.0.html">
  Creative Commons Attribution 4.0
</right>
```

## Example or relation ship 
Cite the original dataset using "source" (to link a bibliographic reference) or "relatedIdentifier" (to link a dataset)

e.g.:
```xml
<relationship>
  <relationshipType>Cites</relationshipType>
  <relatedResource>doi: 10.5270/esa-qa4lep3 : Gaia DR3 ESA</relatedResource> 
</relationship>
```
