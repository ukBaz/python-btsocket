import unittest
from btsocket import btmgmt_protocol


class TestAddress(unittest.TestCase):
    def test_address_decode(self):
        addr = btmgmt_protocol.Address()
        addr.decode(b'\xa4\x0c\x8f\xae\xf8\xfc')
        self.assertEqual('FC:F8:AE:8F:0C:A4', addr.value)

    def test_address_evcode(self):
        addr = btmgmt_protocol.Address()
        addr.encode('FC:F8:AE:8F:0C:A4', 6)
        self.assertEqual(b'\xa4\x0c\x8f\xae\xf8\xfc', addr.octets)


class TestCurrentSettings(unittest.TestCase):
    def test_settings_decode(self):
        expected = {btmgmt_protocol.SupportedSettings.Advertising: False,
                    btmgmt_protocol.SupportedSettings.Powered: True,
                    btmgmt_protocol.SupportedSettings.Connectable: False,
                    btmgmt_protocol.SupportedSettings.FastConnectable: False,
                    btmgmt_protocol.SupportedSettings.Discoverable: False,
                    btmgmt_protocol.SupportedSettings.Bondable: False,
                    btmgmt_protocol.SupportedSettings.LinkLevelSecurity: False,
                    btmgmt_protocol.SupportedSettings.LowEnergy: True,
                    btmgmt_protocol.SupportedSettings.SecureSimplePairing: True,
                    btmgmt_protocol.SupportedSettings.BREDR: True,
                    btmgmt_protocol.SupportedSettings.HighSpeed: False,
                    btmgmt_protocol.SupportedSettings.WidebandSpeech: False,
                    btmgmt_protocol.SupportedSettings.SecureConnections: True,
                    btmgmt_protocol.SupportedSettings.DebugKeys: False,
                    btmgmt_protocol.SupportedSettings.Privacy: False,
                    btmgmt_protocol.SupportedSettings.ControllerConfiguration: False,
                    btmgmt_protocol.SupportedSettings.StaticAddress: False,
                    btmgmt_protocol.SupportedSettings.PHYConfiguration: False}
        settings = btmgmt_protocol.CurrentSettings()
        settings.decode(b'\xc1\n\x00\x00')
        self.assertEqual(expected, settings.value)


class TestEirData(unittest.TestCase):
    def test_eir_data_decode_sd(self):
        expected = {btmgmt_protocol.ADType.Flags: b'\x1a',
                    btmgmt_protocol.ADType.CompleteUUID16ServiceList: b'o\xfd',
                    btmgmt_protocol.ADType.ServiceDataUUID16: b'o\xfds\xc6\xde\xa5\xac>=\x8b\x1b\xe5\xe5\xac\x8f\xd0\xea7%\xa4\xe7\xcd'}

        data = b'\x02\x01\x1a\x03\x03o\xfd\x17\x16o\xfds\xc6\xde\xa5\xac>=\x8b\x1b\xe5\xe5\xac\x8f\xd0\xea7%\xa4\xe7\xcd'
        eir_data = btmgmt_protocol.EIRData()
        eir_data.decode(data)
        self.assertDictEqual(expected, eir_data.value)

    def test_eir_data_decode_md(self):
        expected = {btmgmt_protocol.ADType.Flags: b'\x06',
                    btmgmt_protocol.ADType.CompleteName: b'DC76F7E1',
                    btmgmt_protocol.ADType.ManufacturerData: b'3\x01(\xa7(\x96(\x8c\x00\x00\x00\xf4\x02\x03\x00\xcb\x01\xcf\x00\xe5\x01\xe9\x00\x00\x00\x00\x00'}

        data = b'\x02\x01\x06\x11\xff3\x01\x1bd\x0e\x10\x0bC\x00\xf0\x01\xf3(\x89\x01\x00\t\tDC76F7E1\x1c\xff3\x01(' \
               b'\xa7(\x96(\x8c\x00\x00\x00\xf4\x02\x03\x00\xcb\x01\xcf\x00\xe5\x01\xe9\x00\x00\x00\x00\x00'
        eir_data = btmgmt_protocol.EIRData()
        eir_data.decode(data)
        self.assertEqual(expected, eir_data.value)


class TestAddressTypes(unittest.TestCase):
    def test_address_type_decode_all(self):
        expected = [btmgmt_protocol.AddressType.BREDR,
                    btmgmt_protocol.AddressType.LEPublic,
                    btmgmt_protocol.AddressType.LERandom]
        addr_type = btmgmt_protocol.AddressTypeField()
        addr_type.decode(b'\x07')
        self.assertEqual(expected, addr_type.value)

    def test_address_type_decode_le(self):
        expected = [btmgmt_protocol.AddressType.LEPublic,
                    btmgmt_protocol.AddressType.LERandom]
        addr_type = btmgmt_protocol.AddressTypeField()
        addr_type.decode(b'\x06')
        self.assertEqual(expected, addr_type.value)

    def test_address_type_decode_bdedr(self):
        expected = [btmgmt_protocol.AddressType.BREDR]
        addr_type = btmgmt_protocol.AddressTypeField()
        addr_type.decode(b'\x01')
        self.assertEqual(expected, addr_type.value)

    def test_address_type_encode_all(self):
        addr_type = btmgmt_protocol.AddressTypeField()
        addr_type.encode([btmgmt_protocol.AddressType.BREDR,
                          btmgmt_protocol.AddressType.LEPublic,
                          btmgmt_protocol.AddressType.LERandom], 1)
        self.assertEqual(b'\x07', addr_type.octets)

    def test_address_type_encode_ble(self):
        addr_type = btmgmt_protocol.AddressTypeField()
        addr_type.encode([btmgmt_protocol.AddressType.LEPublic,
                          btmgmt_protocol.AddressType.LERandom], 1)
        self.assertEqual(b'\x06', addr_type.octets)

    def test_address_type_encode_bredr(self):
        addr_type = btmgmt_protocol.AddressTypeField()
        addr_type.encode([btmgmt_protocol.AddressType.BREDR], 1)
        self.assertEqual(b'\x01', addr_type.octets)


if __name__ == '__main__':
    unittest.main()
