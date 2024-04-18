import humanize


def h(val: int, binary=True) -> str:
    return humanize.naturalsize(val, binary)


def as_http_addr(addr: str, port: int) -> str:
    return f'http://{addr}:{port}'


def as_websocket_addr(addr: str, port: int) -> str:
    return f'ws://{addr}:{port}'
