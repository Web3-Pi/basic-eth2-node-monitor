from dataclasses import dataclass


@dataclass
class WaitDelayDescr:
    delay_active: float
    delay_degraded: float
