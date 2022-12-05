#!/usr/bin/python3
""" G.Landais (CDS)
    apr-2021
    manage vodmlinstance in VOTable

    parse vodmlinstance and store in classes.

    parser = vodml_parser(xml_piece)
    root = parser.parse()
    print(root)
    elements = parser.get("dmrole")
    ...

    main node is model_instance which contains global/table_mapping/template
    cf global, table_mapping, template which inherits from node class

    main test programme: 

    ./voldmlinstance.py votable.vot
    cat file | ./voldmlinstance.py 
"""

import logging
import re, sys

NODE_ATT = 1
NODE_INSTANCE = 2
NODE_COLLECTION = 3
NODE_GLOBAL = 4
NODE_MODEL = 5
NODE_TEMPLATES = 6
NODE_REF = 7

NODE_NAME = {
NODE_ATT : "attribute", 
NODE_INSTANCE : "instance",
NODE_COLLECTION : "collection",
NODE_GLOBAL :"global",
NODE_MODEL : "model",       #<MODEL>
NODE_TEMPLATES : "templates", #<TEMPLATES>
NODE_REF : "reference",
}

class Out:
    def __init__(self, out=sys.stdout):
        self.out = out
        self.indent = 0

    def write(self,s):
        self.out.write(2*self.indent*" "+s)

STDOut = Out(sys.stdout)

class Node:
    """base Node"""
    def __init__(self, nodetype:int, dmrole:str=None, dmtype:str=None, id:str=None):
        """Node Constructor 
        :param nodetype: NODE type (int)
        :param dmrole: DataModel role
        :param dmtype: DataModel type 
        :param id: identifier in the <votable> 
        """
        self.__type = nodetype
        self.__dmtype = dmtype
        self.__dmrole = dmrole
        self.id =  id

    def nodetype(self)->int:
        """get Node type
        :return: Node type (int)
        """
        return self.__type

    def dmtype(self)->str:
        """get DataModel type (instance type)
        :return: DataModel type
        """
        return self.__dmtype

    def dmrole(self)->str:
        """get DataModel role
        :return: DataModel role
        """
        return self.__dmrole

    def print(self, out=STDOut):
        """print out
        :param out: output stream
        """
        opt = ""
        if self.__dmrole:
            opt= f" dmrole='{self.__dmrole}'"
        if self.__dmtype:
            opt= f" dmtype='{self.__dmtype}'"
        if self.id:
            opt= f" dmid='{self.id}'"
        out.write(f"<{NODE_NAME[self.__type]} {opt}/>")

    def __str__(self)->str:
        return f"<Node({NODE_NAME[self.__type]}): dmrole={self.__dmrole} dmtype={self.__dmtype} dmid={self.id}>"


class NodeIterable(Node):
    """Iterable Node"""
    def __init__(self, nodetype:int, dmrole:str=None, dmtype:str=None, id:str=None):
        """Iterable Node Constructor  (<COLLECTION>)
        :param nodetype: NODE type (int)
        :param dmrole: DataModel role
        :param dmtype: DataModel type 
        :param id: identifier in the <votable> 
        """
        super().__init__(nodetype, dmrole, dmtype, id)
        self.__child = []

    def append(self, child:Node):
        """add a new node
        :param child: new node
        """
        self.__child.append(child)

    def __iter__(self):
        self.__n = 0
        return self
    
    def __next__(self):
        if self.__n >= len(self.__child):
            raise StopIteration
        self.__n += 1
        return self.__child[self.__n-1]

    def __len__(self):
        return len(self.__child)

    def print(self, out:STDOut):
        """print out"""
        out.write(f"<!-- NodeIterable {NODE_NAME[self.nodetype()]} -->")

    def __str__(self)->str:
        s = f"<NodeIterable{NODE_NAME[self.nodetype()]}: dmrole={ self.dmrole()} dmtype={self.dmtype()} dmid={self.id}>"
        return s


class Attribute(Node):
    def __init__(self, dmrole, dmtype, id=None, value:str=None):
        super().__init__(NODE_ATT, dmrole, dmtype, id)
        self.value = value

    def print(self, out=STDOut):
        opt = ""
        if self.dmrole():
            opt += f" dmrole='{self.dmrole()}'"
        if self.dmtype():
            opt += f" dmtype='{self.dmtype()}'"
        if self.id:
            opt += f" dmid='{self.id}'"
        if self.value:
            opt += f" value='{self.value}'"
        out.write(f"<ATTRIBUTE {opt}/>\n")

    def __str__(self):
        return f"<Attribute: dmrole={self.dmrole()} dmtype={self.dmtype()} dmid={self.id} value={self.value}>"
        

