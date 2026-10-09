# Sample main.py file for a Pico W (pr Pico 2 W) that runs a triggered event.

###################################
# D E M O    D E V I C E    C O D E
###################################
# This is the same code that is node specific


# pixels = new_pixels(CAULDRON_PIN, 30, brightness=CAULDRON_BRIGHTNESS)
# animation = Flicker(pixels, speed=CAULDRON_SPEED, color=CAULDRON_COLOUR)

# audio_controller = AudioController(new_mp3_player(AUDIO_PIN, "interactive/mp3.mp3"))
# audio_controller.register(runner)

# led = create_led()
# led_animation = Blink(led, speed=0.5, color=(255, 255, 255))

# pixels = create_pixels(brightness=0.5)
# pixels_animation = Pulse(pixels, speed=0.1, color=(255, 0, 0), period=3)


def begin_display() -> None:
    # pixels.fill(CAULDRON_COLOUR)
    # pixels.brightness = CAULDRON_BRIGHTNESS
    # pixels.show()

    # audio_controller.queue("bubbling.mp3")
    print("start display")


def run_display() -> None:
    # animation.animate()
    # print("run display")
    pass


def end_display() -> None:
    # pixels.fill(BLACK)
    # pixels.brightness = CAULDRON_OFF
    # pixels.show()

    # audio_controller.stop()
    print("stop display")


########################
# C O M M O N    C O D E
########################
# This is the common code for each node
from network import execute

execute(begin_display, run_display, end_display)
