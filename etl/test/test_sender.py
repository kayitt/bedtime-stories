from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from etl.src.data_classes import Model
from google.cloud.firestore_v1.client import Client


class FirestoreSender:
    def __init__(self, client):
        self.client = client

    def send(self, document, key):
        self.client.collection(u"home").document(key).set(document)


class Sender:
    def __init__(self, sender: FirestoreSender):
        self.sender = sender

    def send(self, model: Model):
        document = {"some": "data"}
        key = datetime.now().strftime("%Y-%m-%d")
        try:
            self.sender.send(document, key)
        except:
            raise UnableToLoadException


class UnableToLoadException(Exception):
    """Raised when upload to Firestore fails"""

    pass


class TestSender(TestCase):
    def setUp(self):
        self.firestore_sender = Mock()

    def test_send_sends_model(self):
        Sender(self.firestore_sender).send(model=Model(current_temperature=21))

    def test_sender_exception_if_firestore_load_fails(self):
        self.firestore_sender.send.side_effect = UnableToLoadException

        with self.assertRaises(UnableToLoadException):
            Sender(self.firestore_sender).send(model=Model(current_temperature=21))
