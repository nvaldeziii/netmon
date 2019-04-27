import unittest
from netmon.netmon import IpAddress
from netmon.netmon import Network

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.Network = Network()

    def test_add_ip_address(self):
        self.Network.add_ip_address('home',IpAddress('127.0.0.1'))
        self.assertEqual(self.Network.Address['home'].Ip,'127.0.0.1')

    def test_add_ip_address_duplicate(self):
        self.Network.add_ip_address('home',IpAddress('127.0.0.1'))
        self.assertRaises(self.Network.DuplicateAddressException, self.Network.add_ip_address, 'home',IpAddress('128.0.0.1'))


    def test_ping_success(self):
        self.Network.add_ip_address('home',IpAddress('127.0.0.1'))
        self.assertTrue(self.Network.ping('home'))

    def test_ping_fail(self):
        self.Network.add_ip_address('not_home',IpAddress('128.0.0.1'))
        self.assertFalse(self.Network.ping('not_home'))

if __name__ == '__main__':
    unittest.main()
