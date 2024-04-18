import argparse
from typing import List

from app.inputargs.customactions.baseappendaction import BaseAppendAction
from app.inputargs.customactions.helpers.defaults import update_default_ports
from app.inputargs.customactions.helpers.validators import validate_num_args, validate_endpoint_with_ports
from config.conf import DEFAULT_GETH_WS_PORT, DEFAULT_CONSENSUS_CLI_HTTP_PORT, DEFAULT_SYSTEM_MONITOR_PORT


class SubparseAndAppendSingleNodeAction(BaseAppendAction):
    MIN_ARGS = 2
    MAX_ARGS = 5
    DEFAULT_PORTS = [DEFAULT_GETH_WS_PORT, DEFAULT_CONSENSUS_CLI_HTTP_PORT, DEFAULT_SYSTEM_MONITOR_PORT]

    @classmethod
    def validate(cls, values: List) -> str:
        msg = validate_num_args(values, cls.MIN_ARGS, cls.MAX_ARGS)
        msg = cls.validate_supported_consensus_clients(values[1]) if msg == "" else msg
        msg = validate_endpoint_with_ports(values, 2) if msg == "" else msg

        return msg

    def parse_me(self, values) -> List:
        msg = self.validate(values)
        if msg != "":
            raise argparse.ArgumentError(self, msg)

        return update_default_ports(values, self.DEFAULT_PORTS, 2)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, self.parse_me(values), option_string)
