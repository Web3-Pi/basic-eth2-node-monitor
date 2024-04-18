from typing import List


def update_default_ports(values: List, defaults: List[int], offset: int) -> List:
    for i in range(len(defaults)):
        if len(values) <= i + offset:
            values.append(str(defaults[i]))

    return values
