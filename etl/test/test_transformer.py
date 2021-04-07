from unittest import TestCase
from unittest.mock import Mock
import pandas as pd
from etl.src.compositetransformer import (
    Builder,
    CurrentTemperatureTransformer,
    CompositeTransformer,
    Transformer,
    Director,
)
from etl.src.data_classes import Model


class StubTransformer(Transformer):
    def transform(self, builder: Builder):
        builder.current_temperature = 21


class TestCurrentTemperatureTransformer(TestCase):
    def setUp(self):
        self.current_temperature_query = """SELECT LAST("value") FROM "autogen"."°C" WHERE ("entity_id" = 'weather_station_temperature') AND time >= now() - 22h"""

        self.extractor = Mock()
        index = pd.to_datetime([17, 15], unit="ms")
        self.extractor.extract.return_value = pd.Series([23, 21], index=index)

    def test_transformed_builder_has_current_temperature(self):
        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.assertIsNotNone(builder.current_temperature)

    def test_accepts_extractor(self):
        CurrentTemperatureTransformer(self.extractor)

    def test_extract_called_with_current_temperature_query(self):
        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.extractor.extract.assert_called_with(query=self.current_temperature_query)

    def test_builder_none_temperature_before_transformation(self):
        builder = Builder()

        self.assertIsNone(builder.current_temperature)

    def test_current_temperature_is_latest_value(self):
        index = pd.to_datetime([17, 15], unit="ms")
        self.extractor.extract.return_value = pd.Series([23, 21], index=index)

        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.assertEqual(23, builder.current_temperature)

    def test_current_temperature_is_latest_value_another(self):
        index = pd.to_datetime([4, 9], unit="ms")
        self.extractor.extract.return_value = pd.Series([23, 21], index=index)

        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.assertEqual(21, builder.current_temperature)


class TestCompositeTransformer(TestCase):
    def setUp(self):
        self.current_temp_mock = Mock()
        self.transformer = CompositeTransformer(transformers=[self.current_temp_mock])

    def test_can_create_report(self):
        self.transformer.transform(Builder())

    def test_create_report_runs_current_temperature_transform(self):
        self.transformer.transform(Builder())

        self.current_temp_mock.transform.assert_called()


class TestDirector(TestCase):
    def test_has_create_report_accepts_transformer(self):
        mock_transformer = Mock()
        Director(mock_transformer).create_report()

        mock_transformer.transform.assert_called_with(Builder())

    def test_create_report_creates_model(self):
        expected_model = Model(current_temperature=21)

        model = Director(StubTransformer()).create_report()

        self.assertEqual(expected_model, model)
