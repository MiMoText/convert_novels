from copy import copy, deepcopy

import lxml.etree as ET

from .base import HTMLBaseDialect

class Hub18CFrenchDialect(HTMLBaseDialect):
    '''Dialect for source documents from hub18thcfrench.'''

    def split_titlepage(self, html_source):
        '''Given the whole html tree, extract the content of the titlepage and the rest.'''
        div_1 = html_source.cssselect('.xml-div1')[0]
        # Create a (shallow) copy to prevent modification of the original
        # element tree.
        tp = copy(div_1)
        rest = ET.Element('div')

        # Remove all the regular chapter divs to get the titlepage content.
        ET.strip_elements(tp, 'div')

        chapters = html_source.cssselect('.xml-div2')
        for chapter in chapters:
            rest.append(chapter)
        
        return tp, rest