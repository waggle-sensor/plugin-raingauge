import typing
import logging

logger = logging.getLogger(__name__)

valid_keys = {"Acc", "EventAcc", "TotalAcc", "RInt"}

unit_scale = {
    "mm": 1.0,
    "in": 25.4,
    "mmph": 1.0,
    "iph": 25.4,
}


def parse_values(s: str) -> typing.Dict[str, float]:
    """Returns the sensor values converted to metric units."""
    values = {}
    # line format looks like:
    # metric units:
    # Acc  0.00 mm, EventAcc  0.00 mm, TotalAcc  1.11 mm, RInt  0.00 mmph
    # imperial units:
    # Acc 0.000 in, EventAcc 0.000 in, TotalAcc 0.000 in, RInt 0.000 iph

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

        try:
            scale_factor = unit_scale[fs[2]]
        except KeyError:
            logger.warning("invalid unit %r", fs[2])
            continue

        # sensor precision is 2 decimal units
        values[key] = round(value * scale_factor, 2)

    return values
