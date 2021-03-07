import logging
from btsocket import btmgmt_callback
from btsocket import btmgmt_protocol

device_addr = 'E5:10:5E:37:11:2D'

# btmgmt_callback.logger.setLevel(logging.INFO)
# btmgmt_protocol.logger.setLevel(logging.DEBUG)


def connect(mgmt_class):
    mgmt_class.send('ReadManagementVersionInformation', 0xffff)
    mgmt_class.send('AddDevice', 0, device_addr,
                    [btmgmt_protocol.AddressType.LEPublic], 2)
    mgmt_class.send('StartDiscovery', 0,
                    [btmgmt_protocol.AddressType.LEPublic])


def disconnect(mgmt):
    mgmt.send('RemoveDevice', 0, device_addr,
              [btmgmt_protocol.AddressType.LEPublic])
    mgmt.send('Disconnect', 0, device_addr,
              [btmgmt_protocol.AddressType.LEPublic])


def on_connected(data, mgmt_class):
    if data.event_frame.address == device_addr:
        print('Connected...')
        mgmt_class.send('StopDiscovery', 0,
                        [btmgmt_protocol.AddressType.LEPublic])
    mgmt_class.loop.call_later(10, disconnect, mgmt_class)


def on_disconnect(data, mgmt_class):
    if data.event_frame.command_opcode == btmgmt_protocol.Commands.Disconnect:
        print('Disconnected...')
        mgmt_class.stop()
        print('Exiting...')


def app():
    mgmt = btmgmt_callback.Mgmt()
    mgmt.add_event_callback(btmgmt_protocol.Events.DeviceConnectedEvent,
                            on_connected)
    mgmt.add_event_callback(btmgmt_protocol.Events.CommandCompleteEvent,
                            on_disconnect)
    connect(mgmt)
    try:
        mgmt.start()
    except KeyboardInterrupt:
        mgmt.stop()
    finally:
        mgmt.close()


if __name__ == '__main__':
    app()
