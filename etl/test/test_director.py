from unittest import TestCase
from etl.src.data_classes import Model


class Director:
    def create_report(self):
        return Model(current_temperature=21)


class TestCurrentTemperatureTransformer(TestCase):
    def test_director_exists(self):
        Director()

    def test_can_direct(self):
        Director().create_report()

    def test_returns_model_with_current_temperature(self):
        model = Director().create_report()

        self.assertIsNotNone(model.current_temperature)
