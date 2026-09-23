# This python module plays audio on a loop for background atmosphere.
import random
import time

from pygame import mixer

from config import TRIGGER_AUDIO
from interactive.configuration import TRIGGER_AUDIOS
from interactive.log import info

if __name__ == '__main__':

    # If a TRIGGER_AUDIO is ever specified then it overwrites TRIGGER_AUDIOS.
    # This is also a useful reference for the expected data structure.
    if TRIGGER_AUDIO:
        TRIGGER_AUDIOS = [
            {
                'weight': 1,
                'file': TRIGGER_AUDIO,
            }
        ]

    # For each entry in TRIGGER_AUDIOS, this list will contain the number
    # of times weight is specified. This allows us to randomly select a
    # audio based on a weighting.
    audio_selector = []
    for idx, audio_set_details in enumerate(TRIGGER_AUDIOS):
        for i in range(audio_set_details['weight']):
            audio_selector.append(idx)

    # The index selected to be played.
    audio_set = []

    mixer.init()
    while True:
        # Randomly select a audio set to play.
        index = audio_selector[random.randint(0, len(audio_selector) - 1)]
        file = TRIGGER_AUDIOS[index]['file']
        info(f"{index} - {file} will play")
        mixer.music.load(file)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(0.1)
