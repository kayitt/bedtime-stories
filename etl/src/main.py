from etl.src.transformer import Director, CurrentTemperatureTransformer
from etl.src.extractor import TimeSeriesExtractor, HomeAPI
from etl.src.sender import Sender, FirestoreSender
from google.cloud import firestore


def report():
    client = firestore.Client()

    director = Director(CurrentTemperatureTransformer(TimeSeriesExtractor(HomeAPI())))
    firestore_sender = FirestoreSender(client)
    Sender(firestore_sender).send(director.create_report())


if __name__ == "__main__":
    report()
