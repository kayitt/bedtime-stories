from unittest import TestCase
import unittest
from etl.src.extractor import Extractor
import pandas as pd
from pandas.testing import assert_series_equal


class HomeAPI(object):
    pass


class TestExtractor(TestCase):

    def test_accepts_connection(self):
        Extractor(connection="connection")

    def test_has_extract_accepts_query(self):
        Extractor(connection="connection").extract(query="query")

    def test_returns_time_series(self):
        index = pd.to_datetime([1615746795223, 1615747408794], unit="ms")
        data = pd.Series([502, 535], index=index)

        extracted_data = Extractor(connection="connection").extract(query="query")

        assert_series_equal(data, extracted_data)

    @unittest.skip
    def test_returns_different_data(self):
        index = pd.to_datetime([1615746795223, 1615747408794], unit="ms")
        data = pd.Series([901, 865], index=index)

        extracted_data = Extractor(connection="connection").extract(query="another_query")

        assert_series_equal(data, extracted_data)
        
    def test_extractor_accepts_api(self):
        Extractor(connection=HomeAPI()).extract(query="another_query")
        
        



