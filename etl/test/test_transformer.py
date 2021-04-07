from unittest import TestCase


class CurrentTemperatureTransformer(object):
    def transform(self, builder):
        pass


class TestCurrentTemperatureTransformer(TestCase):
    def test_exists(self):
        CurrentTemperatureTransformer()

    def test_has_transform_accepts_builder(self):
        CurrentTemperatureTransformer().transform(builder="builder")
