# VOTable Serialisation example

2 examples of Data-origin serialication.

- simple case based on &lt;INFO&gt; for VOTable having a unique table (eg: SCS)
- case based on Data-model (DatasetDM) for VOTable having 2 tables


## Python implementation 

the current implementation exploits VOTable and registry metadata. It is in developement phase.
The code enables to get Data-origin information and provides an api to cite the resource. Citing requires DOI.
The code returns the ADS bibtex (completed with ivoid value) or makes a bibtex from meta-data in registry.

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



