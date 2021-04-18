from datetime import datetime
from google.cloud.firestore_v1 import Client
from etl.src.data_classes import Model
from pandas._libs.tslibs.nattype import NaTType


class FirestoreSender:
    def __init__(self, client: Client):
        self.client = client

    def send(self, data: dict) -> None:
        date = datetime.now().strftime("%Y-%m-%d")
        self.client.collection(u"home").document(date).set(data)


class Sender:
    def __init__(self, firestore_sender: FirestoreSender):
        self.firestore_sender = firestore_sender

    def send(self, model: Model) -> None:
        data = {
            "temperature_inside": {"current": model.current_temperature},
            "num_tea_boils": model.num_tea_boils,
            "temperature_outside": model.outside_temperature,
        }
        if type(model.wake_up_time) != NaTType:
            data.update({"wake_up_time": model.wake_up_time})

        self.firestore_sender.send(data)


class UnableToLoadException(Exception):
    """Raised when upload to Firestore fails"""

    pass
