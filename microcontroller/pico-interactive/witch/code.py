# This is a combined Pico 2 W variant of this code where the network and display
# code is all contained in a single file.
from interactive.audio import AudioController
from interactive.button import ButtonController
from interactive.configuration import AUDIO_PIN, TRIGGER_PIN, TRIGGER_DURATION
from interactive.memory import setup_memory_reporting
from interactive.network import NetworkController
from interactive.polyfills.audio import new_mp3_player
from interactive.polyfills.button import new_button
from interactive.polyfills.network import new_server
from interactive.runner import Runner
from interactive.scheduler import TriggerTimedEvents
from interactive.scheduler import new_triggered_task, Triggerable

CAULDRON_OFF = 0.0

runner = Runner()

runner.cancel_on_exception = False
runner.restart_on_exception = True
runner.restart_on_completion = False

audio_controller = AudioController(new_mp3_player(AUDIO_PIN, "interactive/mp3.mp3"))
audio_controller.register(runner)

# The event is the skull index to enable
trigger_events = TriggerTimedEvents()
trigger_events.add_event(0.0, 0)
trigger_events.add_event(7.0, 2)
trigger_events.add_event(14.0, 3)
trigger_events.add_event(21.0, 4)
trigger_events.add_event(28.0, 1)
trigger_events.add_event(35.0, 0)


async def start_display() -> None:
    trigger_events.start()


async def run_display() -> None:
    events = trigger_events.run()

    for event in events:
        import random
        pick = random.randint(0, 2)

        if event.event == 0:
            audio_controller.queue("witch-laugh.mp3")

        elif event.event == 1:
            audio_controller.queue("witch-thumbs.mp3")

        elif event.event == 2:
            if pick == 0:
                audio_controller.queue("you_look_so_interesting.mp3")
            else:
                audio_controller.queue("aww_you_look_so_good.mp3")

        elif event.event == 3:
            if pick == 0:
                audio_controller.queue("are_you_afraid_my_dear.mp3")
            else:
                audio_controller.queue("are_you_afraid_of_the_dark_my_dear.mp3")

        elif event.event == 4:
            if pick == 0:
                audio_controller.queue("did_you_run_away_from_home.mp3")
            else:
                audio_controller.queue("laugh_i_will_find_you.mp3")


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


def network_trigger() -> None:
    triggerable.triggered = True


server = new_server()
network_controller = NetworkController(server, network_trigger)
network_controller.register(runner)

setup_memory_reporting(runner)
runner.run()
