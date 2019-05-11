import unittest

import sys
sys.path.insert(0,'..')
from netmon.netmon import FileReader

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.FileReader = FileReader('ipaddress_test.json')

    def test_Read(self):
        self.assertEqual("{},{}".format(self.FileReader.Lines[0].name,self.FileReader.Lines[0].ip),'Name,127.0.0.1')
        self.assertEqual("{},{}".format(self.FileReader.Lines[1].name,self.FileReader.Lines[1].ip),'Name2,127.0.0.2')
        self.assertEqual("{},{}".format(self.FileReader.Lines[2].name,self.FileReader.Lines[2].ip),'Name4,127.0.0.4')
        self.assertEqual("{},{}".format(self.FileReader.Lines[3].name,self.FileReader.Lines[3].ip),'Name5,192.168.254.250')

    def test_proxy(self):
        self.assertEqual(self.FileReader.Lines[2].proxy, "127.0.0.1")

if __name__ == '__main__':
    unittest.main()
