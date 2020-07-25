import bitwise
import unittest

class TestBitwise(unittest.TestCase):

    def setUp(self):
        self.ordinals_to_encode = {
            int("00000000", 2) : int("01010101", 2),
            int("11111111", 2) : int("10101010", 2),
            int("10101010", 2) : int("00000000", 2),
            int("01010101", 2) : int("11111111", 2)
        }

        self.ordinals_to_decode = {
            int("01010101", 2) : int("00000000", 2),
            int("10101010", 2) : int("11111111", 2),
            int("00000000", 2) : int("10101010", 2),
            int("11111111", 2) : int("01010101", 2)
        }

    def test_encode(self):
        for actual, expected in self.ordinals_to_encode.items():
            # NOTE: "int" objects must be converted to "List" objects before converting
            # them to "bytearray" objects; otherwise, a "bytearray" is created with the
            # size of the integer, filled with zeros.
            actual = bytearray([actual])
            expected = bytearray([expected])

            actual = bitwise.encode(actual)

            self.assertEqual(actual, expected)

    def test_decode(self):
        for actual, expected in self.ordinals_to_decode.items():
            # NOTE: "int" objects must be converted to "List" objects before converting
            # them to "bytearray" objects; otherwise, a "bytearray" is created with the
            # size of the integer, filled with zeros.
            actual = bytearray([actual])
            expected = bytearray([expected])

            actual = bitwise.decode(actual)

            self.assertEqual(actual, expected)
