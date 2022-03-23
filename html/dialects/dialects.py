from enum import Enum

from .base import HTMLBaseDialect
from .hub18cfrench import Hub18CFrenchDialect


class HTMLDialects(Enum):
    HTMLBASE = HTMLBaseDialect
    HUB18CFRENCH = Hub18CFrenchDialect
