class DefaultEntryFields:
    # Measurement names
    CPU = "cpu"
    MEM = "mem"
    SWAP = "swap"
    DISK = "disk"
    STATUS_NODE = "status_node"
    STATUS_EXEC = "status_exec"
    STATUS_CONSENSUS = "status_consensus"
    CHAIN = "chain"

    # Tags
    HOST_NAME = "host"

    # Fields
    USED_PERCENT = "used_percent"
    USED_BYTES = "used_bytes"
    ACTIVE_PERCENT = "active_percent"
    LAST_BLOCK = "last_block"

    SYNC_PART_PERC_0 = "sync_part_perc_0"
    SYNC_PART_PERC_1 = "sync_part_perc_1"
    SYNC_PART_PERC_2 = "sync_part_perc_2"
    SYNC_PART_PERC_3 = "sync_part_perc_3"


class DefaultStatusValues:

    INACTIVE = 0.0
    WAITING = 40.0
    SYNCING = 50.0
    SYNCED = 100.0
