# NOTE: Rename this to config.py on the primary node path microcontroller.
# This code runs on a Pimoroni Tiny 2040
import board

PRIMARY_NODE = True

BUTTON_PIN = board.GP0
AUDIO_PIN = board.GP26

SKULL_PINS = [board.GP1, board.GP4, board.GP6, board.GP5, board.GP3, board.GP2]
SKULL_COLOUR = ORANGE
SKULL_BRIGHTNESS = 1.0
SKULL_SPEED = 0.1

TRIGGER_PIN = board.GP29
TRIGGER_DURATION = 40

REPORT_RAM = False
REPORT_RAM_PERIOD = 10

from interactive.log import CRITICAL

LOG_LEVEL = CRITICAL
