"""by G.Landais (CDS) 2022-11-01
   Data Origin (test)
 

   Usage: dataoroigin.py [-h] [-f votable [-t type]] | [-i ivoid]
      -h: help
      -f: VOTable filename
      -t: VOTable type:("VOTable" or "VODML")
      -i: ivoid (search into registry)


   Notes:
   - howto extract XML from astropy.table.Table ?  <- not possible!..
   - check data origin usinf relatedIdentifier ?
        - <relatedIdentifier>: http://www.ivoa.net/rdf/voresource/relationship_type eg: isDerivedFrom
   - Make a acknowledgment template
        - in registry: could we have a new field <acknowledgment> ?
   - mivot: use L.Michel library..
   - datasetDM: hoto add related identifier ?
   - use  LastStepProvenance insteadof DatasetDM ?
"""


import astropy.io.votable as vot
from astropy.table import Table
import numpy as np
import urllib.request
import urllib.parse
import requests as rq
import xml.etree.ElementTree as ET
import lxml.etree as etree
import re
import logging

import adsbib

DATA_ORIGIN_REQ = ("ivoid", "publisher", "version", "protocol", "request", "request_date", "contact", "landing_page")
DATA_ORIGIN_PROV = ("publication_id", "curation_level", "resource_version", "rights", "title", # DataCenter info
                    "creator", "related_resource", "editor", "publication_date", "resource_date") # bibliographic/origin info
DATA_ORIGIN_DML= ("product_type", "product_sub_type", "did", "title", "creationType", "date", "author", "pud_did", "rights", "release_date", "contact", "doi", "bibcode")

REGISTRY_SERVER = "https://dc.zah.uni-heidelberg.de/rr/q/pmh/pubreg.xml"
ADS_URL = "https://api.adsabs.harvard.edu/v1/"


class DataOrigin:
    """interface"""
    def print(self):
        print(str(self))
    def print_info(self):
        pass
    def cite(self):
        raise Exception("Cite not available yet")
    def ack(self):
        raise Exception("Ack not available yet")

 
class DataOriginRegistry(DataOrigin):
    """Extract Data Origin from IVOA registry
    """
    def __init__(self, ivoid:str, registry:str=REGISTRY_SERVER, filename:str=None):
        self.__ivoid = ivoid
        self.__registry = registry
        if filename:
            with open(filename, "r") as fd:
                xml = fd.read().decode("utf-8")
        else:
            #ivoid = urllib.parse.quote(ivoid)
            req = urllib.request.Request(url=f"{registry}?verb=GetRecord&metadataPrefix=ivo_vor&identifier={ivoid}")
            with urllib.request.urlopen(req) as f:
                xml = f.read().decode("utf-8")

        self.__xml = ET.fromstring(xml)
        self.info = self.__get_registry_info()


    def __get_registry_info(self):
        root = self.__xml
        h = {}
        elt = root.findall(".//curation/publisher")[0].attrib["ivo-id"]
        if elt: h["publisher"] = root.findall(".//curation/publisher")[0].text

        author = []
        for elt in root.findall(".//curation//creator/name"):
           author.append(elt.text)
        if len(author)>0:
           h["creator"] = ",".join(author)

        elt = root.findall(".//curation/date[@role='Created']")
        if elt:
           h["publication_date"] = elt[0].text

        elt = root.findall(".//curation/contact/email")
        if elt:
            h["contact"] = elt[0].text

        elt = root.findall(".//content/type")
        if elt:
            h["type"] = elt[0].text

        elt = root.findall(".//content/contentLevel")
        if elt:
            h["curation_level"] = elt[0].text

        elt = root.findall(".//rights")
        if elt:
            h["rights"] = elt[0].text
        
        elt = root.findall(".//content/referenceURL")
        if elt:
            h["landing_page"] = elt[0].text

        elt = root.findall(".//identifier")
        if elt:
            h["ivoid"] = elt[0].text

        
        elt = root.findall(".//title")
        if elt:
            h["title"] = elt[0].text

        for elt in root.findall(".//altIdentifier"):
            if elt.text.find("doi:") > -1:
                h["doi"] = elt.text # only one DOI

        source=[]
        for elt in root.findall(".//content/source"):
            source.append(f"{elt.attrib['format']}:{elt.text}")
        h["source_origin"] = ",".join(source)

     
        return h

    def print_info(self):      
        print(f"RESOURCE {self.__ivoid} (from registry):")
        for key in self.info:
            print(f"{key:<20}:{self.info[key]}")

    def cite(self):
        """Citation using registry metadata requires DOI
        """
        if "doi" not in self.info:
            raise Exception("DOI is required for citation")

        print("@dataset{")
        if "doi" in self.info: 
            print(f"  doi={{{self.info['doi']}}},")
        if "title" in self.info:
            print(f"  title={{{self.info['title']}}}")
        if "creator" in self.info:
            print(f"  authors={{{self.info['creator']}}},")

        ivoid_cite = f"{self.__registry}?verb=GetRecord&metadataPrefix=ivo_vor&identifier={self.__ivoid}"
        print(f"  url={{{ivoid_cite}}},")
        if "publisher" in  self.info:
            print("  publisher={"+self.info["publisher"]+"},")
        version = ""
        print("  ivoid={"+self.__ivoid+"},")
        if "version" in self.info:
            version += "(version "+self.info["version"]+")"
        if "publication_date" in self.info:
            version += " executed at "+self.info["publication_date"]
        if version != "":
            print("  version={"+version+"}\n")

        print("}")


