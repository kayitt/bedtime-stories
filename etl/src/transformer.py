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
            # outside_temperature=self.outside_temperature
        )

    # todo: equality
    def __eq__(self, other):
        return self.current_temperature == other.current_temperature


class Transformer(ABC):
    @abstractmethod
    def transform(self, builder: Builder):
        pass


class CurrentTemperatureTransformer(Transformer):
    def __init__(self, extractor: TimeSeriesExtractor):
        self.extractor = extractor
        self.query = """SELECT LAST("value") FROM "autogen"."°C" WHERE ("entity_id" = 'weather_station_temperature') AND time >= now() - 22h"""

    def transform(self, builder: Builder):
        time_series = self.extractor.extract(query=self.query)
        builder.current_temperature = float(time_series.last(offset="ms").values[0])


class CompositeTransformer(Transformer):
    def __init__(self, transformers: List[Transformer]):
        self.transformers = transformers

    def transform(self, builder: Builder):
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
        self.query = """SELECT MAX("value") FROM "W" WHERE ("entity_id" = 'plug_current_consumption_3') AND time >= now() - 21h GROUP BY time(5m) fill(0)"""

    def transform(self, builder: Builder):
        series = self.extractor.extract(query=self.query)
        builder.num_tea_boils = sum(series > 0)


class WakeUpTimeTransformer:
    def __init__(self, extractor):
        self.extractor = extractor
        self.wake_up_query = """SELECT movement FROM (SELECT count("value") AS movement FROM "state" WHERE ("entity_id" = 'hue_motion_sensor_entrance_motion') AND time >= now() - 21h GROUP BY time(1m) ) WHERE movement > 0"""

    def transform(self, builder: Builder):
        series = self.extractor.extract(query=self.wake_up_query)
        builder.wake_up_time = self._series_to_ts(series)

    @staticmethod
    def _series_to_ts(series: pd.Series):
        min_ts = series.index.min()
        min_ts = min_ts.tz_localize("Europe/Berlin")
        return min_ts.astimezone(ZoneInfo("UTC"))
