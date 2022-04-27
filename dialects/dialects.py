from enum import Enum

from .epubs.base import EpubBaseDialect
from .epubs.rousseau import RousseauEpubDialect
from .epubs.wikisource import WikisourceEpubDialect
from .epubs.wikisource_no_chapters import WikisourceNCEpubDialect
from .html.base import HTMLBaseDialect
from .html.hub18cfrench import Hub18CFrenchDialect


class SourceDialects(Enum):
    EPUBBASE = EpubBaseDialect
    ROUSSEAU = RousseauEpubDialect
    WIKISOURCE = WikisourceEpubDialect
    WIKISOURCE_NC = WikisourceNCEpubDialect
    HTMLBASE = HTMLBaseDialect
    HUB18CFRENCH = Hub18CFrenchDialect
