import unittest
from src.net_scanner import ping_ip

class TestNetScanner(unittest.TestCase):
    def test_ping_ip(self):
        result = ping_ip("127.0.0.1")
        self.assertEqual(result[1], "Active")

if __name__ == "__main__":
    unittest.main()
