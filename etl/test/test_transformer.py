from unittest import TestCase


class Transformer(object):
    pass


class TestTransformer(TestCase):
    def test_exists(self):
        Transformer()
