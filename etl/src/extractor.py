import pandas as pd


class HomeAPI:
    @staticmethod
    def query():
        result = {"some_key": "some_value"}
        return result


class Extractor:
    def __init__(self, home_api: HomeAPI):
        self.home_api = home_api

    def extract(self, query):
        result_dict = self.home_api.query()
        data = result_dict['results'][0]['series'][0]['values']
        time = [x[0] for x in data]
        value = [x[1] for x in data]
        return pd.Series(value, index=pd.to_datetime(time, unit="ms"))
