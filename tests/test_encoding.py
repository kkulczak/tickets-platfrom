import re
from unittest import TestCase

from translation_engine import decode, encode, SEPARATOR

original_message = (
    'This is a long looong test sentence,\n'
    'with some big (biiiiig) words!'
)

encoded_message = (
    '\n—weird—\n'
    'Tihs is a lnog loonog tset sntceene,\n'
    'wtih smoe big (biiiiig) wdros!'
    '\n—weird—\n'
    'long looong sentence some test This with words'
)

decoded_message = (
    'This is a long looong test sentence,\n'
    'with some big (biiiiig) words!'
)


class Test(TestCase):
    def test_encode(self):
        message = encode(original_message)

    def test_encode_empy_msg(self):
        empty_mes = encode('')
        self.assertSequenceEqual(empty_mes, f'{SEPARATOR}{SEPARATOR}')

    def test_decode(self):
        dec = decode(encoded_message)
        self.assertSequenceEqual(dec, decoded_message)

    def test_decode_empty_msg(self):
        dec = decode(encoded_message)
        self.assertSequenceEqual(dec, decoded_message)

    def test_encode_decode(self):
        enc = encode(original_message)
        dec = decode(enc)
        self.assertSequenceEqual(dec, original_message)

    def test_encode_decode_special(self):
        msg = '!_2(%*#&'
        self.assertSequenceEqual(decode(encode(msg)), msg)

    def test_decode_sepratators(self):
        with self.assertRaises(ValueError):
            decode(f'{SEPARATOR}')
        with self.assertRaises(ValueError):
            decode(f'{SEPARATOR}' * 3)
        with self.assertRaises(ValueError):
            decode(f'invalid_data{SEPARATOR}Tihs{SEPARATOR}This')
