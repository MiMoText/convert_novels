from copy import copy, deepcopy
import re

import lxml.etree as ET

from .base import HTMLBaseDialect

class Hub18CFrenchDialect(HTMLBaseDialect):
    '''Dialect for source documents from hub18thcfrench.'''

    def build_chapter_xml(self, chapter_source):
        '''Generate chapter div with appropriate markup from HTML source.
        
        This expects a single div node as source. It replaces standard
        markup by its XML equivalent and also implements special treatment
        for chapter headings.
        '''
        # Remove existing class attr and add type attr.
        chapter_source.attrib.clear()
        chapter_source.set('type', 'chapter')

        # Check for chapter heading.
        fst = chapter_source.getchildren()[0]
        if fst.tag == 'b' and fst.get('class') == 'headword':
            fst_copy = copy(fst)
            xml = self._replace_headings(fst_copy)
            chapter_source.replace(fst, xml)

        # Replace all the HTML tags with corresponding TEI XML ones.
        self._replace(chapter_source)
        return chapter_source


    def build_front_xml(self, titlepage):
        '''Build a TEI XML front from a div element with all the needed content.'''
        titlepage.attrib.clear()

        # The Eltec schema prescribes that the linebreaks in our headings should be ignored
        # as mere superficial artifacts of the printed editions. That is why we can not
        # use the lb tags inside the wrapping hi tags which markup the text highlights.
        head = titlepage.find('b')
        head = self._replace_headings(head)
        
        front = ET.Element('front')
        tp = ET.SubElement(front, 'div', attrib={'type': 'titlepage'})
        tp.append(head)
        
        # Recursively replace HTML markup with appropriate XML (in place!).
        self._replace(front)

        return front


    def clean_up(self, text):
        '''Remove obsolete portions of the text before it gets parsed.
        
        In particular, for this dialect we need to remove page break markers.
        We also remove the footnotes markers, since the note's content is
        unfortunately not preserved in the HTML source.  
        '''
        text = super().clean_up(text)
        # Pattern to match page breaks
        pb_pattern = r'<span.*?class="xml-pb-image".*?</span>'
        text = re.sub(pb_pattern, '', text)
        # Pattern to match footnotes
        fn_pattern = r'<span.*?type="note".*?</span>'
        # Note the necessity of re.DOTALL to make the . match newlines as well.
        text = re.sub(fn_pattern, '', text, flags=re.DOTALL)
        # Pattern to match centered text
        cnt_pattern = r'<span class="xml-center">(.*?)</span>'
        text = re.sub(cnt_pattern, '\g<1>', text, flags=re.DOTALL)

        return text


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

    
    def _replace_headings(self, source):
        '''Generate eltec-x compatible headings.
        
        The Eltec schema prescribes that the linebreaks in our headings should be ignored
        as mere superficial artifacts of the printed editions. That is why we can not
        use the lb tags inside the wrapping hi tags which markup the text highlights. 
        '''
        #text = ''.join([ET.tostring(el, encoding='unicode') for el in source.getchildren()])
        text = ET.tostring(source, encoding='unicode')
        lines = text.split('<span class="xml-lb"/>')
        concat = ' '.join([f'{l.strip()}' for l in lines])
        xml = f'<h1>{concat}</h1>'
        html = ET.fromstring(xml, parser=ET.HTMLParser())
        head = html.find('.//h1')
        return head
    

    def _log(self, source):
        print()
        print(ET.tostring(source, encoding="unicode"))
        print()