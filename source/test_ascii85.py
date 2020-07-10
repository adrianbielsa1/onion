import ascii85
import base64
import unittest

# NOTE: I use the standard module "base64" to test against my own implementation. Since "base64"
# works on "bytes" objects, while my implementation uses "str" (string) objects. Proper str.encode()
# calls have been added to circumvent this difference.

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
            actual      = ascii85.encode(phrase).encode("utf-8")
            expected    = base64.a85encode(phrase.encode("utf-8"), adobe = True)

            self.assertEqual(actual, expected)

    def test_decode(self):
        for phrase in self.phrases_to_decode:
            actual      = ascii85.decode(phrase).encode("utf-8")
            expected    = base64.a85decode(phrase.encode("utf-8"), adobe = True)

            self.assertEqual(actual, expected)