class Instance(NodeIterable):
    def __init__(self, dmrole:str=None, dmtype:str=None, id:str=None):
        super().__init__(NODE_INSTANCE, dmrole, dmtype, id)

    def print(self, out=STDOut):
        opt = ""
        if self.dmrole():
            opt += f" dmrole='{self.dmrole()}'"
        if self.dmtype():
            opt += f" dmtype='{self.dmtype()}'"
        if self.id:
            opt += f" dmid='{self.id}'"
        out.write(f"<INSTANCE {opt}>\n")
        out.indent +=1
        for node in self:
            node.print(out)
        out.indent -=1
        out.write("</INSTANCE>\n")

    def get(self, dmrole:str)->Node: 
        """get the dmrole in an instancenode (unique by definition)
        :param dmrole: dmrole to search
        :return: the node
        """
        for node in self:
            if node.dmrole() == dmrole: return node


class Collection(NodeIterable):
    def __init__(self, dmrole:str):
        super().__init__(NODE_COLLECTION, dmrole)

    def append(self, child:Node):
        """add a new node
        :param child: new node
        """
        # check consistency
        ctype = child.nodetype()
        if ctype == NODE_COLLECTION:
            logging.error("Collection can't be child of Collection")
            return
        elif ctype in (NODE_INSTANCE, NODE_REF) :
            if child.dmrole() != None and child.dmrole() != "":
                logging.warning("dmrole is not accepted in Instance is a Collection child "+str(child))
         
        super().append(child)

    def print(self, out=STDOut):
        opt = ""
        if self.dmrole():
            opt += f" dmrole='{self.dmrole()}'"
        out.write(f"<COLLECTION {opt}>\n")
        out.indent +=1
        for node in self:
            node.print(out)
        out.indent -=1
        out.write("</COLLECTION>\n")

    def __str__(self):
        s =  f"<collection: dmrole {self.dmrole()}"
        for child in self:
            s += "\n  "+str(child)
        s += ">"
        return s
       

class Vodml:
    def __init__(self):
        self.models = None
        self.globals = Globals()
        self.templates = []

    def set_default_model(self):
        self.models = Model()
        self.models.name = "ivoa"
        self.models.uri = "https://www.ivoa.net/xml/VODML/IVOA-v1.vo-dml.xml"

    def print(self, out=STDOut):
        out.write("<RESOURCE type='meta'>")
        out.write("<VODML xmlns:dm-mapping='http://www.ivoa.net/xml/merged-syntax'>")
        out.write("<REPORT status='OK'>mivot.py mapping</REPORT>")
        if self.models:
            self.models.print(out)
        if self.globals:
            self.globals.print(out)
        for template in self.templates:
            template.print(out)
        out.write("</VODML>")
        out.write("</RESOURCE>")


class Globals(NodeIterable):
    def __init__(self):
        super().__init__(NODE_GLOBAL)
    
    def print(self, out=STDOut):
        out.write("\n<GLOBALS>\n")
        for node in self:
            node.print(out)
        out.write("</GLOBALS>\n")

    def __str__(self):
        s = "<globals: "
        for key in self:
            s += "\n  {}".format(key)
        s += ">"
        return s


class Reference(Node):
    def __init__(self, dmrole:str, ref:str=None, sourceref:str=None):
        super().__init__(NODE_REF, dmrole)
        self.ref = ref # INSTANCE 
        self.sourceref = sourceref

    def print(self, out:Out):
        opt = ""
        if self.dmrole():
            opt += f" dmrole='{self.dmrole()}'"
        #if self.dmtype():
        #    opt += f" dmtype='{self.dmtype()}'"
        if self.sourceref:
            opt += f" sourceref='{self.sourceref}'"
        if self.ref:
            opt += f" dmref='{self.ref}'"
        out.write(f"<REFERENCE {opt}/>\n")


class Model(Node):
     def __init__(self):
        super().__init__(NODE_MODEL)
        self.name = None
        self.syntax = None
        self.uri = None

     def print(self, out):
        opt = ""
        if self.name:
            opt += f" name='{self.name}'"
        if self.syntax:
            opt += f" syntax='{self.syntax}'"
        if self.uri:
            opt += f" url='{self.uri}'"

        out.write(f"<MODEL {opt}/>")

     def __str__(self):
        return f"<model: name={self.name}, syntax={self.syntax}, uri={self.uri}>"



