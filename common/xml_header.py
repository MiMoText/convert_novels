from datetime import date
from pathlib import Path

import lxml.etree as ET

NAMESPACES = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace',
}

def build_header_xml(root=None, metadata={}, file_name='TODO'):
    '''Create a generic TEI XML header.'''
    nsmap = NAMESPACES
    templ_path = Path(__file__).resolve()
    templ_path = templ_path.parent / 'templates' / 'teiHeader-Template.xml'
    parser = ET.XMLParser(remove_blank_text=True)
    xml = ET.parse(str(templ_path), parser)

    # Pre-fill some known values.
    today = date.today().isoformat()
    xml_id = file_name
    tei = xml.getroot()
    tei.attrib[ET.QName(nsmap.get('xml'), 'id')] = xml_id

    change_path = f"//{ET.QName(nsmap.get('tei'), 'revisionDesc')}/{ET.QName(nsmap.get('tei'), 'change')}"
    change = xml.find(change_path)
    change.attrib['when'] = today

    if metadata != {}:
        raise NotImplementedError('Auto-fill-in of metadata is not yet supported – sorry!')

    if root is not None:
        root.insert(0, xml)
        return root
    return xml