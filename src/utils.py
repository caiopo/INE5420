def multiples_between(start, end, mult):
    first_interval = mult - (start % mult)
    current = start + first_interval

    while current <= end:
        yield current
        current += mult


print(list(multiples_between(100, 50, 321)))
