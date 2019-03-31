import unittest
from netmon import IpAddress
from netmon import Network

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.Network = Network()

    def test_add_ip_address(self):
        self.Network.add_ip_address('home',IpAddress('128.0.0.1'))
        self.assertEqual(self.Network.NetworkAddress['home'].Ip,'128.0.0.1')

if __name__ == '__main__':
    unittest.main()
