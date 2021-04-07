from typing import List
from etl.src.extractor import TimeSeriesExtractor
from etl.src.data_classes import Model
from abc import ABC, abstractmethod


class Builder:
    def __init__(self):
        self.current_temperature = None

    def build(self):
        return Model(current_temperature=self.current_temperature)


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
        builder.current_temperature = time_series.last(offset="ms").values[0]


class MainTransformer:
    def __init__(self, transformers: List[Transformer]):
        self.transformers = transformers

    def create_report(self, builder: Builder):
        for transformer in self.transformers:
            transformer.transform(builder)
        model = builder.build()
        return model
