import unittest
import time
from netmon.netmon import IpAddress

class TestIpAddress(unittest.TestCase):
    INITIAL_TIME = 10
    def setUp(self):
        self.current_time = TestIpAddress.INITIAL_TIME
        self.last_ok_ping_time = TestIpAddress.INITIAL_TIME
        self.expected_downtime = 0
        self.expected_uptime = 0
        self.prev_up_status = True

        self.GoodIpAddress = IpAddress('127.0.0.1' ,initial_time=TestIpAddress.INITIAL_TIME)
        self.BadIpAddress = IpAddress('192.168.254.254' ,initial_time=TestIpAddress.INITIAL_TIME)

    def test_init(self):
        self.assertEqual(self.BadIpAddress.Ip, '192.168.254.254' )
        self.assertEqual(self.GoodIpAddress.Ip, '127.0.0.1' )
        self.assert_all_ip_attribute(self.GoodIpAddress,0,0,TestIpAddress.INITIAL_TIME,10,self.prev_up_status)
        self.assert_all_ip_attribute(self.BadIpAddress,0,0,TestIpAddress.INITIAL_TIME,10,self.prev_up_status)

    def test_refresh_good_ping_only(self):
        self.move_time_and_assert(True, self.GoodIpAddress,1,0)
        self.move_time_and_assert(True, self.GoodIpAddress,2,0)

    def test_refresh_bad_ping_only(self):
        self.move_time_and_assert(False, self.GoodIpAddress,0,1)
        self.move_time_and_assert(False, self.GoodIpAddress,0,2)

    def test_refresh_bad_ping_then_good(self):
        self.move_time_and_assert(True, self.GoodIpAddress,1,0)
        self.move_time_and_assert(False, self.GoodIpAddress,1,1)
        self.move_time_and_assert(True, self.GoodIpAddress,0,1)
        self.move_time_and_assert(True, self.GoodIpAddress,1,1)

    def test_refresh_good_ping_then_bad(self):
        self.move_time_and_assert(True, self.GoodIpAddress,1,0)
        self.move_time_and_assert(False, self.GoodIpAddress,1,1)
        self.move_time_and_assert(False, self.GoodIpAddress,1,2)

    def assert_all_ip_attribute(self,ip_address_obj, uptime, downtime,
        time_of_last_success_ping,time_of_last_ping, Is_Up):
        self.assertEqual(ip_address_obj.Uptime, uptime )
        self.assertEqual(ip_address_obj.Downtime, downtime )
        self.assertEqual(ip_address_obj.time_of_last_success_ping, time_of_last_success_ping )
        self.assertEqual(ip_address_obj.time_of_last_ping, time_of_last_ping )
        self.assertEqual(ip_address_obj.Is_Up, Is_Up)

    def move_time_and_assert(self, isup, IpAddressObj, expect_up, expect_down):
        last_time = self.current_time
        self.current_time += 1
        if isup:
            if not self.prev_up_status:
                self.last_ok_ping_time = self.current_time
        else:
            if self.prev_up_status:
                self.last_ok_ping_time = last_time
        self.prev_up_status = isup

        IpAddressObj.refresh(isup, self.current_time)
        self.assert_all_ip_attribute(
            IpAddressObj,
            expect_up,
            expect_down,
            self.last_ok_ping_time,
            self.current_time,
            isup)

if __name__ == '__main__':
    unittest.main()
