import board

BUZZER_PIN = board.GP22

EVENTS = [
    (0.0, ("crows_1.mp3", "crows_2.mp3", "crows_4.mp3")),
    (8.0, ("crows_1.mp3", "crows_2.mp3", "crows_3.mp3", "crows_4.mp3")),
    (16.0, ("crows_1.mp3", "crows_2.mp3", "crows_3.mp3", "crows_4.mp3")),
    (24.0, ("crows_1.mp3", "crows_2.mp3", "crows_3.mp3", "crows_4.mp3")),
    (32.0, ("crows_1.mp3", "crows_2.mp3", "crows_3.mp3", "crows_4.mp3")),
    (40.0, ("crows_1.mp3", "crows_2.mp3", "crows_4.mp3")),
]

REPORT_RAM = False
TRIGGER_DURATION = 45
