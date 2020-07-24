import ascii85
import base64
import unittest

class TestASCII85(unittest.TestCase):

    def setUp(self):
        self.phrases_to_encode = [
            "Hello",
            "How are you?",
            "I'm fine"
        ]

        self.phrases_to_decode = [
            "<~87cURDZ~>",
            "<~88i\p@<,p%H#Igi~>",
            "<~8LJ?tAnc-o~>"
        ]

    def test_encode(self):
        for phrase in self.phrases_to_encode:
            phrase = phrase.encode("utf-8")

            actual = ascii85.encode(phrase)
            expected = base64.a85encode(phrase, adobe = True)

            self.assertEqual(actual, expected)

    def test_decode(self):
        for phrase in self.phrases_to_decode:
            phrase = phrase.encode("utf-8")

            actual = ascii85.decode(phrase)
            expected = base64.a85decode(phrase, adobe = True)

            self.assertEqual(actual, expected)
