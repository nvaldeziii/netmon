import unittest

import sys
sys.path.insert(0,'..')
from netmon.netmon import FileReader

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.FileReader = FileReader('ipaddress.txt')

    def test_Read(self):
        self.assertEqual(self.FileReader.Lines[0],'Name,127.0.0.1')
        self.assertEqual(self.FileReader.Lines[1],'Name2,127.0.0.2')
        self.assertEqual(self.FileReader.Lines[2],'Name4,127.0.0.4')

if __name__ == '__main__':
    unittest.main()
