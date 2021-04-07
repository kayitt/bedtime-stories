from etl.src.data_classes import Model
from etl.src.extractor import TimeSeriesExtractor


class Builder:
    def __init__(self):
        self.current_temperature = None


class CurrentTemperatureTransformer:
    def __init__(self, extractor: TimeSeriesExtractor):
        self.extractor = extractor
        self.query = """SELECT LAST("value") FROM "autogen"."°C" WHERE ("entity_id" = 'weather_station_temperature') AND time >= now() - 22h"""

    def transform(self, builder: Builder):
        time_series = self.extractor.extract(query=self.query)
        builder.current_temperature = time_series.last(offset="ms").values[0]


class Transformer:
    def __init__(self, transformers):
        self.transformers = transformers

    def create_report(self):
        return Model(current_temperature=21)
