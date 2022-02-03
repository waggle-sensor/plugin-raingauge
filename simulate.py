import argparse
import logging
from main import start_publishing
from waggle.plugin import Plugin
from random import uniform


class MockRaingauge:

    def __init__(self):
        self.resp = []
    
    def write(self, b):
        cmd = b.strip().lower()
        if cmd == b"p":
            self.resp.append(b"p\n")
        elif cmd == b"h":
            self.resp.append(b"h\n")
        elif cmd == b"m":
            self.resp.append(b"m\n")
        elif cmd == b"r":
            self.resp.append(f"Acc  {uniform(0, 2):.2f} mm, EventAcc  {uniform(0, 2):.2f} mm, TotalAcc  {uniform(0, 2):.2f} mm, RInt  {uniform(0, 2):.2f} mmph\n".encode())
        return len(b)

    def readline(self):
        if len(self.resp) == 0:
            return b""
        b = self.resp[0]
        self.resp.pop(0)
        return b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    parser.add_argument("--node-publish-interval", default=1.0, type=float, help="interval to publish data to node")
    parser.add_argument("--beehive-publish-interval", default=30.0, type=float, help="interval to publish data to beehive")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    with Plugin() as plugin:
        start_publishing(args, plugin, MockRaingauge())


if __name__ == "__main__":
    main()
