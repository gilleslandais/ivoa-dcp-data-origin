# Data Origin in the VO

The goal of the document is to make the Data Origin more visible in
the query results executed in the Virtual Observatory. The document lists
meta-data required to provide sufficient **traceability** to end-users in order to
improve the understanding of the resultsets and enabling its reuse and its
**citation**.


## Use cases


- To get basic provenance information in VO output(authors, dates, article, DOI,...)<br/>
The basics meta-data should contain the data origin (space agency or
authors, article references), the data center providing the resource, the date
of publication ...
- To trace data origin: query, resuources used to compute the result...
- To homogenize the Origin-metadata information in VO output.<br/>
*Example: Query the Gaia catalogue using VO services (for instance
with topcat or any other VO-software). The registry lists Data Center
(eg: Gavo, VizieR, ESA) which provides Gaia tables using TAP. The
results returns VOTable having information in the header. However,
the information depends of the implementation.*
- Relevant meta-data for final users to **cite** resources
- Fill the AAS citation template (G.Muench).<br/>
*Example : "we searched optical astrometric data of these sources from
the Gaia (Gaia Collaboration et al. 2016) Early Data Release 3 (Gaia
Collaboration et al. 2021) via the Gaia archive (Gaia Collaboration
2020)."*
- Relevant meta-data for final users to understand data origin.<br/>
Table provided by a Data Center can be a copy of an existing resource.
For instance, a table published in a journal or by a Space Agency is
also hosted in a Data Center like CDS, GAVO, etc. The data curation
depends of the Data Center which can add associated data, enrich
meta-data (eg: add filter for magnitude) or make a sub-selection of
columns.
- Give me a bibliography of everything I’ve used in the workflow" (M.Demleitner)


## Metadata expected
Metadata that can enrich a VOTable output:

- Agents: author(s) / Institue / Space agency / Editor / Journal
- Origin reference: article ref., etc.
- Provider, Datacenter, Creator
- Date(s)
- Identifier: DOI, bibcode...
- Access protocol
- Licences
- Curation level
- Any additional information in text plain that complete the result
- ...?
