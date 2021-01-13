import typing

valid_keys = {"Acc", "EventAcc", "TotalAcc", "RInt"}

def parse_values(s: str) -> typing.Dict[str, float]:
    values = {}
    # line format looks like:
    # Acc  0.00 mm, EventAcc  0.00 mm, TotalAcc  1.11 mm, RInt  0.00 mmph
    
    # split into individual key+value+units groups
    groups = s.split(",")

    for group in groups:
        fs = group.split()

        # skip groups not of the form key+value+units
        if len(fs) != 3:
            continue

        key = fs[0]
        if key not in valid_keys:
            continue

        # values *must* be numeric
        try:
            value = float(fs[1])
        except ValueError:
            continue

        values[key] = value

    return values
