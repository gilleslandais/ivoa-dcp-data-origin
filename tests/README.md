# VOTable Serialisation example

2 example of Data-origin serialication.

- simple case based on &lt;INOF&gt; involving a unique table (eg: SCS)
- case based on Data-models (DatasetDM) for result involving 2 tables


## Python implementation 

the current implementation exploit VOTAble and registry metadata. It is in a devleoppement phase.
The code enables to search information and propose an api to cite a resource. Citing required a DOI, 
The code returns the ADS bibtex (completed with iovoid value) or create a bibtex from meta-data in registry.

Note that ADS bibtex is better and more clean!

**Note:** the mivot and ads library are not public , but just here as example -

```
$ python3 dataorigin.py -h
```

Data-origin from registry using ivoid
```
$ python3 dataorigin.py -i ivo://nasa.heasarc/gc47tuccxo
$ python3 dataorigin.py -i "ivo://cds.vizier/i/355"
```

Data-origin from Simple-cone-search
```
$ python3 dataorigin.py -f J_AJ_161_36_table8.xml
```

Data-origin from DatasetDM serialisation
```
$ python3 dataorigin.py -f tap.xml -t VODML
```



