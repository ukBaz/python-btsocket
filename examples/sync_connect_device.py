import logging
from time import sleep
from btsocket import btmgmt_sync
from btsocket import btmgmt_protocol

btmgmt_sync.logger.setLevel(logging.INFO)


def show_result(data):
    print(data.event_frame.command_opcode, data.event_frame.status)


show_result(btmgmt_sync.send('AddDevice', 0, 'E5:10:5E:37:11:2D',
                             [btmgmt_protocol.AddressType.LEPublic], 2))
show_result(btmgmt_sync.send('StartDiscovery', 0,
                             [btmgmt_protocol.AddressType.BREDR,
                              btmgmt_protocol.AddressType.LERandom,
                              btmgmt_protocol.AddressType.LEPublic]))
sleep(4)
success = False
while not success:
    try:
        show_result(btmgmt_sync.send('StopDiscovery', 0,
                                     [btmgmt_protocol.AddressType.BREDR,
                                      btmgmt_protocol.AddressType.LERandom,
                                      btmgmt_protocol.AddressType.LEPublic]))
    except NameError:
        print('Attempt stop discovery again...')
    finally:
        success = True
    sleep(1)
show_result(btmgmt_sync.send('RemoveDevice', 0, 'E5:10:5E:37:11:2D',
                             [btmgmt_protocol.AddressType.LEPublic]))
show_result(btmgmt_sync.send('Disconnect', 0, 'E5:10:5E:37:11:2D',
                             [btmgmt_protocol.AddressType.LEPublic]))
