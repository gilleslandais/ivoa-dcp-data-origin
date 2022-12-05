# Data Origin in the VO

The goal of the document is to make the Data Origin more visible in
the query results executed in the **Virtual Observatory**. The document lists
meta-data required to provide sufficient **traceability** to end-users in order to
improve the understanding of the resultsets and enabling its reuse and its
**citation**.


## Use cases

- (Data Origin information)
  A researcher has data in a VOTable that shows an odd feature.  They
  would now like to talk to the creator of the data to help figure
  out whether that feature is physics or an artefact. [Requirement:
  contact information to producers present; but then let's not make
  that a MUST: This can be GDPR-relevant data, and it must be
  possible to leave it out if it is]

  The researcher completes his understanding with Data Origin information easily accesible from the VOtable, and this, regardless of the service which generated the result. For instance, a URL that links an article.
  [The information could contain the Author, the year of publication, related resources like an article or the original data URL]
 
  When data provided by the service is derived from external resources, or if the data were performed with an additional curation, the nature and the links to the external resources are available.

  For instance, a table published in a journal or by a Space Agency is
  also hosted in a Data Center like CDS, GAVO, etc. The data curation
  depends of the Data Center which can add associated data, enrich
  meta-data (eg: add filter for magnitude) or make a sub-selection of
  columns.
  [an advanced serialisation could be based on DOI vocabulary "isVariantFormiOf", "IsDerivedFrom", ...]


- (Reproducibility)
  A researcher revisits work they did six months earlier in an ad-hoc
  fashion and would now like to reproduce it in a more structured
  fashion.  Do do that, they need to know, say, which queries against
  which services, or perhaps which programs, produced the files.
  [Requirement: have the request parameters and a service
  identification (access url? ivoid?) in the data origin]

- (Citation)
  While preparing a publication, a researcher would like to properly
  cite the software and data that went into their results.  They now
  run a program to extract that information from the digital artefacts
  going into the publication -- perhaps even in separate parts of
  citations and acknowledgements.  [Requirement: The data origin must
  indicate requests for citation and/or acknowledgement in a
  machine-readable way, preferably in a way that machines can
  generate BibTeX for whatever they specify]

  The information allows the researcher to fill the template citation asked by journals.
  
  *Example (American Astronomical Society template):

"we searched optical astrometric data of these sources from
the Gaia (Gaia Collaboration et al. 2016) Early Data Release 3 (Gaia
Collaboration et al. 2021) via the Gaia archive (Gaia Collaboration
2020)."*

- (Workflow) Give me a bibliography of everything I’ve used in the workflow" .

The VOTable resulting of a session contains homogenized metadata that can be merged and compared.

- **What else ? ....**

## Metadata expected
Tracing Data origin can be complex. It depends on the granularity expected.
- A basic approach consists to add information using key=value pairs. Each interaction is independent with no interaction with each other. This approach could be generally serialized in VOTable using the INFO tag.
- An advanced approach consists in a rich serialization that allows information to interact. 
This approach requires an advanced VOTable serialization. mivot is a repsonse that enables to map data with data-models like DatasetDM or Provenance (or last-step-provenance)


### Basic metadata
The following metadata can be repeated and could follow a controlled vocabulary.

#### Involved agents 
- Author: name or ORCID
- Editor: name or URL
- Journal: name or URL
- Organization: name or URL
- Datacenter that provides the result: name or URL
- Contact: email

#### Involved resources
- Resource Identifier: ivoid of resource(s) hosted by the service which provides the result
- Resource citation: DOI, bibcode of resource(s) hosted by the datacenter which returns the result
- Remote resource identifier: a remote ressource which was used to build the result
- Remote resource citation: a remote ressource which was used to build the result

#### Curation information
- publication date
- Curation level
- Licence
- Access protocol: eg.TAP query, SCS, ...
- Query: eg: ADQL

- Comment: Any additional information in text plain that complete the result
- ...?


