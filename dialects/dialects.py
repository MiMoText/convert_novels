from enum import Enum

from .epubs.base import EpubBaseDialect
from .epubs.rousseau import RousseauEpubDialect
from .epubs.wikisource import WikisourceEpubDialect
from .epubs.wikisource_no_chapters import WikisourceNCEpubDialect
from .html.base import HTMLBaseDialect
from .html.hub18cfrench import Hub18CFrenchDialectA
from .html.hub18cfrench import Hub18CFrenchDialectB
from .html.hub18cfrench import Hub18CFrenchDialectC


class SourceDialects(Enum):
    EPUBBASE = EpubBaseDialect
    ROUSSEAU = RousseauEpubDialect
    WIKISOURCE = WikisourceEpubDialect
    WIKISOURCE_NC = WikisourceNCEpubDialect
    HTMLBASE = HTMLBaseDialect
    HUB18CFRENCH_A = Hub18CFrenchDialectA
    HUB18CFRENCH_B = Hub18CFrenchDialectB
    HUB18CFRENCH_C = Hub18CFrenchDialectC