# For nodes that have a Pico 2W, they have enough RAM to be able to run the
# network code and the display code on the same node, rather than using a
# two-microcontroller setup. This is the common code required for the
# networking part.
#
# There is a sample start_display() function that triggers a remote node but
# If no remote is needed for the node, then it can be deleted, along with the
# REMOTE_TRIGGER_PIN.

import asyncio

from digitalio import Direction, DigitalInOut

from interactive.configuration import REMOTE_TRIGGER_PIN
from interactive.network import NetworkController
from interactive.polyfills.network import new_server

remote = DigitalInOut(REMOTE_TRIGGER_PIN)
remote.direction = Direction.OUTPUT
remote.value = 1


async def start_display() -> None:
    remote.value = 0
    await asyncio.sleep(0.05)
    remote.value = 1
    # TODO: Remove this is there is no remote to trigger


# TODO: Normal code goes in here.


def network_trigger() -> None:
    triggerable.triggered = True


server = new_server()
network_controller = NetworkController(server, network_trigger)
network_controller.register(runner)
