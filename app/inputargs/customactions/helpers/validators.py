from typing import List

from app.inputargs.customactions.helpers.typetesters import represents_numeric


def validate_num_args(values: List, min_val: int, max_val: int) -> str:
    if len(values) < min_val:
        return f"Min number of arguments is {min_val}, {len(values)} provided"

    if len(values) > max_val:
        return f"Max number of arguments is {max_val}, {len(values)} provided"

    return ""


def validate_preamble_spec(preamble: List) -> str:
    for arg in preamble:
        if represents_numeric(arg):
            return f"Host/Client spec arg must be a string, not a numerical value {arg}"

    return ""


def validate_ports(ports_list: List) -> str:
    for port in ports_list:
        try:
            if not 1024 < int(port) < 65535:
                return f"Port argument must be bigger than 1024 and less than 65536, {port} provided"
        except ValueError:
            return f"Port argument must be an int, provided type({port})=={type(port)}"

    return ""


def validate_endpoint_with_ports(values: List, preamble_len: int) -> str:
    msg = validate_preamble_spec(values[:preamble_len])
    if msg != "":
        return msg

    return validate_ports(values[preamble_len:])

