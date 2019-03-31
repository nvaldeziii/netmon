import unittest
from netmon import Netmon

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.Netmon = Netmon('ipaddress_test.txt')
        self.Netmon.Run()

    def test_init(self):
        self.assertEqual(self.Netmon.Network.Address['Name'].Ip,'127.0.0.1')

if __name__ == '__main__':
    unittest.main()
