import argparse

from app.inputargs.customactions.dualnodeaction import SubparseAndAppendDualNodeAction
from app.inputargs.customactions.singlenodeaction import SubparseAndAppendSingleNodeAction
from config.conf import DEFAULT_INFLUX_DB_PORT, DEFAULT_INFLUX_USER, DEFAULT_INFLUX_PASS, DEFAULT_INFLUX_DATABASE, \
    DEFAULT_DELAY_BOTH_ACTIVE, DEFAULT_DELAY_DEGRADED, APP_EPILOG, APP_DESCRIPTION, GENERIC_CONSENSUS_CLIENT_LETTER, \
    LIGHTHOUSE_LETTER


def parse_app_args(args=None):
    parser = argparse.ArgumentParser(epilog=APP_EPILOG, description=APP_DESCRIPTION,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    ll = LIGHTHOUSE_LETTER
    gcl = GENERIC_CONSENSUS_CLIENT_LETTER

    nodes_group = parser.add_argument_group('Nodes', 'Ethereum nodes list')
    nodes_group.add_argument(
        "-sn",
        "--single_device_node",
        nargs="+",
        metavar=(f"endpoint consensus_type({ll}|{gcl})", "exec_port consensus_port sys_port"),
        help=f"Single-Device Ethereum node. Consensus clients: Lighthouse[{ll}], GenericConsensusClient[{gcl}] "
             f"(-sn can be used arbitrary number of times)",
        action=SubparseAndAppendSingleNodeAction
    )
    nodes_group.add_argument(
        "-dn",
        "--dual_device_node",
        nargs="+",
        metavar=(f"node_name endpoint_exec [exec_port exec_sys_port] endpoint_consensus endpoint "
                 f"consensus_type({ll}|{gcl}) [consensus_port consensus_sys_port]", ""),
        help=f"Dual-Device Ethereum node Consensus clients: Lighthouse[{ll}], GenericConsensusClient[{gcl}] "
             f"(-dn can be used arbitrary number of times)",
        action=SubparseAndAppendDualNodeAction
    )

    database_group = parser.add_argument_group('Database', 'Database parameters')
    database_group.add_argument(
        "-db",
        "--database_host",
        type=str,
        required=True,
        metavar="HOST",
        help="InfluxDB host",
    )
    database_group.add_argument(
        "-dbp",
        "--database_port",
        type=int,
        default=DEFAULT_INFLUX_DB_PORT,
        metavar="PORT",
        help="InfluxDB port",
    )
    database_group.add_argument(
        "-dbc",
        "--database_credentials",
        nargs=3,
        metavar=("USER", "PASS", "DATABASE"),
        default=[DEFAULT_INFLUX_USER, DEFAULT_INFLUX_PASS, DEFAULT_INFLUX_DATABASE],
        help="InfluxDB login credentials and a database name to use",
        type=str
    )

    delays_group = parser.add_argument_group('Wait', 'Wait duration between samples')
    delays_group.add_argument(
        "-wa",
        "--wait_active",
        metavar="SECS",
        help="Time between two samples when Ethereum node is active",
        default=DEFAULT_DELAY_BOTH_ACTIVE,
        type=float
    )
    delays_group.add_argument(
        "-wd",
        "--wait_degraded",
        metavar="SECS",
        help="Time between two samples when not all clients are active (including inactive state)",
        default=DEFAULT_DELAY_DEGRADED,
        type=float
    )

    res = parser.parse_args(args)

    if res.single_device_node is None and res.dual_device_node is None:
        parser.error("No nodes to monitor provided in input arguments")

    return res
