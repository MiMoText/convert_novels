from unittest import TestCase

from dialects.html.base import HTMLBaseDialect


class HTMLBaseDialectTests(TestCase):

    def setUp(self) -> None:
        self.d = HTMLBaseDialect()
