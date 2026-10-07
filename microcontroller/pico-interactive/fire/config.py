# This code runs on a standard Pico 2W, using the 2026 Mark 3 node.
import board

from interactive.polyfills.animation import ORANGE

AUDIO_PIN = board.GP26

FIRE_PIN = board.GP28
FIRE_COLOUR = ORANGE
FIRE_BRIGHTNESS = 1.0
FIRE_SPEED = 0.1

TRIGGER_PIN = board.GP9
TRIGGER_DURATION = 40

REPORT_RAM = False
REPORT_RAM_PERIOD = 10

from interactive.log import CRITICAL

LOG_LEVEL = CRITICAL