class VOFileDataOrigin(DataOrigin):
    """extract Data Origin from VOTable
    """
    def __init__(self, votable:vot.tree.VOTableFile, registry:str=REGISTRY_SERVER):
        self.__votable = votable
        self.ivoid = None
        self.data_origin = self.__extract_data_origin_from_info()
        self.data_request = self.__extract_request_from_info()
    
    def __extract_data_origin_from_info(self):
        """the idea is to populate a table with data origin info""" 
        data = []
        for key in DATA_ORIGIN_PROV:
            try:
                elt = self.__votable.get_info_by_id(key)
            except Exception as e:
                logging.warning(e)
                data.append(None)
                continue
            data.append(elt.value)
        return Table(np.array(data), names=DATA_ORIGIN_PROV)
    
    def __extract_request_from_info(self):
        h = {}
        try:
            # Note ivoid could be multiple in case of xmatch/TAP
            self.ivoid = [self.__votable.get_info_by_id("ivoid").value]
        except :
            name = self.__votable.resources[0].name
            if name and name[0] in ('IVXJB') and name[1] == '/': #vizier
                self.ivoid = ["ivo://cds.vizier/"+name.lower()]
            else:
                raise Exception("ivoid is required") 

        for key in DATA_ORIGIN_REQ:
            try:
                h[key] =  self.__votable.get_info_by_id(key).value
            except Exception as e:
                logging.warning(e)
        return h


    def print(self):
        for key in self.data_request:
            print(f"{key}: {self.data_request[key]}")        

    def print_info(self):
        for rec in self.data_origin:
            print(f"RESOURCE {self.ivoid[0]} (from VOTable)")
            print(f"{'ivoid':<20}:{self.ivoid[0]}")
            for key in  DATA_ORIGIN_PROV:
                if rec[key] != None:
                    print(f"{key:<20}:{rec[key]}")
 
    def cite(self) :
        """use VOTable header only"""
        bibtex = "% Protoype to cite a VO-query ?\n"
        bibtex += "@query{\n"
        bibtex += "  ivoa={"+",".join(self.ivoid)+"}\n"
        if "publisher" in  self.data_request:
            bibtex += "  publisher={"+self.data_request["publisher"]+"}\n"
        version = ""
        if "protocol" in self.data_request:
            version += self.data_request["protocol"]+" "
        if "version" in self.data_request:
            version += "(version "+self.data_request["version"]+")"
        if "request_date" in self.data_request:
            version += " executed at "+self.data_request["request_date"]
        if version != "":
            bibtex += "  version={"+version+"}\n"
        if "request" in self.data_request:
            bibtex += "  url={"+self.data_request["request"]+"}\n"
        bibtex += "}" 
        print(bibtex)

    def ack(self):
        """acknowledgment using VOTable header only
           needs: ivoid, publisher, protocol, version
                  source_origin , author, date_origin
        """
        protocol = "?"
        if "protocol" in self.data_request:
            protocol = self.data_request["protocol"]
        datacenter = "?"
        if "publisher" in self.data_request:
            datacenter = self.data_request["publisher"]
        version = "?"
        if "version" in self.data_request:
            version = self.data_request["version"]
        qdate = "?"
        if "request_date" in self.data_request:
            qdate = self.data_request["request_date"]
        

        author = "?"
        if "creator" in self.data_origin:
            author = self.data_origin["creator"]
        source_origin = "?"
        if "source" in  self.data_origin:
            source_origin = self.data_origin["source"]
        date_origin = "?"
        if "date" in  self.data_origin:
            date_origin = self.data_origin["date"]


        import textwrap
        print("\n".join(textwrap.wrap(f"""(from VOTable)\nWe extract data published in {source_origin} ({author}, {date_origin}),
via {datacenter} services (ivoa resource={self.__ivoid}, {pubdate})
using {protocol} (version {version}, executed at {qdate})""", width=80)))



