import datetime


class AppStatsService:

    def __init__(self):
        self.started_at = datetime.datetime.now()
        self.num_samples = 0
        self.num_db_entries = 0

    @classmethod
    def remove_microseconds(cls, dt: datetime.timedelta) -> datetime.timedelta:
        return dt - datetime.timedelta(microseconds=dt.microseconds)

    def print_status(self) -> None:
        started_at = self.started_at.strftime("%d-%m-%Y, %H:%M:%S")
        duration = self.remove_microseconds(datetime.datetime.now() - self.started_at)

        print(f"\rStart time: {started_at}; uptime: {duration} | "
              f"Node samples read: {self.num_samples}, database entries written: {self.num_db_entries}", end="")

    def on_next_sample(self, num_db_entries: int) -> None:
        self.num_samples += 1
        self.num_db_entries += num_db_entries

    def start(self) -> None:
        self.started_at = datetime.datetime.now()

    def shutdown(self) -> None:
        pass
