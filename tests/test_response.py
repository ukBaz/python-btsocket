import unittest
from btsocket import btmgmt_protocol


class TestCmdReponse(unittest.TestCase):
    def test_version_cmd(self):
        expected = ('Response(header=<event_code=CommandCompleteEvent, '
                    'controller_idx=65535, '
                    'param_len=6>, '
                    'event_frame=<command_opcode=ReadManagementVersionInformation, '
                    'status=Success>, '
                    'cmd_response_frame=<version=1, revision=14>)')
        recvd = b'\x01\x00\xff\xff\x06\x00\x01\x00\x00\x01\x0e\x00'
        pkt = btmgmt_protocol.reader(recvd)
        self.assertEqual(expected, str(pkt))
        self.assertEqual(1, pkt.cmd_response_frame.version)
        self.assertEqual(14, pkt.cmd_response_frame.revision)

    def test_commands(self):
        expected = ('Response(header=<event_code=CommandCompleteEvent, '
                    'controller_idx=65535,'
                    ' param_len=41>, '
                    'event_frame=<command_opcode=ReadManagementSupportedCommands, '
                    'status=Success>, '
                    'cmd_response_frame=<num_of_commands=6, num_of_events=11, '
                    'command=[3, 4, 54, 55, 60, 66], event=[4, 5, 6, 7, 8, 29, '
                    '30, 31, 32, 33, 37]>)')
        recvd = (b'\x01\x00\xff\xff)\x00\x02\x00\x00\x06\x00\x0b\x00\x03\x00'
                 b'\x04\x006\x007\x00<\x00B\x00\x04\x00\x05\x00\x06\x00\x07'
                 b'\x00\x08\x00\x1d\x00\x1e\x00\x1f\x00 \x00!\x00%\x00')
        pkt = btmgmt_protocol.reader(recvd)
        self.assertEqual(expected, str(pkt))

    def test_controllers(self):
        expected = ("Response(header=<event_code=CommandCompleteEvent, "
                    "controller_idx=0, "
                    "param_len=283>, "
                    "event_frame=<command_opcode=ReadControllerInformation, "
                    "status=Success>,"
                    " cmd_response_frame=<address=FC:F8:AE:8F:0C:A4, "
                    "bluetooth_version=6, manufacturer=2, "
                    "supported_settings=130815, current_settings={Powered: True,"
                    " Connectable: False, FastConnectable: False, "
                    "Discoverable: False, Bondable: False, "
                    "LinkLevelSecurity: False, "
                    "SecureSimplePairing: True, BREDR: True, "
                    "HighSpeed: False, LowEnergy: True, Advertising: False, "
                    "SecureConnections: True, DebugKeys: False, Privacy: False,"
                    " ControllerConfiguration: False, StaticAddress: False, "
                    "PHYConfiguration: False, WidebandSpeech: False}, "
                    "class_of_device=786700, name=b'thinkabit1',"
                    " short_name=0>)")
        recvd = (b'\x01\x00\x00\x00\x1b\x01\x04\x00\x00\xa4\x0c\x8f\xae\xf8'
                 b'\xfc\x06\x02\x00\xff\xfe\x01\x00\xc1\n\x00\x00\x0c\x01'
                 b'\x0cthinkabit1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00')
        pkt = btmgmt_protocol.reader(recvd)
        self.assertEqual(expected, str(pkt))

    def test_info(self):
        expected = ('Response(header=<event_code=CommandStatusEvent, '
                    'controller_idx=0, '
                    'param_len=3>, event_frame=<command_opcode=SetPowered, '
                    'status=PermissionDenied>, '
                    'cmd_response_frame=None)')
        recvd = b'\x02\x00\x00\x00\x03\x00\x05\x00\x14'
        pkt = btmgmt_protocol.reader(recvd)
        self.assertEqual(expected, str(pkt))

    def test_power_off_fail(self):
        expected = ('Response(header=<event_code=CommandStatusEvent, '
                    'controller_idx=0, '
                    'param_len=3>, event_frame=<command_opcode=SetConnectable, '
                    'status=PermissionDenied>, '
                    'cmd_response_frame=None)')
        recvd = b'\x02\x00\x00\x00\x03\x00\x07\x00\x14'
        pkt = btmgmt_protocol.reader(recvd)
        self.assertEqual(expected, str(pkt))

    def test_support_cmd_names(self):
        expected = ('Response(header=<event_code=CommandCompleteEvent, '
                    'controller_idx=65535, '
                    'param_len=41>, '
                    'event_frame=<command_opcode=ReadManagementSupportedCommands, '
                    'status=Success>, '
                    'cmd_response_frame=<num_of_commands=6, num_of_events=11, '
                    'command=[3, 4, 54, 55, 60, 66], event=[4, 5, 6, 7, 8, '
                    '29, 30, 31, 32, 33, 37]>)')
        recvd = (b'\x01\x00\xff\xff)\x00\x02\x00\x00\x06\x00\x0b\x00\x03\x00'
                 b'\x04\x006\x007\x00<\x00B\x00\x04\x00\x05\x00\x06\x00\x07'
                 b'\x00\x08\x00\x1d\x00\x1e\x00\x1f\x00 \x00!\x00%\x00')
        pkt = btmgmt_protocol.reader(recvd)
        self.assertEqual(expected, str(pkt))


if __name__ == '__main__':
    unittest.main()
