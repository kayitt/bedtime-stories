import pandas as pd
import requests
import json
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


class Clock:
    @staticmethod
    def now():
        return datetime.now(tz=ZoneInfo("Europe/Berlin"))


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
    def __init__(self, home_api: HomeAPI, day_start_hour: int, clock: Clock):
        self.home_api = home_api
        self.day_start_hour = day_start_hour
        self.clock = clock

    def extract(self, query: str) -> pd.Series:
        result_dict = self.home_api.query(query=query)
        data = result_dict["results"][0]["series"][0]["values"]
        ts_threshold = self._to_milliseconds(self._last_6am(self.clock.now()))
        data_today = [x for x in data if x[0] > ts_threshold]

        return pd.Series(
            [x[1] for x in data_today],
            index=pd.to_datetime([x[0] for x in data_today], unit="ms"),
        )

    def _last_6am(self, ts: datetime) -> datetime:
        if ts.hour >= self.day_start_hour:
            return datetime(
                ts.year, ts.month, ts.day, hour=self.day_start_hour, tzinfo=ts.tzinfo
            )
        else:
            return datetime(
                ts.year, ts.month, ts.day, hour=self.day_start_hour, tzinfo=ts.tzinfo
            ) - timedelta(days=1)

    @staticmethod
    def _to_milliseconds(ts: datetime) -> int:
        return int(ts.timestamp() * 1000)
