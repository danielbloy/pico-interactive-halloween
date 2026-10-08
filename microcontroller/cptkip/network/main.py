from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from cptkip.zero.audio import create_pwm_queue
from cptkip.zero.led import create_led, stop_animation as stop_led_animation
from cptkip.zero.pixels import create_pixels, stop_animation as stop_pixels_animation
from network import execute

AUDIO_FILE = "examples/lion.mp3"

queue = create_pwm_queue()

led = create_led()
led_animation = Blink(led, speed=0.5, color=(255, 255, 255))

pixels = create_pixels(brightness=0.5)
pixels_animation = Pulse(pixels, speed=0.1, color=(255, 0, 0), period=3)


def run() -> bool:
    queue.update()
    led_animation.animate()
    pixels_animation.animate()
    return True


def trigger():
    pass


execute(trigger, run)

stop_led_animation(led_animation)
stop_pixels_animation(pixels_animation)
queue.deinit()