class Template(NodeIterable):
    def __init__(self, table_ref:str):
        super().__init__(NODE_TEMPLATES)
        self.table_ref = table_ref

    def print(self, out:Out):
        opt = ""
        if self.table_ref:
            opt += f" tableref='{self.table_ref}'"
        out.write(f"<TEMPLATES {opt}>\n")
        out.indent += 1
        for node in self:
            node.print(out)
        out.indent -= 1
        out.write("</TEMPLATES>\n")

    def __str__(self):
        s = f"<template: {self.table_ref}"
        for col in self:
            s +="\n  "+str(col)
        s += ">"
        return s

""" Parser """
import xmltodict
#from lxml import etree

class vodml_parser:
    def __init__(self, doc:str):
        """Constructor
           :param doc: piece ox XML
        """
        self.__doc = doc
        self.__xml = xmltodict.parse(doc)['VODML']

        self.__ids = {} # list od ID available for dmref usage
        self.__dmrefs = [] # list of instance having dmref 
        self.__index = {} # dmrole index
      

    def get(self, dmrole:str) -> list:
        """get all node matching with dmrole
        :param dmrole: dmrole name
        :return: list of nodes
        """
        if dmrole in self.__dmroles:
            return self.__dmroles[dmrole]
        return None

    def parse(self):
        """parse xml and memorize
        """
        self.model = self.__fill_models()
        self.globals = self.__fill_globals()
        self.template = self.__fill_template()
        self.__resolve_dmrefs()

    def __resolve_dmrefs(self):
        for inst in self.__dmrefs:
            logging.debug("resolve dmref {}".format(inst.ref))
            if inst.ref not in self.__ids:
                logging.error("dmref {} is not resolved".format(inst.ref))
            else:
                inst.ref = self.__ids[inst.ref]

    def __get_att(self, doc, param):
        if param in doc: return doc[param]
        low = param.lower() 
        if low in doc: return doc[low]

    def __add_index(self, node:Node):
        print(f"add index {node}")
        role =  node.dmrole()
        if role is None: 
            return
        if role not in self.__index:
            self.__index[role] = []
        self.__index[role].append(node)


    def __fill_models(self):
        doc = self.__xml;
        if "MODEL" not in doc:
            return None

        models = []
        if isinstance(self.__xml["MODEL"], list):
            lmodels = self.__xml["MODEL"]
        else:
            lmodels = [self.__xml["MODEL"]]

        for instxml in lmodels:
            model = Model()
            if "@syntax" in instxml:
                model.syntax = instxml["@syntax"]
            if "@name" in instxml:
                model.name = instxml["@name"]
            if "@url" in instxml:
                model.uri = instxml["@url"]
            models.append(model)
        return models


    def __fill_template(self, doc):
        if "INSTANCE" in doc:
            logging.debug("add table_row_template/instance")
            return self.__fill_instance(doc["INSTANCE"])
        raise Exception("only INSTANCE are acceptable under TEMPLATES")

    def __fill_instance(self, inst)->Instance:
        if "@dmrole" in inst:
            dmrole = inst["@dmrole"]
        else:
            dmrole = None
        if "@dmtype" in inst:
            dmtype = inst["@dmtype"]
        else:
            dmtype = None
        if "@dmid" in inst:
            id = inst["@dmid"]
        else:
            id = None

        instance = Instance(dmrole, dmtype, id)
        if id:
            self.__ids[id] = instance

        self.__add_index(instance)
        return instance

    def __fill_attribute(self,att)->Attribute:
        if "@dmrole" in att:
            dmrole = att["@dmrole"]
        else:
            dmrole = None
        if "@dmtype" in att:
            dmtype = att["@dmtype"]
        else:
            dmtype = None
        if "@value" in att:
            value = att["@value"]
        else:
            value = None
        if "@dmid" in att:
            id = att["@dmid"]
        else:
            id = None

        attribute = Attribute(dmrole, dmtype, id, value=value)
        if id :
            self.__ids[id] = attribute

        self.__add_index(attribute)
        return attribute

    def __fill_reference(self,ref)->Reference:
        if "@dmrole" in ref:
            dmrole = ref["@dmrole"]
        else:
            dmrole = None
