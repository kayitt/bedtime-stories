import unittest
from unittest import TestCase

from etl.src.extractor import HomeAPI, Extractor


class TestE2EExtractor(TestCase):
    def test_returns_time_series(self):
        query = """SELECT "value" FROM "autogen"."ppm" WHERE ("entity_id" = 'weather_station_co2') AND time >= now() - 1h"""
        extracted_data = Extractor(home_api=HomeAPI()).extract(query=query)

        self.assertIsNotNone(extracted_data.index.time)
