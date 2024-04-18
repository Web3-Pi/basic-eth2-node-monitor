from typing import List

from app.appdescr.applicationdescriptor import ApplicationDescriptor
from app.appdescr.components.databasedescr import DatabaseDescr
from app.appdescr.components.waitdelaydescr import WaitDelayDescr
from config.conf import LIGHTHOUSE_LETTER, GENERIC_CONSENSUS_CLIENT_LETTER
from core.sampling.samplingunit.descriptors.devicedescriptors import SingleClientDeviceDesc, FullDeviceDesc
from core.sampling.samplingunit.descriptors.nodedescriptor import NodeDescriptor
from core.sampling.samplingunit.descriptors.supportedclients import SupportedClients


def exec_client_device_from_args(args: List) -> SingleClientDeviceDesc:
    assert len(args) == 3
    return SingleClientDeviceDesc(args[0], args[1], args[2], SupportedClients.GETH)


def get_supported_consensus_client(arg: str) -> SupportedClients:
    if arg == LIGHTHOUSE_LETTER or arg == LIGHTHOUSE_LETTER.upper():
        return SupportedClients.LIGHTHOUSE
    else:
        assert arg == GENERIC_CONSENSUS_CLIENT_LETTER or arg == GENERIC_CONSENSUS_CLIENT_LETTER.upper()
        return SupportedClients.GENERIC_CONSENSUS


def consensus_client_device_from_args(args: List) -> SingleClientDeviceDesc:
    assert len(args) == 4
    return SingleClientDeviceDesc(args[0], args[2], args[3], get_supported_consensus_client(args[1]))


def full_device_from_args(args: List) -> FullDeviceDesc:
    assert len(args) == 5
    return FullDeviceDesc(args[0], args[2], args[3], args[4], get_supported_consensus_client(args[1]))


def descriptor_from_args(args) -> ApplicationDescriptor:
    nd = []
    if args.single_device_node is not None:
        for entry in args.single_device_node:
            assert entry[0].endswith('.local')
            nd.append(NodeDescriptor(entry[0].removesuffix('.local'), full_device_from_args(entry)))

    if args.dual_device_node is not None:
        for entry in args.dual_device_node:
            assert len(entry) == 8

            dev_exec = exec_client_device_from_args(entry[1:4])
            dev_consensus = consensus_client_device_from_args(entry[4:])

            nd.append(NodeDescriptor(entry[0], dev_exec, dev_consensus))

    dbd = DatabaseDescr(args.database_host, args.database_port, *args.database_credentials)
    wdd = WaitDelayDescr(args.wait_active, args.wait_degraded)

    return ApplicationDescriptor(nd, dbd, wdd)
