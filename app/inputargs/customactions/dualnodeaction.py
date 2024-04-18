import argparse
from typing import List

from app.inputargs.customactions.baseappendaction import BaseAppendAction
from app.inputargs.customactions.helpers.defaults import update_default_ports
from app.inputargs.customactions.helpers.typetesters import represents_numeric
from app.inputargs.customactions.helpers.validators import validate_num_args, validate_endpoint_with_ports
from config.conf import DEFAULT_GETH_WS_PORT, DEFAULT_CONSENSUS_CLI_HTTP_PORT, DEFAULT_SYSTEM_MONITOR_PORT


class SubparseAndAppendDualNodeAction(BaseAppendAction):
    MIN_ARGS = 4
    MAX_ARGS = 8

    DEFAULT_EXEC_PORTS = [DEFAULT_GETH_WS_PORT, DEFAULT_SYSTEM_MONITOR_PORT]
    DEFAULT_CONSENSUS_PORTS = [DEFAULT_CONSENSUS_CLI_HTTP_PORT, DEFAULT_SYSTEM_MONITOR_PORT]

    @classmethod
    def read_exec_endpoint(cls, values: List) -> [List, List]:
        if represents_numeric(values[0]):
            return [], []

        res = [values[0]]
        for i in range(1, len(values)):
            if represents_numeric(values[i]):
                res.append(values[i])
            else:
                return res, values[i:]

        return values, []

    @classmethod
    def validate(cls, values: List) -> str:
        msg = validate_num_args(values, cls.MIN_ARGS, cls.MAX_ARGS)
        if msg != "":
            return msg

        exec_endpoint, consensus_endpoint = cls.read_exec_endpoint(values[1:])

        if len(exec_endpoint) < 1:
            return f"Not enough arguments in exec endpoint specification, provided {values}, parsed {exec_endpoint}"

        if len(exec_endpoint) > 3:
            return f"Too many execution endpoint parameters provided {exec_endpoint}"

        if len(consensus_endpoint) < 2:
            return f"Not enough arguments in consensus endpoint specification, provided {values}, " \
                   f"parsed {consensus_endpoint}"

        if len(consensus_endpoint) > 4:
            return f"Too many consensus endpoint parameters provided {consensus_endpoint}"

        msg = validate_endpoint_with_ports(exec_endpoint, 1)
        msg = cls.validate_supported_consensus_clients(consensus_endpoint[1]) if msg == "" else msg
        msg = validate_endpoint_with_ports(consensus_endpoint, 2) if msg == "" else msg

        return msg

    @classmethod
    def update_defaults(cls, values: List) -> List:
        exec_endpoint, consensus_endpoint = cls.read_exec_endpoint(values[1:])

        endpoint0 = update_default_ports(exec_endpoint, cls.DEFAULT_EXEC_PORTS, 1)
        endpoint1 = update_default_ports(consensus_endpoint, cls.DEFAULT_CONSENSUS_PORTS, 2)

        return [values[0]] + endpoint0 + endpoint1

    def parse_me(self, values) -> List:
        msg = self.validate(values)
        if msg != "":
            raise argparse.ArgumentError(self, msg)

        return self.update_defaults(values)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, self.parse_me(values), option_string)
