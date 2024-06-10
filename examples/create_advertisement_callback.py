import enum
import logging

from btsocket import btmgmt_callback
from btsocket import btmgmt_protocol


# logger = logging.getLogger("btsocket.btmgmt_callback")
# logger.setLevel(logging.DEBUG)
logger_prot = logging.getLogger('btsocket.btmgmt_protocol')
logger_prot.setLevel(logging.INFO)


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


ctrl_idx = 0  # hci0
instance = 1  # Arbitrary value
flags = Flags.GENERAL_DISCOVERABLE
duration = 0x00  # 0 means use default
timeout = 0x0  # 0 means use default
adv_data = "1bfff0ff6DB643CF7E8F471188665938D17AAA26495E131415161718"  # (0-255 Octets)
adv_data_len = len(bytes.fromhex(adv_data))
scan_rsp = ""  # (0-255 Octets)
scan_rsp_len = len(bytes.fromhex(scan_rsp))


def show_result(pkt, mgmt_class):
    print(pkt)


def main():
    mgmt = btmgmt_callback.Mgmt()
    mgmt.add_event_callback(btmgmt_protocol.Events.CommandCompleteEvent, show_result)
    mgmt.send('AddAdvertising', ctrl_idx,
              instance,
              flags,
              duration,
              timeout,
              adv_data_len,
              scan_rsp_len,
              adv_data,
              scan_rsp)

    mgmt.start()


if __name__ == '__main__':
    main()
