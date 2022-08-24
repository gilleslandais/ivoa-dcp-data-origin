# Data Origin in the VO

The goal of the document is to make the Data Origin more visible in
the query results executed in the **Virtual Observatory**. The document lists
meta-data required to provide sufficient **traceability** to end-users in order to
improve the understanding of the resultsets and enabling its reuse and its
**citation**.


## Use cases


- To provide basic provenance information in VO output(authors, dates, article, DOI,...)<br/>
The basics metadata should contain the data origin (space agency or
authors, article references), the data center providing the resource, the date
of publication ...
- To trace data origin: query, resources used to compute the result...
(for instance, xmatch 2 tables)
- To homogenize the Origin metadata in VO output.<br/>
The Richness and quality of Origin information provided in VOTable depends of the data center implementation.<br/>
*Example: the same TAP query on Gaia catalogue executed by different services (hosted by datacenter like ESA, CDS, Gavo, etc.)
provides more or less information on the origin of data (often serialized with the "INFO" tag and a name convention specific to each).*
- Relevant metadata for final users to **cite** resources
- Fill the AAS citation template (G.Muench).<br/>
*Example : "we searched optical astrometric data of these sources from
the Gaia (Gaia Collaboration et al. 2016) Early Data Release 3 (Gaia
Collaboration et al. 2021) via the Gaia archive (Gaia Collaboration
2020)."*
- Relevant metadata for final users to understand data origin.<br/>
Table provided by a Datacenter can be a copy of an existing resource.
For instance, a table published in a journal or by a Space Agency is
also hosted in a Data Center like CDS, GAVO, etc. The data curation
depends of the Data Center which can add associated data, enrich
meta-data (eg: add filter for magnitude) or make a sub-selection of
columns.
- Give me a bibliography of everything I've used in the workflow" (M.Demleitner)
- <span style='color:red'>**What else ? ....**</span>

## Metadata expected
Tracing Data origin can be complex. It depends on the granularity expected.
- A basic approach consists to add information using key=value pairs. Each interaction is independent with no interaction with each other. This approach could be generally serialized in VOTable using the INFO tag.
- An advanced approach consists in a rich serialization that allows information to interact. Typically a resource can be attached to an agent (a Person or an institute).
This approach requires an advanced VOTable serialization, a remote Provenance service or a TAP schema evolution.

As a prelimiary work, We will limit the investigation to the DCP scope by listing the relevant information from either approach.

### Basic metadata
The following metadata can be repeated and could follow a controlled vocabulary.

#### Involved agents 
- Author: name or orcid
- Editor: name or URL
- Journal: name or URL
- Organization: name or URL
- Datacenter that provides the result: name or URL

#### Involved resources
- Resource Identifier: ivoid of resource(s) hosted by the service which provides the result
- Resource citation: DOI, bibcode of resource(s) hosted by the datacenter which returns the result
- Remote resource identifier: a remote ressource which was used to build the result
- Remote resource citation: a remote ressource which was used to build the result

#### Curation information
- publication date
- Curation level
- Licence: free text
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


