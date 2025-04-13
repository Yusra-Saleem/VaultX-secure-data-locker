import unittest
from src.encryption.fernet_handler import generate_key, encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.key = generate_key()
        self.plaintext = "Test data for encryption"
        self.ciphertext = encrypt_data(self.plaintext, self.key)

    def test_encrypt_data(self):
        self.assertIsNotNone(self.ciphertext)
        self.assertNotEqual(self.plaintext, self.ciphertext)

    def test_decrypt_data(self):
        decrypted_data = decrypt_data(self.ciphertext, self.key)
        self.assertEqual(self.plaintext, decrypted_data)

    def test_decrypt_invalid_data(self):
        with self.assertRaises(Exception):
            decrypt_data("invalid_data", self.key)

if __name__ == '__main__':
    unittest.main()