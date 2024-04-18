def represents_int(s: str) -> bool:
    try:
        int(s)
    except ValueError:
        return False

    return True


def represents_float(s: str) -> bool:
    try:
        float(s)
    except ValueError:
        return False

    return True


def represents_numeric(s: str) -> bool:
    return represents_int(s) or represents_float(s)