class VODMLFileDataOrigin(DataOrigin):
    """extract Data Origin from VOTable (VODMLite/mivot)
    """
    def __init__(self, filename:str):
        self.__filename = filename
        self.ivoid = None
        self.data_origin = self.__extract_data_origin_from_info()
        #self.data_request = self.__extract_request_from_info()

    def __extract_data_origin_from_info(self):
        """the idea is to populate a table with data origin info""" 

        import mivot

        with  open(self.__filename, "r") as fd:
            xml = fd.read()

        xml_piece = mivot.extract_vodml_from_votable(xml)
        parser = mivot.vodml_parser(xml_piece)
        root = parser.parse()
       
        data = []
        coll = parser.search("dataset:Dataset")
        if coll is None :
            return

        for dset in coll[0]:
            product_type = parser.search("dataset:productType", dset)[0].value
            product_sub_type = parser.search("dataset:productSubType", dset)[0].value
            did = parser.search("dataset:DataID.datasetDID", dset)[0].value
            title = parser.search("dataset:DataID.title", dset)[0].value
            creationType = parser.search("dataset:DataID.creationType", dset)[0].value
            date = parser.search("dataset:DataID.date", dset)[0].value
            author = parser.search("dataset:Party.name", dset)[0].value
            pud_did = parser.search("dataset:Curation.publisherDID", dset)[0].value
            rights = parser.search("dataset:Curation.rights", dset)[0].value
            release_date = parser.search("dataset:Curation.releaseDate", dset)[0].value
            contact = parser.search("party.Organisation.email", dset)[0].value
            doi = parser.search("dataset:Curation.doi", dset)[0].value
            bibcode = parser.search("dataset:Curation.bibcode", dset)[0].value
            
            data.append((product_type,product_sub_type,did,title,creationType,date,author,pud_did,rights,release_date,contact,doi,bibcode))
        return Table(np.array(data), names=DATA_ORIGIN_DML)
    
    def print_info(self):
        for rec in self.data_origin:
            print("-----------------------------------")
            print(f"RESOURCE {rec['did']} (from VOTable)")
            print(f"{'ivoid':<20}:{rec['did']}")
            for key in  DATA_ORIGIN_DML:
                if rec[key] != None:
                    print(f"{key:<20}:{rec[key]}")



class VOCite:
    def __init__(self, ivoid):
        self.__ivoid = ivoid
        self.__registry_info = None  

    def get_registry_info(self):
        if self.__registry_info:
            return self.__registry_info

        self.__registry_info = DataOriginRegistry(self.__ivoid)

        return self.__registry_info

    def cite_source_origin(self):
        """- use ADS if resource exist : from bibcode/DOI
           - use registry (if DOI exists?)
        """
        info = self.get_registry_info()

        if "source_origin" in info.info:
            source = info.info["source_origin"].replace("\n","")
            mo = re.match(".*bibcode:([^ ]+).*$", source)
            if mo is None:
                mo = re.match(".*(\d{4}[a-zA-Z]+[a-zA-Z0-9.]+).*$", source)
            if mo:
                ads = adsbib.adsbib()
                try:
                    export_citation = ads.get(bibcode=mo.group(1))
                    if export_citation:
                        print("%ADS export (from bibcode)\n")
                        export_citation = re.sub("adsnote =","  ivoid = {"+self.__ivoid+"},\n  adsnote =", export_citation)
                        print(export_citation)
                        return
                except Exception as e:
                    logging.debug(e)

            mo = re.match(".*doi:([^ ]+).*$", info.info["source_origin"])
            if mo:
                ads = adsbib.adsbib()
                try:
                    export_citation = ads.get(doi=mo.group(1))
                    if export_citation:
                        print("%ADS export (from doi)\n")
                        export_citation = re.sub("adsnote =","  ivoid = {"+self.__ivoid+"},\n  adsnote =", export_citation)
                        print(export_citation)
                        return
                except Exception as e:
                    logging.debug(e)
                return

    def cite(self):
        info = self.get_registry_info()
        info.cite()

    def ack(self, vofile:VOFileDataOrigin=None):
        data_request = vofile.data_request
        protocol = "?"
        if "protocol" in data_request:
            protocol = data_request["protocol"]
        datacenter = "?"
        if "publisher" in data_request:
            datacenter = data_request["publisher"]
        version = "?"
        if "version" in data_request:
            version = data_request["version"]
        qdate = "?"
        if "request_date" in data_request:
            qdate = data_request["request_date"]

        reg_info = self.get_registry_info()
        info = reg_info.info
        pubdate = ""
        if "version" in info:
            pubdate += "(version "+info["version"]+")"
        if "publication_date" in info:
            pubdate += info["publication_date"]
        source_origin = ""
        if "creator" in info:
            author = info["creator"].split(",")[0]
        if "source_origin" in info:
            source_origin = info["source_origin"]
        if "datacenter" in info:
            datacenter = info["datacenter"]
        else:
            print("not available yet")
               
        date_origin = "???"
        if "date" in info:
            date_origin = info["date"]

        import textwrap
        print("\n".join(textwrap.wrap(f"""We extract data published in {source_origin} ({author}, {date_origin}),
via {datacenter} services (ivoa resource={self.__ivoid}, {pubdate})
using {protocol} (version {version}, executed at {qdate})""", width=80)))

        


