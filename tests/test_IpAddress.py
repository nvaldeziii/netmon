import unittest
import time
from netmon.netmon import IpAddress

class TestIpAddress(unittest.TestCase):
    INITIAL_TIME = 10
    def setUp(self):
        self.GoodIpAddress = IpAddress('127.0.0.1' ,initial_time=TestIpAddress.INITIAL_TIME)
        self.BadIpAddress = IpAddress('192.168.254.254' ,initial_time=TestIpAddress.INITIAL_TIME)

    def test_init(self):
        self.assertEqual(self.BadIpAddress.Ip, '192.168.254.254' )
        self.assertEqual(self.GoodIpAddress.Ip, '127.0.0.1' )
        self.assert_all_ip_attribute(self.GoodIpAddress,0,0,TestIpAddress.INITIAL_TIME,10,False)
        self.assert_all_ip_attribute(self.BadIpAddress,0,0,TestIpAddress.INITIAL_TIME,10,False)

    def test_refresh_good_ping(self):
        current_time = TestIpAddress.INITIAL_TIME + 1
        self.GoodIpAddress.refresh(True, current_time)
        self.assert_all_ip_attribute(self.GoodIpAddress,1,0,TestIpAddress.INITIAL_TIME,current_time,True)
        current_time += 1
        self.GoodIpAddress.refresh(True, current_time)
        self.assert_all_ip_attribute(self.GoodIpAddress,2,0,TestIpAddress.INITIAL_TIME,current_time,True)

    def test_refresh_good_ping_then_bad(self):
        current_time = TestIpAddress.INITIAL_TIME + 1
        LAST_SUCCESS_PING_TIME = TestIpAddress.INITIAL_TIME + 1

        self.GoodIpAddress.refresh(True, current_time)
        self.assert_all_ip_attribute(self.GoodIpAddress,1,0,TestIpAddress.INITIAL_TIME,current_time,True)

        current_time += 1
        self.GoodIpAddress.refresh(False, current_time)
        self.assert_all_ip_attribute(self.GoodIpAddress,1,1,LAST_SUCCESS_PING_TIME,current_time,False)

        current_time += 1
        self.GoodIpAddress.refresh(False, current_time)
        self.assert_all_ip_attribute(self.GoodIpAddress,1,2,LAST_SUCCESS_PING_TIME,current_time,False)

    def assert_all_ip_attribute(self,ip_address_obj, uptime, downtime,
        time_of_last_success_ping,time_of_last_ping, Is_Up):
        self.assertEqual(ip_address_obj.Uptime, uptime )
        self.assertEqual(ip_address_obj.Downtime, downtime )
        self.assertEqual(ip_address_obj.time_of_last_success_ping, time_of_last_success_ping )
        self.assertEqual(ip_address_obj.time_of_last_ping, time_of_last_ping )
        self.assertEqual(ip_address_obj.Is_Up, Is_Up)

if __name__ == '__main__':
    unittest.main()
