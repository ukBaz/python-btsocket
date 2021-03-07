import logging
from btsocket import btmgmt_sync
from btsocket import tools


def show_result(response):
    from btsocket import btmgmt_protocol
    print(response.event_frame.command_opcode,
          '-',
          response.cmd_response_frame.current_settings.get(
              btmgmt_protocol.SupportedSettings.Powered),
          '-',
          response.event_frame.status)


logger = logging.getLogger('btsocket.btmgmt_sync')
logger.setLevel(logging.INFO)

data = btmgmt_sync.send('ReadManagementVersionInformation', None)
print(f'Bluez mgmt Version: '
      f'{data.cmd_response_frame.version}.{data.cmd_response_frame.revision}')
data = btmgmt_sync.send('SetPowered', 0, 0)
show_result(data)
data = btmgmt_sync.send('SetPowered', 0, 1)
show_result(data)
