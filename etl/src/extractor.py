import pandas as pd
import requests
import json


class HomeAPI:
    def __init__(self):
        self.url = (
            "http://user:user@192.168.178.94:8080/api/hassio_ingress"
            "/uRmXKLfm0vxpbj_90ivhuGFWRFbJb3bVcVO91AaAwwA/api/datasources/proxy/1/query"
        )
        self.params = {"db": "homeassistant", "epoch": "ms"}

    def query(self, query):
        self.params["q"] = query
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic dXNlcjp1c2Vy",
        }
        response = requests.request(
            "GET", self.url, headers=headers, params=self.params
        )
        return json.loads(response.content)


class TimeSeriesExtractor:
    def __init__(self, home_api: HomeAPI):
        self.home_api = home_api

    def extract(self, query):
        result_dict = self.home_api.query(query=query)
        data = result_dict["results"][0]["series"][0]["values"]
        time = [x[0] for x in data]
        value = [x[1] for x in data]
        return pd.Series(value, index=pd.to_datetime(time, unit="ms"))
