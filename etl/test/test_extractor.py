from unittest import TestCase
from unittest.mock import Mock

from etl.src.extractor import TimeSeriesExtractor, HomeAPI
import pandas as pd
from pandas.testing import assert_series_equal


class TestExtractor(TestCase):
    def setUp(self):
        self.mock_api = Mock()
        self.mock_api.query.return_value = {
            "results": [
                {
                    "statement_id": 0,
                    "series": [
                        {
                            "name": "ppm",
                            "columns": ["time", "value"],
                            "values": [[1615746795223, 502], [1615747408794, 535]],
                        }
                    ],
                }
            ]
        }

    def test_accepts_connection(self):
        TimeSeriesExtractor(home_api=self.mock_api)

    def test_accepts_day_start_hour(self):
        TimeSeriesExtractor(home_api=self.mock_api, day_start_hour=6)

    def test_has_extract_accepts_query(self):
        TimeSeriesExtractor(home_api=self.mock_api).extract(query="query")

    def test_returns_time_series(self):
        index = pd.to_datetime([1615746795223, 1615747408794], unit="ms")
        data = pd.Series([502, 535], index=index)

        extracted_data = TimeSeriesExtractor(home_api=self.mock_api).extract(
            query="query"
        )
        assert_series_equal(data, extracted_data)

    def test_returns_different_data(self):
        index = pd.to_datetime([1617638207104, 1617641225353], unit="ms")
        data = pd.Series([872, 882], index=index)

        self.mock_api.query.return_value = {
            "results": [
                {
                    "statement_id": 0,
                    "series": [
                        {
                            "name": "ppm",
                            "columns": ["time", "value"],
                            "values": [[1617638207104, 872], [1617641225353, 882]],
                        }
                    ],
                }
            ]
        }

        extracted_data = TimeSeriesExtractor(home_api=self.mock_api).extract(
            query="another_query"
        )

        assert_series_equal(data, extracted_data)
