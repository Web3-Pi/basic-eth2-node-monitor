from __future__ import annotations

import enum


class SupportedClients(enum.Enum):
    GETH = 0
    LIGHTHOUSE = 1
    GENERIC_CONSENSUS = 2

    @classmethod
    def str_repr(cls, c: SupportedClients) -> str:
        d = {
            SupportedClients.GETH: "Geth",
            SupportedClients.LIGHTHOUSE: "Lighthouse",
            SupportedClients.GENERIC_CONSENSUS: "Generic consensus client"
        }

        return d[c]
