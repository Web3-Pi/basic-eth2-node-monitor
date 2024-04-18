import argparse

from config.conf import LIGHTHOUSE_LETTER, GENERIC_CONSENSUS_CLIENT_LETTER


class BaseAppendAction(argparse._AppendAction):
    ALLOWED_CONSENSUS_CLIENTS = {LIGHTHOUSE_LETTER, LIGHTHOUSE_LETTER.upper(),
                                 GENERIC_CONSENSUS_CLIENT_LETTER, GENERIC_CONSENSUS_CLIENT_LETTER.upper()}

    @classmethod
    def validate_supported_consensus_clients(cls, arg: str) -> str:
        if arg not in cls.ALLOWED_CONSENSUS_CLIENTS:
            return f"Only {cls.ALLOWED_CONSENSUS_CLIENTS} client specification allowed, provided {arg}"

        return ""