#        if "@dmtype" in ref:
#            dmtype = ref["@dmtype"]
#        else:
#            dmtype = None
        dmref = sourceref = None
        if "@dmref" in ref:
            dmref = ref["@dmref"]
        elif "@sourceref" in ref:
            sourceref = ref["@sourceref"]
        else:
            raise Exception("reference is needed")

        reference = Reference(dmrole, dmref, sourceref)
        self.__dmrefs.append(reference)
        self.__add_index(reference)
        return reference

    def __fill_collection(self, collection):
        if "@dmrole" in collection:
            dmrole = collection["@dmrole"]
        else:
            dmrole = None
        coll = Collection(dmrole)
        self.__add_index(coll)
        return coll
        
 
    def __fill_nodes(self, node:Node, doc):
        for name in doc:
            elt = doc[name]
            
            if name == "INSTANCE":
                if isinstance(elt, list):
                    for inst in elt:
                        instance = self.__fill_instance(inst)
                        node.append(instance)
                        self.__fill_nodes(instance, inst)
                else:
                    instance = self.__fill_instance(elt)
                    node.append(instance)
                    self.__fill_nodes(instance, elt)


            elif name == "ATTRIBUTE":
                if isinstance(elt, list):
                    for atts in elt:
                        att = self.__fill_attribute(atts)
                        node.append(att)
                else:
                    att = self.__fill_attribute(elt)
                    node.append(att)

            elif name == "COLLECTION":
                if isinstance(elt, list):
                    for colls in elt:
                        coll = self.__fill_collection(colls)
                        node.append(coll)
                        self.__fill_nodes(coll, colls)
                else:
                    coll = self.__fill_collection(elt)
                    node.append(coll)
                    self.__fill_nodes(coll, elt)

            elif name == "REFERENCE":
                if isinstance(elt, list):
                    for refs in elt:
                        ref = self.__fill_reference(refs)
                        node.append(ref)
                else:
                    ref = self.__fill_reference(elt)
                    node.append(ref)

 
    def __fill_globals(self)->Globals:
        glob = Globals()
        self.__fill_nodes(glob, self.__xml["GLOBALS"])
        return glob


    def __fill_template(self):
        if "@tableref" in self.__xml["TEMPLATES"]:
            tableref = self.__xml["TEMPLATES"]["@tableref"]
        else:
            tableref = ""
        template = Template(tableref)
        self.__fill_nodes(template, self.__xml["TEMPLATES"])
        return template

    def __search_index(self, role:str)->list:
        if role in self.__index:
            return self.__index[role]
        return None

    def search(self, role:str, node:Node=None)->Node:
        #logging.debug(f"..search {role} in {node}")
        matches = self.__search_index(role)
        if node is None:
           return matches
        if matches is None:
            return None
        nmatches = len(matches)

        result = []
        if isinstance(node, NodeIterable):
            for n in node:
                if n in matches: 
                    result.append(n)
                    if len(result) == nmatches: 
                        break

                if n.nodetype() == NODE_REF:
                    logging.debug("I add the ref")
                    if n.ref in matches:
                        result.append(n)
                        if len(result) == nmatches: 
                            break
                        continue

                if n.nodetype() == NODE_ATT:
                    continue

                f = self.search(role, n)
                if f: 
                     result += f
        else:
            if node in matches:
                return [node]
            if node.nodetype() == NODE_REF:
                if node.ref in matches:
                    result.append(node)
                
            f = self.search(role, node)
            if f: 
                return f

        if len(result) == 0:
           return None
        return result

#    def xpath(self, expression:str):
#        if self.__lxml is None:
#             self.__lxml = etree.parse(self.__doc)
#        l = tree.xpath(expression)
#        return l


def extract_vodml_from_votable(doc:str):
    """extract vodml piece
    :param doc: piece of xml(votable)
    :return: vodml sectionmeas:GenericMeasure.coord.value
    """
    # try tag <VODML>
    begin = doc.find("<VODML");
    if begin < 0:
        raise Exception("NO VODML found")
    end =  doc.find("</VODML>")
    if end < 0:
        raise Exception("NO VODML found")
    return doc[begin:end+8]
    

