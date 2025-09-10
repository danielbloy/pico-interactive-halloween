# NOTE: Rename this to config.py on the secondary node path microcontroller.
# This code runs on a standard Pico 2040
import board

PRIMARY_NODE = False

BUTTON_PIN = board.GP26
AUDIO_PIN = board.GP22
ULTRASONIC_TRIGGER_PIN = board.GP17
ULTRASONIC_ECHO_PIN = board.GP16

SKULL_PINS = [board.GP5, board.GP7, board.GP9, board.GP10, board.GP8, board.GP6]
SKULL_COLOUR = ORANGE
SKULL_BRIGHTNESS = 1.0
SKULL_SPEED = 0.1

TRIGGER_PIN = board.GP0
TRIGGER_DURATION = 40

REPORT_RAM = False
REPORT_RAM_PERIOD = 10

from interactive.log import CRITICAL

LOG_LEVEL = CRITICAL
