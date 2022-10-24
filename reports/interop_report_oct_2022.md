(DRAFT -  Sorry about the grammar and spelling...)

# DCP splinter Data Origin GatherTown, Interop, 20th oct 2022

14 participants

presentation of the metadata origin, use cases, plan

## Topics discussed
- linking resources in vo registry
- licences
- citation and the DOI role
- what can be cited ?


## Linking resources
the registry as well as the DOI enables to make link between resources (relatedIdentifier can be enriched with a controlled semantic to specify the nature of the relation).
This capability is not very used today and when it exists, its coverage is limitted and difficult to exploit.
For instance VizieR provides links to other VizieR resources and sometimes URL to agencies who produced the data.

Linking resources enables to link derived product to their original repository. Bibcode is also available in the registry and can be used to link litterature.

For derived resources, the status of the dataset (copy, subset, etc.) could qualify the resource originality. This metadata doesn't exist today in registry.
eg:
- VizieR provides a subset of SDSS tables
- HiPS contains metadata that includes the provenance of the previous HiPS nodes (it is include in the Hipsgen tool) - see talk M.Buga, interop 2022.

We underlined the differences existing for the same dataset in multiple data centers. The data centers can make subset and can enrich data !
The Data-Center provenance becomes an important information for citation. 

## Licences
Licences with identifiers are required by FAIR principles: see GOFair: https://www.go-fair.org/fair-principles/

Licences information is required for end-users. The license should be provided in a machine-readable representation!
Some existing softwares can already detect if a configuration can be used according to licenses. 
Then, it is recommended to add URI licenses (eg: http://creativecommons.org/licenses/by-sa/2.0/legalcode) - (ndlr: Are there a standard way to specify licenses? DOI? URL?)

**Multiple lisences** are clearly to avoid! In the worst case, they could be incompatible with unusable consequences.
The use case of dataset resulting from compilation having 2 licences is clearly to avoid! The capability of multiple licenses has been deprecated in the registry.

When mutliple licenses are needed, they often point 2 distincts resources (eg: HiPS property file): 
for instance a license on the data + a license on the service. The best approach consists to separate the 2 resources: each having his own lisence.

**Copyright is accepted by FAIR principle.**
But copyright is only a link to the data producer. It gives the contact point to any users who would like to use data.
Copyright is more simple to implement for data-center that provides a copy of original resource, but its use is not well integrated in an interoperable workflow.


## VO citation
is it possible to cite a VO Resource? 

The question interests AAS: to cite VO resources goes in the direction of reproducibility (encouraged by editors) . Then, to find a method could be good!

To generate a DOI for a query is a possibility and has already been implemented. This type of architecture could generates a lot of DOI and is clearly an advanced implementation (and not always adapated with Data centers requirements).

ivoid is not citable because there are no guaranty of sustainability.
ADS tested VO harvesting in the past with a result that has not convinced it! But the question stays open and depends of the current registry quality ?

The amounts of data is also to take into account. Dataset indexation in ADS is submitted to requirements: it needs METADATA, a clear ownership and DOI is preferable (talk Alberto Accomazzi, interop 2022)
ADS philosophy consists to provide link to resources having a potential impact - to make an automated choice in a VO registry harvesting is clearly not feasible today.

ADS underlines also the bibcode limits (tech limitation issues of 19 char) and encourages DOI !
DOI exists in registry : is DOI harvesting in registry relevant ? We noted that DOI can be the resource itself or an other linked resource (article, service...)


For dataset not selected in ADS or having no DOI; can we propose acknowledgment ? 
Could we propose a template (may be filled in registry), based on the AAS template ?  Question stays open? and is it feasible?


We proposed to divide the question to use cases and to check the feasability.
1) find acknowledgment 
2) find citing
3) reproducibility

Question: Is it possible to add a bibtex section with ivoid reference? 
for instance VizieR provides in the DOI metadata an alternate identifier to link the VO resource (using ivoid identifier)


## Todo
- make a list of metadata
- propose output on a concret basis: VOTable, registry, python service or API



