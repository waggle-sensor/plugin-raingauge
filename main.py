import argparse
import serial
import time
import parse
import logging
import waggle.plugin as plugin


def validate_response(dev: serial.Serial, test) -> str:
    """
    Validate the response is not empty and matches `test` criteria.
    Returns response on success, `None` on failure.
    """
    # try for up-to 3 seconds to get a response
    wait = 0.1
    loops = 30
    for i in range(loops):
        data = dev.readline()
        logging.debug(f"read data [{data}]")
        if data == b"":
            time.sleep(wait)
            break
        try:
            line = data.decode()
        except UnicodeDecodeError:
            time.sleep(wait)
            continue
        if not test(line):
            time.sleep(wait)
            continue
        # all tests passed, return response
        return line
    return None


def request_sample(dev: serial.Serial) -> str:
    """
    Attempt forever to send the read command until we get a response
    Return command response on success.
    """
    while True:
        logging.debug("write read command")
        dev.write(b"r\n")
        line = validate_response(dev, lambda x: x.startswith("Acc"))
        if line:
            return line


publish_names = {
    "Acc": "env.raingauge.acc",
    "EventAcc": "env.raingauge.event_acc",
    "TotalAcc": "env.raingauge.total_acc",
    "RInt": "env.raingauge.rint",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    parser.add_argument("--device", default="/dev/ttyUSB0", help="serial device to use")
    parser.add_argument("--rate", default=30.0, type=float, help="sampling rate")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    plugin.init()

    with serial.Serial(args.device, baudrate=9600, timeout=3.0) as dev:
        while True:
            time.sleep(args.rate)

            logging.info("requesting sample")
            sample = request_sample(dev)
            values = parse.parse_values(sample)
            logging.info("read values %s", values)

            # publish each value in sample
            for key, name in publish_names.items():
                try:
                    value = values[key]
                except KeyError:
                    continue
                plugin.publish(name, value=value)


if __name__ == "__main__":
    main()
