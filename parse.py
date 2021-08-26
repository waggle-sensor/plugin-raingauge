import typing
import logging

logger = logging.getLogger(__name__)

valid_keys = {"Acc", "EventAcc", "TotalAcc", "RInt"}
valid_units = {"mm", "mmph"}


def parse_values(s: str) -> typing.Dict[str, float]:
    """Parses the sensor output only accepting metric units."""
    values = {}
    # line format looks like:
    # metric units:
    # Acc  0.00 mm, EventAcc  0.00 mm, TotalAcc  1.11 mm, RInt  0.00 mmph
    # imperial units (skipped):
    # Acc 0.000 in, EventAcc 0.000 in, TotalAcc 0.000 in, RInt 0.000 iph

    # split into individual key+value+units groups
    groups = s.split(",")

    for group in groups:
        fs = group.split()

        # skip groups not of the form key+value+units (ex "Acc 0.00 mm")
        if len(fs) != 3:
            logger.warning(f"data format error [{fs}], skipping")
            continue

        key = fs[0]
        if key not in valid_keys:
            logger.warning(f"unaccepted key [{fs[0]}], skipping value [{fs[1]}]")
            continue

        # only accept
        if fs[2] not in valid_units:
            logger.warning(f"unaccepted unit [{fs[2]}] skipping value [{fs[1]}]")
            continue

        # values *must* be numeric
        try:
            value = float(fs[1])
        except ValueError:
            logger.warning(f"exception parsing value [{fs[1]}], skipping value")
            continue

        values[key] = value

    return values
