import asyncio
import enum
import sys

from btsocket import btmgmt_socket
from btsocket import btmgmt_protocol


class Flags(enum.IntEnum):
    CONNECTABLE = enum.auto()
    GENERAL_DISCOVERABLE = enum.auto()
    LIMITED_DISCOVERABLE = enum.auto()
    FLAGS_IN_ADV_DATA = enum.auto()
    TX_IN_ADV_DATA = enum.auto()
    APPEARANCE_IN_ADV_DATA = enum.auto()
    LOCAL_NAME_IN_ADV_DATA = enum.auto()
    PHY_LE_1M = enum.auto()
    PHY_LE_2M = enum.auto()
    PHY_LE_CODED = enum.auto()


def little_bytes(value, size_of):
    return int(value).to_bytes(size_of, byteorder='little')


def advert_command(instance_id, flags, duration, timeout, adv_data, scan_rsp):
    cmd = little_bytes(0x003e, 2)
    ctrl_idx = little_bytes(0x00, 2)
    instance = little_bytes(instance_id, 1)  # (1 Octet)
    flags = little_bytes(flags, 4)  # (4 Octets)
    duration = little_bytes(duration, 2)  # (2 Octets)
    timeout = little_bytes(timeout, 2)  # (2 Octets)
    adv_data = bytes.fromhex(adv_data)  # (0-255 Octets)
    adv_data_len = little_bytes(len(adv_data), 1)  # (1 Octet)
    scan_rsp = bytes.fromhex(scan_rsp)  # (0-255 Octets)
    scan_rsp_len = little_bytes(len(scan_rsp), 1)  # (1 Octet)
    params = instance + flags + duration + timeout + adv_data_len + scan_rsp_len + adv_data + scan_rsp
    param_len = little_bytes(len(params), 2)

    return cmd + ctrl_idx + param_len + params


def test_asyncio_usage():
    sock = btmgmt_socket.open()

    if sys.version_info < (3, 10):
        loop = asyncio.get_event_loop()
    else:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

    def reader():
        raw_data = sock.recv(100)
        data = btmgmt_protocol.reader(raw_data)
        print("Received:", data.event_frame.command_opcode, data.event_frame.status)

        # We are done: unregister the file descriptor
        loop.remove_reader(sock)

        # Stop the event loop
        loop.stop()

    # Register the file descriptor for read event
    loop.add_reader(sock, reader)

    # Write a command to the socket
    loop.call_soon(sock.send, advert_command(
        instance_id=1,
        flags=Flags.GENERAL_DISCOVERABLE,
        duration=0x00,  # zero means use default
        timeout=0x00,  # zero means use default
        adv_data='1bfff0ff6DB643CF7E8F471188665938D17AAA26495E131415161718',
        scan_rsp='',
    ))

    try:
        # Run the event loop
        loop.run_forever()
    finally:
        # We are done. Close sockets and the event loop.
        btmgmt_socket.close(sock)
        loop.close()


if __name__ == '__main__':
    test_asyncio_usage()
