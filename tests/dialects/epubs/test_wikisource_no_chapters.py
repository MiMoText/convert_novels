from unittest import TestCase

from dialects.epubs.wikisource_no_chapters import WikisourceNCEpubDialect 


class EpubWikisourceNCTest(TestCase):
    '''
    Test the modifications which are specific to sources from wikisource without chapters.
    '''

    def setUp(self):
        self.dialect = WikisourceNCEpubDialect()


    def test_split_titlepage(self):
        '''Ensure that the modified `split_titlepage()` works.
        
        Since the markup in this dialect is somewhat unpredictable, we simply split after the
        line "###### Exporté de Wikisource...". 
        '''
        text = '''
Stuff
###### Exporté de Wikisource le 15 mars 2022
Text
## Heading
More text'''
        titlepage, rest = self.dialect.split_titlepage(text)
        self.assertEqual(titlepage, '\nStuff\n###### Exporté de Wikisource le 15 mars 2022\n')
        self.assertEqual(rest, 'Text\n## Heading\nMore text\n')


    def test_split_titlepage_from_start(self):
        '''split_titlepage() needs to deal with the marker being at the start of the doc.'''
        text = '''###### Exporté de Wikisource le 15 mars 2022
Text
## Heading
More text'''
        titlepage, rest = self.dialect.split_titlepage(text)
        self.assertEqual(titlepage, '###### Exporté de Wikisource le 15 mars 2022\n')
        self.assertEqual(rest, 'Text\n## Heading\nMore text\n')