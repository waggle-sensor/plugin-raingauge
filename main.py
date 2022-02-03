import argparse
import serial
import parse
import logging
import sched
import time
from waggle.plugin import Plugin


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
            line = data.decode().strip()
        except UnicodeDecodeError:
            time.sleep(wait)
            continue
        if not test(line):
            time.sleep(wait)
            continue
        # all tests passed, return response
        return line
    return None


def set_mode(dev: serial.Serial, mode: str):
    """
    Send the `mode` setting and attempt to verify (echo of `mode`).
    Exception on failure.
    """
    for i in range(5):
        logging.debug(f"writing command[try: {i}] '{mode}'")
        dev.write("{}\n".format(mode).encode())
        if validate_response(dev, lambda x: x == mode.lower()):
            return
    raise Exception(f"Unable to validate command '{mode}'")


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
    # "Acc": "env.raingauge.acc", # NOT PUBLISHING
    "EventAcc": "env.raingauge.event_acc",
    "TotalAcc": "env.raingauge.total_acc",
    "RInt": "env.raingauge.rint",
}

# We are not publishing the Acc values for the following reasons:
#
# 1. We believe is is more accurate for users who want accumulation
#    in some interval to take the diff of the first and last TotalAcc.
#
# 2. The scale and meaning of Acc is sampling rate dependent and would
#    require looking at two samples anyway.

def start_publishing(args, plugin, dev):
    """
    start_publishing initializes the raingauge and begins sampling and publishing data
    """
    # initialize the raingauge
    try:
        logging.info("set to polling mode")
        set_mode(dev, "p")
    except:
        pass
    try:
        logging.info("set to high precision")
        set_mode(dev, "h")
    except:
        pass
    try:
        logging.info("set to metric mode")
        set_mode(dev, "m")
    except:
        pass

    sch = sched.scheduler(time.time, time.sleep)

    def sample_and_publish_task(scope, delay):
        sch.enter(delay, 0, sample_and_publish_task, kwargs={
            "scope": scope,
            "delay": delay,
        })

        logging.info("requesting sample for scope %s", scope)
        sample = request_sample(dev)
        values = parse.parse_values(sample)
        logging.info("read values %s", values)

        # publish each value in sample
        for key, name in publish_names.items():
            try:
                value = values[key]
            except KeyError:
                continue
            plugin.publish(name, value=value, scope=scope)

    # setup and run publishing schedule
    if args.node_publish_interval > 0:
        sch.enter(0, 0, sample_and_publish_task, kwargs={
            "scope": "node",
            "delay": args.node_publish_interval,
        })

    if args.beehive_publish_interval > 0:
        sch.enter(0, 0, sample_and_publish_task, kwargs={
            "scope": "beehive",
            "delay": args.beehive_publish_interval,
        })

    sch.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    parser.add_argument("--device", default="/dev/ttyUSB0", help="serial device to use")
    parser.add_argument("--baudrate", default=9600, type=int, help="baudrate to use")
    parser.add_argument("--node-publish-interval", default=1.0, type=float, help="interval to publish data to node (negative values disable node publishing)")
    parser.add_argument("--beehive-publish-interval", default=30.0, type=float, help="interval to publish data to beehive (negative values disable beehive publishing)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    with Plugin() as plugin, serial.Serial(args.device, baudrate=args.baudrate, timeout=3.0) as dev:
        start_publishing(args, plugin, dev)


if __name__ == "__main__":
    main()
