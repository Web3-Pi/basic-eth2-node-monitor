from __future__ import annotations

from app.appdescr.applicationdescriptor import ApplicationDescriptor
from app.helpers.argshelpers import descriptor_from_args
from app.inputargs.parser import parse_app_args
from app.services.appstatsservice import AppStatsService
from app.services.databaseservice import DatabaseService
from app.services.introservice import IntroService
from app.services.nodesamplingservice import NodeSamplingService


class Application:

    def __init__(self, app_descr: ApplicationDescriptor,
                 database_service: DatabaseService, node_sampling_service: NodeSamplingService) -> None:
        self.app_descr = app_descr

        self.database_service = database_service
        self.node_sampling_service = node_sampling_service
        self.app_stats_service = AppStatsService()

    def print_intro(self) -> None:
        IntroService.print_intro(self.app_descr)

    def run_forever(self) -> None:
        self.print_intro()

        print("Application: entering main loop")

        self.database_service.start()
        self.node_sampling_service.start()
        self.app_stats_service.start()

        print()

        while True:
            node_sample = self.node_sampling_service.wait_for_sample()
            num_db_entries = self.database_service.write_sample(node_sample)

            self.app_stats_service.on_next_sample(num_db_entries)
            self.app_stats_service.print_status()

    def shutdown(self) -> None:
        self.node_sampling_service.shutdown()
        self.database_service.shutdown()

    @classmethod
    def create_from_arguments(cls, args=None) -> Application | None:
        app_descr = descriptor_from_args(parse_app_args(args))

        print("Application: initializing database connection")
        db_service = DatabaseService.create(app_descr.database)
        if db_service is None:
            print("Application: Initialization failed")
            return None

        print("Application: initializing endpoints samplers")
        ns_service = NodeSamplingService.create(app_descr)
        if ns_service is None:
            print("Application: Initialization failed")
            db_service.shutdown()
            return None

        return Application(app_descr, db_service, ns_service)
