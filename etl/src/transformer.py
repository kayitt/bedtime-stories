from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

import pandas as pd
from etl.src.extractor import TimeSeriesExtractor
from etl.src.data_classes import Model
from abc import ABC, abstractmethod


class Builder:
    def __init__(self):
        self.current_temperature = None
        self.num_tea_boils = None
        self.wake_up_time = None
        self.outside_temperature = None

    def build(self) -> Model:
        return Model(
            current_temperature=self.current_temperature,
            num_tea_boils=self.num_tea_boils,
            wake_up_time=self.wake_up_time,
            outside_temperature=self.outside_temperature,
        )

    def __eq__(self, other):
        return (
            (self.current_temperature == other.current_temperature)
            & (self.num_tea_boils == other.num_tea_boils)
            & (self.wake_up_time == other.wake_up_time)
            & (self.outside_temperature == other.outside_temperature)
        )


class Transformer(ABC):
    @abstractmethod
    def transform(self, builder: Builder) -> None:
        pass


class CurrentTemperatureTransformer(Transformer):
    def __init__(self, extractor: TimeSeriesExtractor):
        self.extractor = extractor
        self.query = """SELECT LAST("value") FROM "autogen"."°C" WHERE ("entity_id" = 'weather_station_temperature') AND time >= now() - 24h"""

    def transform(self, builder: Builder) -> None:
        time_series = self.extractor.extract(query=self.query)
        builder.current_temperature = float(time_series.last(offset="ms").values[0])


class CompositeTransformer(Transformer):
    def __init__(self, transformers: List[Transformer]):
        self.transformers = transformers

    def transform(self, builder: Builder) -> None:
        for transformer in self.transformers:
            transformer.transform(builder)


class Director:
    def __init__(self, transformer: Transformer):
        self.transformer = transformer

    def create_report(self) -> Model:
        builder = Builder()
        self.transformer.transform(builder)
        return builder.build()


class TeaBoilsTransformer:
    def __init__(self, extractor: TimeSeriesExtractor):
        self.extractor = extractor
        self.query = """SELECT MAX("value") FROM "W" WHERE ("entity_id" = 'plug_current_consumption_3') AND time >= now() - 24h GROUP BY time(5m) fill(0)"""

    def transform(self, builder: Builder) -> None:
        tz = ZoneInfo("Europe/Berlin")
        ts_0 = datetime(2021, 1, 1)
        series = self.extractor.extract(query=self.query)
        print("series")
        print(series)
        series = pd.concat([pd.Series([0], index=[ts_0]), series])

        series = series.sort_index().apply(lambda x: 1 if x > 0 else 0)
        builder.num_tea_boils = sum(series.diff() > 0)


class WakeUpTimeTransformer:
    def __init__(self, extractor):
        self.extractor = extractor
        self.wake_up_query = """SELECT movement FROM (SELECT count("value") AS movement FROM "state" WHERE ("entity_id" = 'hue_motion_sensor_entrance_motion') AND time >= now() - 24h GROUP BY time(1m) ) WHERE movement > 0"""

    def transform(self, builder: Builder) -> None:
        series = self.extractor.extract(query=self.wake_up_query)
        builder.wake_up_time = series.index.min()


class OutsideTemperatureTransformer:
    def __init__(self, extractor):
        self.extractor = extractor
        self.outside_temperature_query = """SELECT "value" FROM "autogen"."°C" WHERE ("entity_id" = 'outdoor_module_temperature') AND time >= now() - 24h"""

    def transform(self, builder: Builder) -> None:
        series = self.extractor.extract(query=self.outside_temperature_query)
        builder.outside_temperature = self._outside_temperature(series)

    @staticmethod
    def _outside_temperature(s: pd.Series) -> dict:
        min_temp = s.min()
        min_ts = s[s == min_temp].index[0]
        max_temp = s.max()
        max_ts = s[s == max_temp].index[0]
        return {
            "min": {
                "ts": min_ts,
                "value": float(min_temp),
            },
            "max": {
                "ts": max_ts,
                "value": float(max_temp),
            },
        }
