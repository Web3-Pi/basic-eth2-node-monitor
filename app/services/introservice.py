import json

from app.appdescr.applicationdescriptor import ApplicationDescriptor
from core.sampling.readers.impl.http_reader import HTTPReader
from core.sampling.samplingunit.descriptors.devicedescriptors import SingleClientDeviceDesc, FullDeviceDesc
from core.sampling.samplingunit.descriptors.supportedclients import SupportedClients
from util.strconverions import as_websocket_addr, as_http_addr


class IntroService:

    @classmethod
    def get_consensus_client(cls, dev_descr) -> str:
        if isinstance(dev_descr, SingleClientDeviceDesc):
            port = dev_descr.client_port
        else:
            assert isinstance(dev_descr, FullDeviceDesc)
            port = dev_descr.consensus_client_port

        res = HTTPReader(as_http_addr(dev_descr.host, port)).query_data('/eth/v1/node/version')
        if res is not None:
            return json.loads(res.content.decode("utf-8"))["data"]["version"]
        else:
            "unknown consensus client"

    @classmethod
    def consensus_api_descr(cls, cli: SupportedClients) -> str:
        assert cli != SupportedClients.GETH
        d = {
            SupportedClients.LIGHTHOUSE: "Lighthouse Non-Standard API",
            SupportedClients.GENERIC_CONSENSUS: "Eth Beacon Node API"
        }

        return d[cli]

    @classmethod
    def print_intro(cls, app_descr: ApplicationDescriptor) -> None:
        print("Starting monitoring duties")

        print(f"  Database endpoint: {as_http_addr(app_descr.database.host, app_descr.database.port)}, using database: "
              f"{app_descr.database.database}")

        print(f"  Sampling delays")
        print(f"    Active node sampling delay:   {app_descr.wait_delay.delay_active} seconds")
        print(f"    Degraded node sampling delay: {app_descr.wait_delay.delay_degraded} seconds")

        print(f"  Monitoring {app_descr.num_nodes()} node{'s' if app_descr.num_nodes() != 1 else ''}")
        print(f"    Dual device nodes number:   {app_descr.num_dual_device_nodes()}")
        print(f"    Single device nodes number: {app_descr.num_single_device_nodes()}")

        i = 1

        if app_descr.num_dual_device_nodes() > 0:
            print(f"  Dual device nodes:")

            for node in app_descr.dual_device_nodes():
                exec_dev = node.get_execution_device_descriptor()
                cons_dev = node.get_consensus_device_descriptor()

                print(f"  {i:2}. Node name: {node.name}")
                print(f"      Execution device: {exec_dev.host}, client: "
                      f"{SupportedClients.str_repr(exec_dev.supported_client)}"
                      f", endpoints: (execution: {as_websocket_addr(exec_dev.host, exec_dev.client_port)}, monitoring: "
                      f"{as_http_addr(exec_dev.host, exec_dev.system_monitor_port)})")
                print(f"      Consensus device: {cons_dev.host}, client: {cls.get_consensus_client(cons_dev)}, "
                      f"endpoints: (consensus: {as_http_addr(cons_dev.host, cons_dev.client_port)}, monitoring: "
                      f"{as_http_addr(cons_dev.host, cons_dev.system_monitor_port)}), "
                      f"sampling with: {cls.consensus_api_descr(cons_dev.supported_client)}")
                i += 1

        i = 1
        if app_descr.num_single_device_nodes() > 0:
            print(f"  Single device nodes:")

            for node in app_descr.single_device_nodes():
                full_dev = node.get_full_device_descriptor()

                print(f"  {i:2}. Node name: {node.name}, device: {full_dev.host}, monitoring endpoint "
                      f"{as_http_addr(full_dev.host, full_dev.system_monitor_port)}")
                print(f"      Execution client: {SupportedClients.str_repr(SupportedClients.GETH)}, "
                      f"endpoint: {as_websocket_addr(full_dev.host, full_dev.exec_client_port)}")
                print(f"      Consensus client: {cls.get_consensus_client(full_dev)}, endpoint: "
                      f"{as_http_addr(full_dev.host, full_dev.consensus_client_port)}, "
                      f"sampling with: {cls.consensus_api_descr(full_dev.consensus_client)}")

                i += 1

        print()
