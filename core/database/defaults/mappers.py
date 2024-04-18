import math

from core.sampling.samplers.node.results.syncstatus import ClientSyncingStatus, NodeSyncingStatus
from core.database.defaults.defaults import DefaultStatusValues


def client_sync_status_to_float(c: ClientSyncingStatus) -> float:
    mapping = {
        ClientSyncingStatus.INACTIVE: DefaultStatusValues.INACTIVE,
        ClientSyncingStatus.WAITING: DefaultStatusValues.WAITING,
        ClientSyncingStatus.SYNCING: DefaultStatusValues.SYNCING,
        ClientSyncingStatus.SYNCED: DefaultStatusValues.SYNCED
    }

    return mapping[c]


def node_sync_status_to_float(n: NodeSyncingStatus) -> float:
    mapping = {
        NodeSyncingStatus.INACTIVE: DefaultStatusValues.INACTIVE,
        NodeSyncingStatus.SYNCING: DefaultStatusValues.SYNCING,
        NodeSyncingStatus.SYNCED: DefaultStatusValues.SYNCED
    }

    return mapping[n]


def sync_percent_to_sync_percent_4(percent: float) -> [float, float, float, float]:
    p1 = 0.0
    p2 = 0.0
    p3 = 0.0

    if percent == 100.0:
        p0 = p1 = p2 = p3 = 100.0
    else:
        p0 = float(math.ceil(percent))
        if p0 == 100.0:
            p1 = 100.0 * math.modf(percent)[0]
            if math.ceil(p1) == 100.0:
                p2 = 100.0 * math.modf(p1)[0]
                p1 = 100.0
                if math.ceil(p2) == 100.0:
                    p3 = 100.0 * math.modf(p2)[0]
                    p2 = 100.0

    return p0, p1, p2, p3
