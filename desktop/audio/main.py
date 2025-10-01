# This is designed to run on a desktop computer and play of set of audio clips.
# Each time the application is triggered, the set of audio clips to play will be randomly
# selected from the configuration data based on weight. A audio set consists of a list of
# sound files to play and the timing intervals to play them at.
#
# A simplified TRIGGER_AUDIO value dispenses with the more complex TRIGGER_AUDIO and
# simply overwrites it so that only a single sound clip is played.
#
import random

import pygame

from config import TRIGGER_AUDIO
from interactive.configuration import TRIGGER_DURATION, TRIGGER_AUDIOS
from interactive.log import info
from interactive.network import NetworkController
from interactive.polyfills.network import new_server
from interactive.runner import Runner
from interactive.scheduler import new_triggered_task, Triggerable, TriggerTimedEvents

if __name__ == '__main__':

    pygame.init()
    pygame.mixer.init()

    # If a TRIGGER_AUDIO is ever specified then it overwrites TRIGGER_AUDIOS.
    # This is also a useful reference for the expected data structure.
    if TRIGGER_AUDIO:
        TRIGGER_AUDIOS = [
            {
                'weight': 1,
                'audios': [
                    {'time': 0, 'file': TRIGGER_AUDIO}
                ]
            }
        ]

    # For each entry in TRIGGER_AUDIOS, this list will contain its index the number
    # of times weight is specified. This allows us to randomly select a audio based
    # on a weighting.
    audio_selector = []
    for idx, audio_set_details in enumerate(TRIGGER_AUDIOS):
        for i in range(audio_set_details['weight']):
            audio_selector.append(idx)

    # The index selected to be played.
    audio_set = []

    trigger_events = TriggerTimedEvents()


    async def start_display() -> None:
        global audio_selector, audio_set
        info("Start display")

        # Randomly select a audio set to play.
        selected_index = audio_selector[random.randint(0, len(audio_selector) - 1)]
        audio_set = TRIGGER_AUDIOS[selected_index]['audios']

        # Add the audio events.
        trigger_events.events.clear()

        for idx, audio in enumerate(audio_set):
            info(f"{idx} - {audio['file']} will play at {audio['time']} seconds")
            trigger_events.add_event(audio['time'], idx)

        trigger_events.start()


    async def run_display() -> None:
        events = trigger_events.run()

        for event in events:
            info(f"Playing audio {event.event} - {audio_set[event.event]['file']}")
            pygame.mixer.music.load(audio_set[event.event]['file'])
            pygame.mixer.music.play()


    async def stop_display() -> None:
        info("Stop display")
        trigger_events.stop()


    runner = Runner()

    runner.cancel_on_exception = False
    runner.restart_on_exception = True
    runner.restart_on_completion = False

    triggerable = Triggerable()

    trigger_loop = new_triggered_task(
        triggerable,
        duration=TRIGGER_DURATION,
        start=start_display,
        run=run_display,
        stop=stop_display)
    runner.add_task(trigger_loop)


    def network_trigger() -> None:
        triggerable.triggered = True


    server = new_server()
    network_controller = NetworkController(server, network_trigger)
    network_controller.register(runner)


    # Adding this task to handle pygame events
    async def pygame_event_loop() -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner.cancel = True


    runner.add_loop_task(pygame_event_loop)

    runner.run()
    pygame.quit()
