# This is an example of a combination of the common code that runs the network device
# and the cauldron code running on a single Pico 2 W (or other device with more memory).
# It has a capability to trigger a remote node but the local node trigger has been removed.
# The config.py file must setup the following properties:
#   * BUTTON_PIN
#   * TRIGGER_DURATION
#   * REMOTE_TRIGGER_PIN
import asyncio
from digitalio import Direction, DigitalInOut

from interactive.animation import Flicker
from interactive.audio import AudioController
from interactive.button import ButtonController
from interactive.configuration import BUTTON_PIN, AUDIO_PIN, TRIGGER_DURATION
from interactive.configuration import CAULDRON_PIN, CAULDRON_COLOUR, CAULDRON_BRIGHTNESS, \
    CAULDRON_SPEED
from interactive.configuration import REMOTE_TRIGGER_PIN
from interactive.configuration import TRIGGER_PIN
from interactive.memory import setup_memory_reporting
from interactive.network import NetworkController
from interactive.polyfills.animation import BLACK
from interactive.polyfills.audio import new_mp3_player
from interactive.polyfills.button import new_button
from interactive.polyfills.network import new_server
from interactive.polyfills.pixel import new_pixels
from interactive.runner import Runner
from interactive.scheduler import new_triggered_task, Triggerable

CAULDRON_OFF = 0.0

# Because of memory constraints, we do not use the Interactive class here.
# Rather, we setup everything ourselves to minimise what we pull in.
runner = Runner()

runner.cancel_on_exception = False
runner.restart_on_exception = True
runner.restart_on_completion = False

remote = DigitalInOut(REMOTE_TRIGGER_PIN)
remote.direction = Direction.OUTPUT
remote.value = 1

pixels = new_pixels(CAULDRON_PIN, 30, brightness=CAULDRON_BRIGHTNESS)
animation = Flicker(pixels, speed=CAULDRON_SPEED, color=CAULDRON_COLOUR)

audio_controller = AudioController(new_mp3_player(AUDIO_PIN, "interactive/mp3.mp3"))
audio_controller.register(runner)


async def start_display() -> None:
    remote.value = 0
    await asyncio.sleep(0.05)
    remote.value = 1

    pixels.fill(CAULDRON_COLOUR)
    pixels.brightness = CAULDRON_BRIGHTNESS
    pixels.show()

    audio_controller.queue("bubbling.mp3")


async def run_display() -> None:
    animation.animate()


async def stop_display() -> None:
    pixels.fill(BLACK)
    pixels.brightness = CAULDRON_OFF
    pixels.show()

    audio_controller.stop()


triggerable = Triggerable()

trigger_loop = new_triggered_task(
    triggerable,
    duration=TRIGGER_DURATION,
    start=start_display,
    run=run_display,
    stop=stop_display)
runner.add_task(trigger_loop)


async def button_press() -> None:
    triggerable.triggered = True


button_controller = ButtonController(new_button(BUTTON_PIN))
button_controller.add_single_press_handler(button_press)
button_controller.register(runner)


def network_trigger() -> None:
    triggerable.triggered = True


server = new_server()
network_controller = NetworkController(server, network_trigger)
network_controller.register(runner)

setup_memory_reporting(runner)
runner.run()