if __name__ == "__main__":
    import sys
    import getopt

    try:
        __opts, __args = getopt.getopt(sys.argv[1:], "ah:t:f:i:", ["help", "type=", "file=", "ivoid=","ads"])
    except getopt.GetoptError as err:
        help("__main__")
        sys.exit(1)

    __filename = None
    __ivoid = None
    __type = "VOTable"
    __use_ads = False

    for __o, __a in __opts:
        if __o in ("-f", "--file"):
            __filename = __a
        elif __o in ("-h", "--help"):
            help("__main__")
            sys.exit(0)
        elif __o in ("-i", "--ivoid"):
            __ivoid= __a
        elif __o in ("-t", "--type"):
            __type = __a
        elif __o in ("-a", "--ads"):
            __use_ads = True

    if __ivoid :
        regdataorig = DataOriginRegistry(__ivoid)

        print("\nGET Data Origin (from registry)")
        regdataorig.print_info()
        
        print("\nCITE a resource (from Registry)")
        try:
            regdataorig.cite()
        except Exception as e:
            logging.error(e);

        if __use_ads:
            try:
                vocite = VOCite(__ivoid)
                print("\nCITE the \"source origin\" (using ADS or registry)")
                vocite.cite_source_origin()
            except Exception as e:
                logging.error(e)

    elif __filename and __type == "VOTable":
        table = vot.parse(__filename)
        vodatorig = VOFileDataOrigin(table)
        regdataorig = DataOriginRegistry(vodatorig.ivoid[0])

        print("GET Data Origin - basic (from VOTable)")
        vodatorig.print()
        print("\nGET Data Origin (from VOTable)")
        vodatorig.print_info()

        print("\nGET Data Origin (from registry)")
        regdataorig.print_info()
        print("\nCITE a VO query (from VOTable)")
        vodatorig.cite()

        try:
            print("\nCITE a resource (from Registry)")
            regdataorig.cite()
        except Exception as e:
           logging.error(e)

        try:
            vocite = VOCite(vodatorig.ivoid[0])
            if __use_ads:
                print("\nCITE the \"source origin\" (using ADS or registry)")
                vocite.cite_source_origin()
        except Exception as e:
            logging.error(e)

        print("\nAck (from VOTable+registry)")
        vocite.ack(vodatorig)

    elif __filename and __type == "VODML":
        vodatorig = VODMLFileDataOrigin(__filename) #TODO use votable astropy

        print("\nGET Data Origin (from VOTable)")
        vodatorig.print_info()

        print(vodatorig.data_origin)

        #print("\nCITE a VO query (from VOTable)") TODO
        #vodatorig.cite()

        #for ivoid in vodatorig.data_origin["did"]: TODO
        #    vocite = VOCite(ivoid)
        #    print("\nCITE the \"source origin\" (using ADS or registry)")
        #    vocite.cite_source_origin()

        #    print("\nAck (from VOTable+registry)")
        #    vocite.ack(vodatorig)



