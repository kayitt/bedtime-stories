from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from zoneinfo import ZoneInfo

from etl.src.extractor import TimeSeriesExtractor, Clock
import pandas as pd
from pandas.testing import assert_series_equal


def to_milliseconds(ts: datetime):
    return ts.timestamp() * 1000


class TestExtractor(TestCase):
    def setUp(self):
        self.mock_api = Mock()
        tz = ZoneInfo("Europe/Berlin")
        ts_1 = datetime(2021, 4, 11, hour=5, tzinfo=tz)
        ts_2 = datetime(2021, 4, 11, hour=10, tzinfo=tz)
        ts_3 = datetime(2021, 4, 11, hour=22, tzinfo=tz)
        self.ts_1 = to_milliseconds(ts_1)
        self.ts_2 = to_milliseconds(ts_2)
        self.ts_3 = to_milliseconds(ts_3)
        self.mock_api.query.return_value = {
            "results": [
                {
                    "statement_id": 0,
                    "series": [
                        {
                            "name": "ppm",
                            "columns": ["time", "value"],
                            "values": [
                                [self.ts_1, 500],
                                [self.ts_2, 502],
                                [self.ts_3, 535],
                            ],
                        }
                    ],
                }
            ]
        }
        clock = Mock()
        clock.now.return_value = datetime(2021, 4, 11, hour=23, tzinfo=tz)
        self.extractor = TimeSeriesExtractor(
            home_api=self.mock_api, day_start_hour=6, clock=clock
        )

    def test_has_extract_accepts_query(self):
        self.extractor.extract(query="query")

    def test_returns_time_series(self):
        index = pd.to_datetime([self.ts_2, self.ts_3], unit="ms").tz_localize("UTC")
        data = pd.Series([502, 535], index=index)

        extracted_data = self.extractor.extract(query="query")
        assert_series_equal(data, extracted_data)

    def test_returns_different_data(self):
        index = pd.to_datetime([self.ts_2, self.ts_3], unit="ms").tz_localize("UTC")
        data = pd.Series([872, 882], index=index)

        self.mock_api.query.return_value = {
            "results": [
                {
                    "statement_id": 0,
                    "series": [
                        {
                            "name": "ppm",
                            "columns": ["time", "value"],
                            "values": [
                                [self.ts_1, 800],
                                [self.ts_2, 872],
                                [self.ts_3, 882],
                            ],
                        }
                    ],
                }
            ]
        }

        extracted_data = self.extractor.extract(query="another_query")

        assert_series_equal(data, extracted_data)


class TestClock(TestCase):
    def test_clock_has_now(self):
        Clock().now()

    def test_now_returns_timestamp(self):
        ts = Clock().now()
        self.assertIsNotNone(ts.astimezone(ZoneInfo("UTC")))
