import pandas as pd


class Extractor:
    def __init__(self, connection):
        self.connection = connection

    def extract(self, query):
        index = pd.to_datetime([1615746795223, 1615747408794], unit="ms")
        data = pd.Series([502, 535], index=index)
        return data
