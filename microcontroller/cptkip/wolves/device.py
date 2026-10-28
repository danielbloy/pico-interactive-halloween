import board

BUZZER_PIN = board.GP22

EVENTS = [
    (5.0, ("wolves_1.mp3", "wolves_2.mp3")),
    (20.0, ("wolves_3.mp3", "wolves_4.mp3")),
    (35.0, ("wolves_4.mp3", "wolves_5.mp3")),
]

REPORT_RAM = False
TRIGGER_DURATION = 45
