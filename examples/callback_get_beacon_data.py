import logging
from btsocket import btmgmt_callback
from btsocket import btmgmt_protocol

scan_loop = 0
max_scans = 4
beacon_address = 'DC:76:F7:E1:62:E0'

logger = logging.getLogger('btsocket.btmgmt_protocol')
logger.setLevel(logging.INFO)


def print_sensor_data(data):
    """
    Function to print sensor beacon data in pretty format
    """
    if len(data) == 14:
        battery_lvl = data[1]
        inst_temp = int.from_bytes(data[6:8],
                                   byteorder='big', signed=True) / 10
        humidity = int.from_bytes(data[8:10],
                                  byteorder='big', signed=True) / 10
        print(f'\tTemperature:   {inst_temp}\u00B0C')
        print(f'\tHumidity:      {humidity}%')
        print(f'\tBattery Level:  {battery_lvl}%')


def close_loop(data, mgmt_class):
    """
    Callback for when discovering event has happened. In this example
    check to see how many times discovery has timed out. If it is `max_scans
    then exit

    :param data: discovering event packet
    :param mgmt_class: Mgmt class object to access enums etc
    """
    global scan_loop
    if data.event_frame.discovering == 0:
        print(f'Discovering loop {scan_loop} ended')
        scan_loop += 1
        if scan_loop < max_scans:
            mgmt_class.send('StartDiscovery', 0,
                            [btmgmt_protocol.AddressType.LEPublic,
                             btmgmt_protocol.AddressType.LERandom])
        else:
            mgmt_class.stop()


def device_found(data, mgmt_class):
    """
    Callback for when device is found

    :param data: Device found event packet
    :param mgmt_class: Mgmt class object to access enums etc
    """
    if data.event_frame.address == beacon_address:
        eir_data = data.event_frame.eir_data
        manuf_data = eir_data.get(btmgmt_protocol.ADType.ManufacturerData)
        if all((manuf_data,
                manuf_data.startswith(b'\x33\01'),
                len(manuf_data) == 16)):
            print_sensor_data(manuf_data[2:])
            mgmt_class.stop()


def app():
    mgmt = btmgmt_callback.Mgmt()
    mgmt.add_event_callback(btmgmt_protocol.Events.DiscoveringEvent,
                            close_loop)
    mgmt.add_event_callback(btmgmt_protocol.Events.DeviceFoundEvent,
                            device_found)
    mgmt.send('StartDiscovery', 0, [btmgmt_protocol.AddressType.LEPublic,
                                    btmgmt_protocol.AddressType.LERandom])
    print('Starting search...')
    mgmt.start()


if __name__ == '__main__':
    app()
