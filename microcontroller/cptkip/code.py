###################################
# D E M O    D E V I C E    C O D E
###################################
import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.zero.audio import create_pwm_queue
from cptkip.zero.pixels import create_pixels, stop_animation as stop_pixels_animation

AUDIO_FILE = "bubbling.mp3"
queue = create_pwm_queue()

pixels = create_pixels(brightness=config.PIXELS_BRIGHTNESS)
pixels_animation = Flicker(pixels, speed=config.PIXELS_SPEED, color=config.PIXELS_COLOUR)


def begin_display() -> None:
    queue.queue(AUDIO_FILE)
    pixels.fill(config.PIXELS_COLOUR)
    pixels.brightness = config.PIXELS_BRIGHTNESS
    pixels.show()


def run_display() -> None:
    queue.update()
    pixels_animation.animate()


def end_display() -> None:
    queue.cancel()
    stop_pixels_animation(pixels_animation)


########################
# C O M M O N    C O D E
########################
from network import execute

execute(begin_display, run_display, end_display)
