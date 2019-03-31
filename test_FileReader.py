import unittest
from netmon import FileReader

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.FileReader = FileReader('ipaddress_test.txt')

    def test_Read(self):
        self.assertEqual(self.FileReader.Lines[0],'Name,127.0.0.1')
        self.assertEqual(self.FileReader.Lines[1],'Name2,127.0.0.2')

if __name__ == '__main__':
    unittest.main()
