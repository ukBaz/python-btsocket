from btsocket import btmgmt_sync

data = btmgmt_sync.send('ReadManagementSupportedCommands', None)
print(f'Raw response: {data}')
print('Command Code |        Command Name            | Command Parameters')
print('=' * 65)

for cmd in data.cmd_response_frame.command:
    try:
        params = btmgmt_sync.btmgmt_protocol.cmds[cmd]
        required_params = [param.name for param in params.shape]
    except KeyError:
        required_params = None

    try:
        print(f'{cmd:<12} | {btmgmt_sync.btmgmt_protocol.Commands(cmd):30} | '
              f'{required_params}')
    except ValueError:
        pass

from time import sleep
sleep(10)
