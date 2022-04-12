from unittest import TestCase, skip

import lxml.etree as ET

from html.dialects.hub18cfrench import Hub18CFrenchDialect


class Hub18CFrenchDialectTests(TestCase):

    def setUp(self) -> None:
        self.d = Hub18CFrenchDialect()


    def test_build_chapter_xml(self):
        '''Ensure that build_chapter_xml() correctly replaces chapter headings.'''
        text = '''<div class="xml-div2">
<b class="headword">CHAPITRE VI.<span class="xml-lb"></span>
<i>Réparation des torts</i>.</b>
<p>Text</p></div>'''
        html = ET.fromstring(text)
        results = self.d.build_chapter_xml(html)
        results = ET.tostring(results, encoding='unicode').replace('\n', '')
        expected = ''.join([
            '<div type="chapter">',
            '<head><hi rend="bold">CHAPITRE VI. ',
            '<hi rend="italic">Réparation des torts</hi>.',
            '</hi></head>',
            '<p>Text</p>',
            '</div>'])
        self.assertEqual(results, expected)


    def test_clean_up_page_breaks(self):
        '''Ensure that page break markers get removed.'''
        text = '<p>some text<span id="bbl_41_00_3478_0435_k" n="32" class="xml-pb-image">--32--</span> some more.</p>'
        results = self.d.clean_up(text)
        expected = '<p>some text some more.</p>'
        self.assertEqual(results, expected)


    def test_clean_up_footnotes(self):
        '''Ensure that footnotes are deleted, since their content is not available anyway.'''
        text = '''<p>some text<span type="note" target="n18" n="*"
data-ref="/scripts/get_notes.py?philo_id=517+2+1&amp;arg=&amp;sort_order=rowid&amp;target=n18"
id="n18-link-back" class="note-ref" tabindex="0" data-toggle="popover" data-container="body"
data-placement="right" data-trigger="focus" data-html="true" data-animation="true">*</span> more text.</p>'''
        results = self.d.clean_up(text)
        expected = '<p>some text more text.</p>'
        self.assertEqual(results, expected)
    

    def test_clean_up_centered(self):
        '''Ensure that centered text is kept without special markup.'''
        text = '<p><span class="xml-center">Text</span></p>'
        results = self.d.clean_up(text)
        expected = '<p>Text</p>'
        self.assertEqual(results, expected)


    def test_replace_headings(self):
        '''Ensure that eltec-x compatible headings are generated.'''
        text = '<b class="headword">dummy<span class="xml-lb"/>title</b>'
        html = ET.fromstring(text)
        results = self.d._replace_headings(html)
        results = ET.tostring(results, encoding='unicode')
        expected = '<h1><b class="headword">dummy title</b></h1>'
        self.assertEqual(results, expected)


    def test_build_front_xml(self):
        text = '''<div><b class="headword">HISTOIRE<span class="xml-lb"></span>
        DE<span class="xml-lb"/>
        ROBERT LE DIABLE;<span class="xml-lb"/>
        DUC DE NORMANDIE.</b></div>
        '''
        html = ET.fromstring(text)
        results = self.d.build_front_xml(html)
        results = ET.tostring(results, encoding="unicode")
        expected = '<front><div type="titlepage"><head><hi rend="bold">HISTOIRE DE ROBERT LE DIABLE; DUC DE NORMANDIE.</hi></head></div></front>'
        self.assertEqual(results, expected)