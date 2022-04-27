from .base import EpubBaseDialect


class WikisourceEpubDialect(EpubBaseDialect):
    '''Epub dialect for documents from Wikisource.
    
    Epubs from Wikisource have been the reference implementation,
    so for the moment we can re-use the base dialect without further
    modifications.
    '''