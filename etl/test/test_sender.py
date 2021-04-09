from unittest import TestCase
from unittest.mock import Mock
from etl.src.data_classes import Model
from etl.src.sender import Sender, UnableToLoadException


class TestSender(TestCase):
    def setUp(self):
        self.firestore_sender = Mock()

    def test_send_sends_model(self):
        Sender(self.firestore_sender).send(model=Model(current_temperature=21))

    def test_sender_exception_if_firestore_load_fails(self):
        self.firestore_sender.send.side_effect = UnableToLoadException

        with self.assertRaises(UnableToLoadException):
            Sender(self.firestore_sender).send(model=Model(current_temperature=21))

    def test_sender_sends_model_dictionary(self):
        self.firestore_sender = Mock()

        Sender(self.firestore_sender).send(model=Model(current_temperature=21))

        self.firestore_sender.send.assert_called_with(
            {"temperature_inside": {"current": 21}}
        )