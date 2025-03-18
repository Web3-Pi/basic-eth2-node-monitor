from dataclasses import dataclass


@dataclass
class DatabaseDescr:
    host: str
    port: int

    user: str
    token: str
    org: str
    bucket: str
