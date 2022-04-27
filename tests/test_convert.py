'''
Tests concerning the main `epubs.py` file. 
'''

from unittest import TestCase

from dialects.dialects import SourceDialects
from convert import determine_dialect


class HTMLDialectTest(TestCase):
    '''HTML dialect detection tests.'''

    def test_detect_hub18cfrench(self):
        '''Ensure that HTML sources from hub18cfrench are detected.'''
        text = '''<div class="xml-div1">
            <p>some content</p>
        </div>'''
        expected = SourceDialects['HUB18CFRENCH'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)

    def test_enforce_dialect(self):
        '''When enforcing usage of a dialect, make sure it is actually used.'''
        text = 'irrelevant dummy test text'
        ds = (
            ('HUB18CFRENCH', SourceDialects['HUB18CFRENCH'].value),
        )
        for forced, expected in ds:
            results = determine_dialect(text, forced)
            self.assertIsInstance(results, expected)


class EpubDialectTest(TestCase):
    '''Epub dialect detection tests.'''

    def test_detect_rousseauonline(self):
        '''Ensure sources from rousseauonline.ch are detected correctly.'''
        text = '''
## Jean-Jacques Rousseau  
Collection complète des oeuvres

#### 17 vol., in-4º, Genève, 1780-1789  
www.rousseauonline.ch

JEAN JACQUES ROUSSEAU

## LA REINE FANTASQUE, CONTE

Il y avoit autrefois un Roi qui aimoit son peuple...
        '''
        expected = SourceDialects['ROUSSEAU'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)
    

    def test_detect_wikisource_with_chapters(self):
        '''Ensure sources from wikisource are detected correctly.'''
        text = '''
## Les Lettres d'Amabed

### Voltaire

##### Garnier, Paris, 1877

###### Exporté de Wikisource le 11 novembre 2021

LES LETTRES D'AMABED

### PREMIÈRE LETTRE  

D'AMABED À SHASTASID, GRAND BRAME DE MADURÉ.
'''
        expected = SourceDialects['WIKISOURCE'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)
    

    def test_detect_wikisource_without_chapters(self):
        '''Ensure sources from wikisource without chapters are detected correctly.'''
        text = '''
## La Petite Maison \(version de 1763\)

### Jean-François de Bastide

##### Librairie des Bibliophiles, Paris, 1879

###### Exporté de Wikisource le 11 janvier 2022

## **LA PETITE MAISON**

Cette maison unique est sur les bords de la Seine. Une avenue, conduisant à une patte d’oie,
'''
        expected = SourceDialects['WIKISOURCE_NC'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)
    
    
    def test_enforce_dialect(self):
        '''When enforcing usage of a dialect, make sure it is actually used.'''
        text = 'test'
        ds = (
            ('WIKISOURCE', SourceDialects['WIKISOURCE'].value),
            ('WIKISOURCE_NC', SourceDialects['WIKISOURCE_NC'].value),
            ('ROUSSEAU', SourceDialects['ROUSSEAU'].value),
        )
        for forced, expected in ds:
            results = determine_dialect(text, forced)
            self.assertIsInstance(results, expected)
