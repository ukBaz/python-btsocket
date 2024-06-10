import unittest
from btsocket import btmgmt_protocol


class TestCmdReponse(unittest.TestCase):
    def test_version_cmd(self):
        expected = b'\x01\x00\xff\xff\x00\x00'
        pkt = btmgmt_protocol.command('ReadManagementVersionInformation', None)
        self.assertEqual(expected, pkt.header.octets)

    def test_disconnect_cmd(self):
        expected = b'\x14\x00\x00\x00\x07\x00\x2d\x11\x37\x5e\x10\xe5\x01'

        pkt = btmgmt_protocol.command('Disconnect', 0, 'E5:10:5E:37:11:2D',
                                      [btmgmt_protocol.AddressType.BREDR])
        self.assertEqual(expected,
                         pkt.header.octets + pkt.cmd_params_frame.octets)

    def test_power_on_cmd(self):
        expected = b'\x05\x00\x00\x00\x01\x00\x01'

        pkt = btmgmt_protocol.command('SetPowered', 0, 1)
        self.assertEqual(expected,
                         pkt.header.octets + pkt.cmd_params_frame.octets)

    def test_add_adv(self):
        expected = bytes.fromhex('3e00000027000102000000000000001c001bfff0ff6db643cf7e8f4711886659'
                                 '38d17aaa26495e131415161718')
        pkt = btmgmt_protocol.command('AddAdvertising', 0,
                                      1, 2, 0, 0, 0x1c, 0,
                                      "1bfff0ff6DB643CF7E8F471188665938D17AAA26495E131415161718", '')
        self.assertEqual(expected,
                         pkt.header.octets + pkt.cmd_params_frame.octets)


if __name__ == '__main__':
    unittest.main()