# -----------------------------------------------------------------------------
# TEST
# -----------------------------------------------------------------------------
def test_parser(filename:str):
    with  open(filename, "r") as fd:
        data = extract_vodml_from_votable(fd.read())
        parser =  vodml_parser(data)
        parser.parse()
        parser.globals.print()

        coll = parser.search("dataset:Dataset")
        print(coll)
        if coll is None:
            return
        for inst in coll[0]:
             print(f"look in  {inst}")
             s = parser.search('dataset:Curation.bibcode', inst)
             print("search dataset:Curation.bibcode = "+str(s))
        print("SEARCH dataset:Dataset.dataID = "+str(parser.search('dataset:Dataset.dataID')))


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    test_parser("tap.xml")

    #create
    vodml =  Vodml()
    vodml.set_default_model()
    global_node = vodml.globals
    
    collection = Collection(dmrole='dataset:Dataset')
    global_node.append(collection)

    # create first DatasetDM instance
    dset = Instance(dmtype='dataset:Dataset')
    collection.append(dset) 

    dset.append(Attribute(dmrole='dataset:productType', dmtype='ivoa:string', value='CATALOGUE'))
    dset.append(Attribute(dmrole='dataset:productSubType', dmtype='ivoa:string', value='Critical Comp.'))

    inst = Instance(dmrole='dataset:Dataset.dataID', dmtype='dataset:DataID')
    inst.append(Attribute(dmrole='dataset:DataID.datasetDID', dmtype='ivoa:string', value='ivo://CDS.VizieR.IV/39'))
    inst.append(Attribute(dmrole='dataset:DataID.title', dmtype='ivoa:string', value='TESS Input Catalog version 8.2 (TIC v8.2)'))
    inst.append(Attribute(dmrole='dataset:DataID.creationType', dmtype='ivoa:string', value='CATALOG_EXTRACTION'))
    inst.append(Attribute(dmrole='dataset:DataID.date', dmtype='ivoa:date', value='2021'))
    instcr = Instance(dmrole='dataset:DataID.creator', dmtype='Party')
    inst.append(instcr)
    instcr.append(Attribute(dmrole='dataset:Party.name', dmtype='ivoa:string', value='Paegert M.'))
    dset.append(inst)

    inst = Instance(dmrole='dataset:Dataset.curation', dmtype='dataset:Curation')
    dset.append(inst)
    inst.append(Attribute(dmrole='dataset:Curation.publisherDID', dmtype='ivoa:string', value='ivo://CDS'))
    inst.append(Attribute(dmrole='dataset:Curation.rights', dmtype='ivoa:string', value='https://cds.unistra.fr/vizier-org/licenses_vizier.html'))
    inst.append(Attribute(dmrole='dataset:Curation.releaseDate', dmtype='ivoa:date', value='2022-10-20T17:15:00Z'))
    instct = Instance(dmrole='dataset:Curation.contact', dmtype='party.Organisation')
    inst.append(instct)
    instct.append(Attribute(dmrole='party.Organisation.email', dmtype='ivoa:string', value='cds-question@unistra.fr'))
    inst.append(Attribute(dmrole='dataset:Curation.doi', dmtype='ivoa:string', value=''))
    inst.append(Attribute(dmrole='dataset:Curation.bibcode', dmtype='ivoa:string', value='2021arXiv210804778P'))

    # create 2D DatasetDM instance
    dset = Instance(dmtype='dataset:Dataset')
    collection.append(dset) 

    dset.append(Attribute(dmrole='dataset:productType', dmtype='ivoa:string', value='CATALOGUE'))
    dset.append(Attribute(dmrole='dataset:productSubType', dmtype='ivoa:string', value='General Comp.'))

    inst = Instance(dmrole='dataset:Dataset.dataID', dmtype='dataset:DataID')
    inst.append(Attribute(dmrole='dataset:DataID.datasetDID', dmtype='ivoa:string', value='ivo://CDS.VizieR/J/AJ/161/36'))
    inst.append(Attribute(dmrole='dataset:DataID.title', dmtype='ivoa:string', value='117 exoplanets in habitable zone with Kepler DR25'))
    inst.append(Attribute(dmrole='dataset:DataID.creationType', dmtype='ivoa:string', value='COPY_ORIGINAL'))
    inst.append(Attribute(dmrole='dataset:DataID.date', dmtype='ivoa:date', value='2021'))
    instcr = Instance(dmrole='dataset:DataID.creator', dmtype='Party')
    inst.append(instcr)
    instcr.append(Attribute(dmrole='dataset:Party.name', dmtype='ivoa:string', value='Bryson S.'))
    dset.append(inst)

    inst = Instance(dmrole='dataset:Dataset.curation', dmtype='dataset:Curation')
    dset.append(inst)
    inst.append(Attribute(dmrole='dataset:Curation.publisherDID', dmtype='ivoa:string', value='ivo://CDS'))
    inst.append(Attribute(dmrole='dataset:Curation.rights', dmtype='ivoa:string', value='https://cds.unistra.fr/vizier-org/licenses_vizier.html'))
    inst.append(Attribute(dmrole='dataset:Curation.releaseDate', dmtype='ivoa:date', value='2022-10-07T06:50:31Z'))
    instct = Instance(dmrole='dataset:Curation.contact', dmtype='party.Organisation')
    inst.append(instct)
    instct.append(Attribute(dmrole='party.Organisation.email', dmtype='ivoa:string', value='cds-question@unistra.fr'))
    inst.append(Attribute(dmrole='dataset:Curation.doi', dmtype='ivoa:string', value='10.26093/cds/vizier.51610036'))
    inst.append(Attribute(dmrole='dataset:Curation.bibcode', dmtype='ivoa:string', value='2021AJ....161...36B'))
    vodml.print()

