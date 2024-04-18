import enum


class ClientSyncingStatus(enum.Enum):
    INACTIVE = 0
    WAITING = 1
    SYNCING = 2
    SYNCED = 3


class NodeSyncingStatus(enum.Enum):
    INACTIVE = 0
    SYNCING = 2
    SYNCED = 3
