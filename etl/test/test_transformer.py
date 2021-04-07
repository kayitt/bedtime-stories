from unittest import TestCase
from unittest.mock import Mock
import pandas as pd
from etl.src.extractor import TimeSeriesExtractor


class Builder:
    def __init__(self):
        self.current_temperature = None


class CurrentTemperatureTransformer:
    def __init__(self, extractor: TimeSeriesExtractor):
        self.extractor = extractor
        self.query = """SELECT LAST("value") FROM "autogen"."°C" WHERE ("entity_id" = 'weather_station_temperature') AND time >= now() - 22h"""

    def transform(self, builder: Builder):
        builder.current_temperature = 23
        self.extractor.extract(query=self.query)


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
