import enum


class DeviceSamplerType(enum.Enum):
    EXECUTION_ONLY = 0
    CONSENSUS_ONLY = 1
    FULL = 2
