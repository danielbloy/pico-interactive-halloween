# This is designed to run on a Plasma 2350 (or 2350 W) with a microphone.
# The microphone will be used to control the "brightness" of the flickering
# of the fire effect so as the dragon make more noise, the flames will get
# brighter and vice versa.

import board

from interactive.button import ButtonController
from interactive.log import set_log_level, INFO
from interactive.microphone import MicrophoneController
from interactive.polyfills.animation import BLACK
from interactive.polyfills.button import new_button
from interactive.polyfills.microphone import Microphone
from interactive.polyfills.pixel import new_pixels
from interactive.runner import Runner

BUTTON_PIN = board.BUTTON
PIXELS_PIN = board.GP15

MICROPHONE_PIN = board.A0

set_log_level(INFO)

runner = Runner()

stop = False


async def long_press_handler() -> None:
    global stop
    stop = True


button = new_button(BUTTON_PIN)
button_controller = ButtonController(button)
button_controller.add_long_press_handler(long_press_handler)
button_controller.register(runner)

# Framework for pixels and microphone.
# See this example: https://learn.adafruit.com/easy-neopixel-graphics-with-the-circuitpython-pixel-framebuf-library
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

# Colours are in GRB form
RED = 0x00_FF_00
DARK_ORANGE = 0x5B_FF_00
ORANGE = 0x45_FF_00
BRIGHT_ORANGE = 0xA5_FF_00
YELLOW = 0xFF_FF_00
OFF = 0x000000
BAND_1 = RED
BAND_2 = DARK_ORANGE
BAND_3 = ORANGE
BAND_4 = BRIGHT_ORANGE
BAND_5 = YELLOW

WIDTH = 20
HEIGHT = 20
FRAME_RATE = 5

pixels = new_pixels(PIXELS_PIN, WIDTH * HEIGHT, brightness=0.5)

display = PixelFramebuffer(
    pixels,
    WIDTH,
    HEIGHT,
    orientation=VERTICAL,
    alternating=False,
    rotation=0)

display.fill(OFF)
display.display()

microphone = Microphone(MICROPHONE_PIN)
microphone_controller = MicrophoneController(microphone, frequency=FRAME_RATE)
microphone_controller.register(runner)

SENSITIVITY_FACTOR = 10


def display_sound_as_bar_chart(minimum, maximum, bar_height: int):
    # Just report amplitude along the bottom of the screen to a maximum height.
    display.scroll(-1, 0)

    amplitude = maximum - minimum
    divisor = (microphone.max / bar_height) / SENSITIVITY_FACTOR
    height = min(int(amplitude / divisor), bar_height)

    # Start with default colours for the bar and then blank out those that we don't need.
    colours = [
        BAND_1, BAND_1, BAND_1, BAND_1,
        BAND_2, BAND_2, BAND_2, BAND_2,
        BAND_3, BAND_3, BAND_3, BAND_3,
        BAND_4, BAND_4, BAND_4, BAND_4,
        BAND_5, BAND_5, BAND_5, BAND_5]

    for idx in range(bar_height - height):
        colours[bar_height - idx - 1] = OFF

    for idx, colour in enumerate(colours):
        display.pixel(WIDTH - 1, HEIGHT - 1 - idx, colour)


async def draw_screen(minimum, maximum: int) -> None:
    display_sound_as_bar_chart(minimum, maximum, HEIGHT)
    display.display()


microphone_controller.add_handler(draw_screen)
microphone_controller.start()


async def callback() -> None:
    global stop
    runner.cancel = stop
    if runner.cancel:
        microphone_controller.stop()
        pixels.fill(BLACK)
        pixels.write()


runner.run(callback)
