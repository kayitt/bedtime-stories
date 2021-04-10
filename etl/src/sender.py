from datetime import datetime
from google.cloud.firestore_v1 import Client
from pandas import Timestamp

from etl.src.data_classes import Model


class FirestoreSender:
    def __init__(self, client: Client):
        self.client = client

    def send(self, data: dict):
        date = datetime.now().strftime("%Y-%m-%d")
        self.client.collection(u"home").document(date).set(data)


class Sender:
    def __init__(self, firestore_sender: FirestoreSender):
        self.firestore_sender = firestore_sender

    def send(self, model: Model):
        self.firestore_sender.send(
            {
                "temperature_inside": {"current": model.current_temperature},
                "num_tea_boils": model.num_tea_boils,
                "wake_up_time": model.wake_up_time,
                "temperature_outside": model.outside_temperature,
            }
        )


class UnableToLoadException(Exception):
    """Raised when upload to Firestore fails"""

    pass
