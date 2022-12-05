""" Get metadata from ADS
    G.Landais (CDS) 17-apr-2018
"""

import sys
import os
import logging
import getopt
import json

from urllib import request, parse

ADS_META = ["abstract", "ack", "aff", "alternate_bibcode", "alternate_title", "arxiv_class", "author",
            "bibcode", "bibgroup", "bibstem", "body*", "citation_count", "copyright", "data", "database",
            "doi", "doctype", "first_author", "grant", "id", "identifier", "indexstamp", "issue", "keyword",
            "lang*", "orcid_pub", "orcid_user", "orcid_other", "page", "property", "pub", "pubdate",
            "read_count", "title", "vizier", "volume", "year"]

ADS_DEFAULT_META = ["author", "first_author", "id", "identifier", "doi", "orcid_pub", "orcid_user", "orcid_other", "copyright"]

ADS_URL = "https://api.adsabs.harvard.edu"


class adsbib:

    def __init__(self, certs=None):
        """Constructor
        :param certs: ADS token file
        """
        self.__csrf = self.__getcsrf(certs)

    def __getcsrf(self, certs):
        try:
            if certs is None:
                certs = ".ads"

            with open(certs, "r") as fd:
                csrf = fd.read().strip()
        except Exception as e:
            raise Exception("Error getting file certification {0}: {1}".format(certs, str(e)))

        return csrf

    def get(self, bibcode:str=None, doi:str=None)->str:
        """get ADS data
        :param name: list of metadata to retrieve (default see ADS_DEFAULT_META)
        :return: the result in a dictionary
        """
        url = f"{ADS_URL}/v1/export/bibtex"
        logging.info(f"url {url}")

        if bibcode:
            enc_bibcode = bibcode.replace("&","%26")
            data = bytes('{"bibcode":["'+enc_bibcode+'"]}', "utf-8")
        elif doi:
            data = bytes('{"bibcode":["'+bibcode+'"]}', "utf-8")
        else:
            raise Exception("bibcode or DOI are required")
        try:
            req =  request.Request(url, data=data)
            req.add_header("Authorization", "Bearer:"+self.__csrf)
            logging.debug(f"url {url} -H Authorization: Bearer:{self.__csrf}")

            fd = request.urlopen(req)
            data = json.loads(fd.read().decode('utf8'))
            fd.close()

            if "export" in data:
                return data["export"]
            return None
        except Exception as e:
            raise Exception(f"Error getting ADS {e}")


if __name__ == "__main__":

    try:
        __opt, __args = getopt.getopt(sys.argv[1:], 'b:d:h', ["help", "bibcode=", "doi="])
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(1)

    __bibcode = None
    __doi = None
    for __o, __a in __opt:
        if __o in ("-h", "--help"):
            help("__main__")
            sys.exit(0)
        elif __o in ("-b", "--bibcode"):
            __bibcode = __a
        elif __o in ("-d", "--doi"):
            __doi = __a

    ads = adsbib()
    if __bibcode:
        print(ads.get(bibcode=__bibcode))
