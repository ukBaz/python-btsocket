import enum
import logging
from btsocket import btmgmt_sync


logger = logging.getLogger("btsocket.btmgmt_protocol")
logger.setLevel(logging.INFO)


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
adv_data = "1bfff0ff6DB643CF7E8F471188665938D17AAA26495E131415161718"
adv_data_len = len(bytes.fromhex(adv_data))
scan_rsp = ""  # (0-255 Octets)
scan_rsp_len = len(bytes.fromhex(scan_rsp))


def show_result(data):
    print(data.event_frame.command_opcode, data.event_frame.status)


show_result(
    btmgmt_sync.send(
        "AddAdvertising",
        ctrl_idx,
        instance,
        flags,
        duration,
        timeout,
        adv_data_len,
        scan_rsp_len,
        adv_data,
        scan_rsp,
    )
)

input("Press <enter> key to end advertisement")

show_result(
    btmgmt_sync.send(
        "RemoveAdvertising",
        ctrl_idx,
        instance,
    )
)
