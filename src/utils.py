def multiples_between(start, end, mult):
    first_interval = mult - (start % mult)
    current = start + first_interval

    while current <= end:
        yield current
        current += mult


def try_float(f):
    try:
        return float(f)
    except ValueError:
        return None
