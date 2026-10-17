import cptkip.core.environment as environment

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

LED_PIN_1 = None
LED_PIN_2 = None
LED_PIN_3 = None

if environment.are_pins_available():
    LED_PIN_1 = board.GP1  # Red
    LED_PIN_2 = board.GP5  # Green
    LED_PIN_3 = board.GP6  # Yellow
