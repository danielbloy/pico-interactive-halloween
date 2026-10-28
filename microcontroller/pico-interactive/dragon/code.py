from interactive.audio import AudioController
from interactive.button import ButtonController
from interactive.configuration import AUDIO_PIN, TRIGGER_DURATION, TRIGGER_PIN
from interactive.memory import setup_memory_reporting
from interactive.polyfills.audio import new_mp3_player
from interactive.polyfills.button import new_button
from interactive.runner import Runner
from interactive.scheduler import new_triggered_task, Triggerable, TriggerTimedEvents

# Because of memory constraints when using a Pico W CircuitPython image we do not use the
# Interactive class here. This allows for much easier testing but also keeps the code
# consistent with network_code.py which must use the Pico W CircuitPython image.
# Doing the setup ourselves saves a notable amount of RAM.
runner = Runner()

runner.cancel_on_exception = False
runner.restart_on_exception = True
runner.restart_on_completion = False

audio_controller = AudioController(new_mp3_player(AUDIO_PIN, "interactive/mp3.mp3"))
audio_controller.register(runner)

# The event is the index to enable
trigger_events = TriggerTimedEvents()
trigger_events.add_event(0.0, 0)  # Growl
trigger_events.add_event(5.0, 1)  # Flapping wings - 10 seconds
trigger_events.add_event(15.0, 0)  # Growl
trigger_events.add_event(20.0, 2)  # Roar
trigger_events.add_event(30.0, 1)  # Flapping wings - 10 seconds
trigger_events.add_event(40.0, 0)  # Growl


async def start_display() -> None:
    trigger_events.start()


async def run_display() -> None:
    events = trigger_events.run()

    for event in events:
        import random

        if event.event == 0:
            pick = random.randint(0, 4)
            if pick == 0:
                audio_controller.queue("dragon-growl-1.mp3")
            elif pick == 1:
                audio_controller.queue("dragon-growl-2.mp3")
            elif pick == 2:
                audio_controller.queue("dragon-growl-3.mp3")
            elif pick == 3:
                audio_controller.queue("dragon-growl-4.mp3")
            else:
                audio_controller.queue("dragon-growl-5.mp3")

        elif event.event == 1:
            pick = random.randint(0, 1)
            if pick == 0:
                audio_controller.queue("dragon-flapping-wings-1.mp3")
            else:
                audio_controller.queue("dragon-flapping-wings-2.mp3")

        elif event.event == 2:
            pick = random.randint(0, 3)
            if pick == 0:
                audio_controller.queue("dragon-roar-1.mp3")
            elif pick == 1:
                audio_controller.queue("dragon-roar-2.mp3")
            elif pick == 2:
                audio_controller.queue("dragon-roar-3.mp3")
            else:
                audio_controller.queue("dragon-roar-4.mp3")


async def stop_display() -> None:
    trigger_events.stop()
    audio_controller.stop()


triggerable = Triggerable()

trigger_loop = new_triggered_task(
    triggerable,
    duration=TRIGGER_DURATION,
    start=start_display,
    run=run_display,
    stop=stop_display)
runner.add_task(trigger_loop)


async def button_press() -> None:
    triggerable.triggered = True


trigger_controller = ButtonController(new_button(TRIGGER_PIN))
trigger_controller.add_single_press_handler(button_press)
trigger_controller.register(runner)

setup_memory_reporting(runner)
runner.run()
