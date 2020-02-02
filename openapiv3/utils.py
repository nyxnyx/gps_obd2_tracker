from xml.etree import ElementTree
from json.decoder import JSONDecoder
import logging

def getJSON(xml_string):
    """
    Will return JSON tree only from OpenAPIv3 response.

    params: xml_string: OpenAPIv3 response XML string.
    """
    
    tree = ElementTree.fromstring(xml_string)
    return JSONDecoder().decode(tree.text)