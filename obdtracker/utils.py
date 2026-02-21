from xml.etree import ElementTree
from json.decoder import JSONDecoder
from typing import Dict, Any

def get_json(xml_string: str) -> Dict[str, Any]:
    """
    Will return JSON tree only from OpenAPIv3 response.
    The response is usually an XML document with JSON content in the root element's text.
    """
    tree = ElementTree.fromstring(xml_string)
    if tree.text is None:
        return {}
    return JSONDecoder().decode(tree.text)

# Legacy naming for compatibility
def getJSON(xml_string: str) -> Dict[str, Any]:
    return get_json(xml_string)