### Advanced metadata
- Explain the link existing between a resource provided by the datacenter and the original repository <br/>
(eg: Gaia table provided by CDS as a variant form of the original ESA table)
- Link Agents (author, editor, organization, ...) with the resources implied to build the result
- Nature of the information <br/>
explain transformation operated by datacenter. 
for instance, "this column has been added by the datacenter", "this resource is a subset of the original data" ...
- specialization of the information<br/>
For instance :
    - an *article* is specialized with attributes: PID, journal name, date, link to agent(s)..
    - a *resource* : **type** , url, PID, comment, link to agent(s)
- ...

## Proposal

### Query information
Query information enables to link the registry and to reproduce the query. 
For queries on evolving dataset, the version or the date must complete the information.


|meta-data| Description| Mandatory |
|---      |:-:  |:-: |
|IVOID    | ivoid identifier to link registry | yes |
|DATA-CENTER| Data center that provides the VOTable | yes |
|VERSION | Dataset version (or release date) | |
|ACCESS-PROTOCOL| Protcol access with version | |
|QUERY| Request url  | |
|QUERY-DATE| Query execution date | |
|DATA-CENTER-CONTACT| email or URL contact | |
|LANDING-PAGE| Dataset landing page | |
(M=Mandatory)

Serialisation example: &lt;info&gt; tag makes the jobs. see <a href='tests/J_AJ_161_36_table8.xml'>SCS example</a>

### Dataset Origin
Dataset-origin completes the "Query information" - 


Simple case providing a uniq resource int the output (eg: SCS)

|meta-data| Description| Mandatory |
|---      |:-:  |:-: |
|Publication-id| Dataset identifier that can be used for citation | yes |
|Curation-level| Controled vocabulary | |
|Resource-version| Dataset version od last release | |
|Rights| Licence URI | |
|Rights-type| Licence type (eg: CC-by, CC-0, private, public) | |
|Copyrights| Copyright text | |
|Author| Dataset Author(s) or group | |
|Publication-ref| Identifier of the original resource that can be an article or the origin Data Center| 
|Editor| editor name| |
|Publication-date| Date of the original publication | |

**Publication-id**: can be prefixed with the identifier type:
eg: bibcode:...
    doi:...
    ror:...

Serialisation example:  &lt;info&gt; tag makes the jobs. see <a href='tests/J_AJ_161_36_table8.xml'>SCS example</a>


Complex output involving several datasets (eg: TAP query, ObsCore result)
Dataset-origin depends on each table used for the output. Datamodels like Last-step -Provenance or DatasetDM allows to gather the metadata.

DatasetDM Example:

|meta-data| Description| Mandatory |
|---      |:-:  |:-: |
|dataset:productType|||
|dataset:productSubType| controled vocabulary||
|dataset:DataID.datasetDID| dataset ivoid|yes|
|dataset:DataID.title| dataset title||
|dataset:DataID.creationType| type of resource ||
|dataset:DataID.date| Publication date of original dataset/article||
|dataset:Party.name| (first)Author | |
|dataset:Curation.publisherDID| data-center identifier (ivoid)|yes|
|dataset:Curation.rights| rights text| |
|dataset:Curation.releaseDate| Data-center publication date|yes|
|party.Organisation.email|Data-center contact||
|dataset:Curation.doi| Dataset DOI| |
|dataset:Curation.bibcode| Dataset bibcode||

Serialisation example:  DatasetDM serialisation. see <a href='tests/tap.xml'>TAP example</a>



This document describes simple means to declare basic provenance
information in the [Virtual Observatory](https://ivoa.net).

Stable versions of this document are available through the [IVOA
document repository](http://ivoa.net/documents/).

To build a PDF version this document, you will need a reasonably
complete LaTeX installation, a sufficiently capable `make`, preferably
[latexmk](https://personal.psu.edu/~jcc8/software/latexmk/) and probably
[rsvg-convert](https://wiki.gnome.org/Projects/LibRsvg). For further
details, see [ivoatexDoc](https://ivoa.net/documents/Notes/IVOATex/).

This document is distributed under CC-BY-SA.
