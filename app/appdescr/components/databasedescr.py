from dataclasses import dataclass


@dataclass
class DatabaseDescr:
    host: str
    port: int

    user: str
    password: str
    database: str
