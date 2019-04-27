import unittest
from netmon.netmon import Netmon

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.Netmon = Netmon('ipaddress.txt')
        self.Netmon.Run()

    def test_init(self):
        self.assertEqual(self.Netmon.Network.Addresses['Name'].Ip,'127.0.0.1')

if __name__ == '__main__':
    unittest.main()
