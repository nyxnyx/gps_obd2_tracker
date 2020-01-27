from xml.etree import ElementTree
from json.decoder import JSONDecoder
import logging

def getJSON(xml_string):
    tree = ElementTree.fromstring(xml_string)
    return JSONDecoder().decode(tree.text)