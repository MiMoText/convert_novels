from unittest import TestCase

from html.dialects.base import HTMLBaseDialect


class HTMLBaseDialectTests(TestCase):

    def setUp(self) -> None:
        self.d = HTMLBaseDialect()
