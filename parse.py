import typing

valid_keys = {"Acc", "EventAcc", "TotalAcc", "RInt"}

def parse_values(s: str) -> typing.Dict[str, float]:
    values = {}
    groups = s.split(",")
    for group in groups:
        fs = group.split()
        # expects group of key value units
        if len(fs) != 3:
            continue
        key = fs[0]
        if key not in valid_keys:
            continue
        try:
            value = float(fs[1])
        except ValueError:
            continue
        values[key] = value
    return values
