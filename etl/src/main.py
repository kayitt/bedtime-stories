import sys

sys.path.append(".")

from etl.src.transformer import (
    Director,
    CurrentTemperatureTransformer,
    TeaBoilsTransformer,
    WakeUpTimeTransformer,
    CompositeTransformer,
    OutsideTemperatureTransformer,
)
from etl.src.extractor import TimeSeriesExtractor, HomeAPI, Clock
from etl.src.sender import Sender, FirestoreSender
from google.cloud import firestore


def report():
    client = firestore.Client()

    extractor = TimeSeriesExtractor(HomeAPI(), day_start_hour=6, clock=Clock())

    current_temp = CurrentTemperatureTransformer(extractor)
    num_tea_boils = TeaBoilsTransformer(extractor)
    wake_up_time = WakeUpTimeTransformer(extractor)
    outside_temperature = OutsideTemperatureTransformer(extractor)

    composite = CompositeTransformer(
        [current_temp, num_tea_boils, wake_up_time, outside_temperature]
    )

    director = Director(composite)

    firestore_sender = FirestoreSender(client)

    Sender(firestore_sender).send(director.create_report())


if __name__ == "__main__":
    report()
