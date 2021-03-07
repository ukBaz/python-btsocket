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


if __name__ == '__main__':
    unittest.main()
