import os
import requests
import signal
import sys
from dataclasses import dataclass, field
from pathlib import Path
from threading import Event


USERNAME = os.environ.get("USERNAME", "")
PASSWORD = os.environ.get("PASSWORD", "")
HOST = os.environ.get("HOST", "")

SAVE_FILE = Path("/data/current_ip.txt")


@dataclass
class SignalState:
    exit_event: Event = field(default_factory=Event)

    def on_sigterm(self, signal_number, stack_frame):
        self.exit_event.set()

    def add_handler(self):
        signal.signal(signal.SIGTERM, self.on_sigterm)


state = SignalState()
state.add_handler()


def main():
    if not USERNAME:
        print("missing $USERNAME", file=sys.stderr)
        return 1

    if not PASSWORD:
        print("missing $PASSWORD", file=sys.stderr)
        return 1

    if not HOST:
        print("missing $HOST", file=sys.stderr)
        return 1

    # Load previous ip from file
    previous_ip = SAVE_FILE.read_text().strip()

    # Main loop
    while not state.exit_event.is_set():
        # Get current ip
        current_ip = requests.get("https://domains.google.com/checkip").content.strip().decode()

        # Update DNS if necessary
        if current_ip != previous_ip:
            print(f"Updating IP for {HOST}: {previous_ip} -> {current_ip}")
            response = requests.post(f"https://{USERNAME}:{PASSWORD}@domains.google.com/nic/update?hostname={HOST}")
            print("Google Dynamic DNS Response:", response.status_code, response.content.decode())

        # Save current ip to previous ip
        previous_ip = current_ip
        SAVE_FILE.write_text(current_ip)

        # Wait 5 minutes, or until a signal comes in
        state.exit_event.wait(300)

    return 0


if __name__ == '__main__':
    sys.exit(main())
