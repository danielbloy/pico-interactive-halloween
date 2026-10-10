# Rename this to code.py on the CircuitPython device.
# This code runs a basic single sound and pixel Flicker animation.
import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.zero.audio import create_pwm_queue
from cptkip.zero.pixels import create_pixels

queue = create_pwm_queue()

pixels = create_pixels(brightness=config.PIXELS_BRIGHTNESS)
pixels_animation = Flicker(pixels, speed=config.PIXELS_SPEED, color=config.PIXELS_COLOUR)


def begin_display() -> None:
    queue.queue(config.AUDIO_FILE)
    pixels.brightness = config.PIXELS_BRIGHTNESS
    pixels.show()


def run_display() -> None:
    queue.update()
    pixels_animation.animate()


def end_display() -> None:
    queue.cancel()
    pixels.brightness = 0
    pixels.show()


from network import execute

execute(begin_display, run_display, end_display)
