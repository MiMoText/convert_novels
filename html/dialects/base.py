from copy import copy
from io import StringIO
import logging

import lxml.etree as ET
from lxml.etree import HTMLParser

from common.aux_file import remove_suffix
from common.xml_header import build_header_xml


class HTMLBaseDialect:
    '''Base functionality for dialects of HTML sources.
    
    Inherit from this and overwrite some of its methods to create
    your own dialects.
    '''

    NAMESPACES = {
        'tei': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace',
    }

    def transform(self, text, filename):
        '''Convert an HTML file to TEI XML.
        
        This should be the only method that gets called from the outside.
        To modify the transformation process, do not modify this method.
        Instead, create a new HTML dialect by subclassing this class and
        by overriding one or more of its other methods which get called
        by this method and which do the actual work. 
        '''
        # Perform some kind of preprocessing on the raw string.
        text = self.clean_up(text)
        html = ET.parse(StringIO(text), HTMLParser())
        html = html.getroot()
        
        name = remove_suffix(filename, '.html')
        xml = self.build_header_xml(file_name=name)
        tei = xml.getroot()

        # Split the source document into its components.
        try:
            tp, rest = self.split_titlepage(html)
            chapters = self.split_chapters(rest)
        except IndexError as e:
            front = None
            msg = f'Source file "{filename}" has unexpected structure, conversion will likely fail!'
            logging.warning(msg)
        

        # Create the various parts of the text node.
        front = self.build_front_xml(tp)
        chapters = [self.build_chapter_xml(c) for c in chapters]
        body = self.build_body_xml(chapters)
        back = self.build_back_xml()

        # Put all the pieces together.
        text_node = ET.Element('text')
        if front is not None:
            text_node.append(front)
        text_node.append(body)
        text_node.append(back)

        tei.append(text_node)
        tree = ET.ElementTree(tei)
        return tree

    # ********************************************************************************
    # Overwrite the following methods in your custom dialect.
    # ********************************************************************************
    
    def build_back_xml(self, footnotes={}):
        '''Create back section.

        Normally, this would contain previously collected notes as endnotes.
        But since our current HTML sources do not contain any, we just append
        an empty back.
        '''
        nsmap = self.__class__.NAMESPACES
        back = ET.Element('back', nsmap=nsmap)

        if footnotes != {}:
            logging.warning('The current implementation does not create endnotes.')

        return back


    def build_body_xml(self, chapters_xml_list):
        '''Generate the body element of the TEI XML and optionally footnotes.
        
        Expects a list of chapter nodes which have already been converted
        with `build_chapter_xml()`. By default, it only wraps them inside
        a body element, and it does not collect any footnotes along the way.
        '''
        body = ET.Element('body')
        for chapter in chapters_xml_list:
            body.append(chapter)
        return body


    def build_chapter_xml(self, chapter_source):
        '''Generate chapter div with appropriate markup from HTML source.
        
        By default, this expects a single div node and only sets some attributes
        and replaces some standard markup to generate TEI XML.
        '''
        # Remove existing class attr and add type attr.
        chapter_source.attrib.clear()
        chapter_source.set('type', 'chapter')

        # Check for chapter heading.
        fst = chapter_source.getchildren()[0]
        if fst.tag == 'b' and fst.get('class') == 'headword':
            fst_copy = copy(fst)
            head = ET.Element('head')
            head.append(fst_copy)
            chapter_source.replace(fst, head)

        # Replace all the HTML tags with corresponding TEI XML ones.
        self._replace(chapter_source)
        return chapter_source


    def build_header_xml(self, root=None, metadata={}, file_name='TODO'):
        '''Create a TEI XML header section.
        
        It does not take any textual content from the actual document, so
        it can be generic across EPUB and HTML source documents.
        '''
        return build_header_xml(root, metadata, file_name)


    def build_front_xml(self, titlepage):
        '''Build a TEI XML front from a div element with all the needed content.'''
        titlepage.attrib.clear()
        titlepage.attrib['type'] = 'titlepage'

        # Recursively replace HTML markup with appropriate XML (in place!).
        self._replace(titlepage)

        front = ET.Element('front')
        front.append(titlepage)

        return front
    

    def clean_up(self, text):
        '''Perform preprocessing on the raw input string.
        
        This method does not take the HTML structure into deep consideration.
        It expects a string as input (which happens to be HTML) and returns
        a string as well. By default, this method returns the text unchanged.
        '''
        return text
    

    def split_chapters(self, html_source):
        '''Split tree into chapter nodes.
        
        By default, just return all direct child nodes of the given node.
        '''
        return html_source.getchildren()


    def split_titlepage(self, html_source):
        '''Given the whole html tree, extract the content of the titlepage and the rest.
        
        This is highly specific to the source file, so we do not provide a generic
        implementation. Instead each concrete dialect is expected to implement an
        appropriate `split_titlepage()` method.
        '''
        msg = 'The dialect in use has not provided a `split_titlepage()` method.'
        logging.error(msg)

    # **************************************************************************
    #  Helper functions which probably need no overwriting, but can be reused
    #  in subclasses.
    # **************************************************************************

    def _replace(self, node):
        '''Recursively replace certain HTML tags with appropriate XML tags.
        
        Please note that this method modifies the node in place. If this is not
        what you want, copy or deepcopy the node first.
        '''
        if node.tag == 'b':
            self._replace_bold(node)
        elif node.tag == 'i':
            self._replace_italics(node)
        elif node.tag == 'span' and node.attrib['class'] == 'small-caps':
            self._replace_small_caps(node)
        elif node.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._replace_h(node)
        elif node.tag == 'span' and node.attrib['class'] == 'xml-q':
            self._replace_q(node)
        
        for child in node.getchildren():
            self._replace(child)
        
        return node
    

    def _replace_bold(self, elem):
        '''Replace b tag with appropriate XML.'''
        elem.tag = 'hi'
        elem.attrib.clear()
        elem.set('rend', 'bold')
        return elem
    

    def _replace_h(self, elem):
        '''Replace h1, h2 etc with appropriate XML tags.'''
        elem.tag = 'head'
        elem.attrib.clear()
        return elem


    def _replace_q(self, elem):
        '''Replace span with class "xml-q" with q tags.
        
        Note that eltec-x does not allow that (TEI does), but I don't know what
        a proper alternative would be.
        '''
        parent = elem.getparent()
        elem_copy = copy(elem)
        elem_copy.tag = 'q'
        elem_copy.attrib.clear()
        parent.replace(elem, elem_copy)
        return elem


    def _replace_small_caps(self, elem):
        '''Replace span tag with small caps with appropriate XML.'''
        elem.tag = 'hi'
        elem.attrib.clear()
        elem.set('rend', 'caps')
        return elem


    def _replace_italics(self, elem):
        '''Replace i tag with appropriate XML.'''
        elem.tag = 'hi'
        elem.attrib.clear()
        elem.set('rend', 'italic')
