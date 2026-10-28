import board

BUZZER_PIN = board.GP22

EVENTS = [
    (3.0, ("ghost_1.mp3", "ghost_2.mp3", "ghost_3.mp3", "ghost_4.mp3", "ghost_5.mp3")),
    (12.0, ("ghost_1.mp3", "ghost_2.mp3", "ghost_3.mp3", "ghost_4.mp3", "ghost_5.mp3")),
    (28.0, ("ghost_1.mp3", "ghost_2.mp3", "ghost_3.mp3", "ghost_4.mp3", "ghost_5.mp3")),
    (38.0, ("ghost_1.mp3", "ghost_2.mp3", "ghost_3.mp3", "ghost_4.mp3", "ghost_5.mp3")),
]

REPORT_RAM = False
TRIGGER_DURATION = 45
