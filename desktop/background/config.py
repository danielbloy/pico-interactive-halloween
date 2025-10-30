# When set to a value, TRIGGER_AUDIO overrides TRIGGER_AUDIOS and
# allows for a simple method to simply display a single video. To
# use the more powerful TRIGGER_AUDIOS, set TRIGGER_AUDIO to None.
# TRIGGER_AUDIO = "../../audio/witch-thumbs.mp3"
TRIGGER_AUDIO = None

TRIGGER_AUDIOS = [
    {
        'weight': 1,
        'file': '../../audio/graveyard/eerie-ambiance-541secs.mp3'
    },
    {
        'weight': 4,
        'file': '../../audio/graveyard/eerie-and-creepy-56secs.mp3'
    },
    {
        'weight': 9,
        'file': '../../audio/graveyard/fountain-and-birds-55-secs.mp3'
    },
    {
        'weight': 1,
        'file': '../../audio/graveyard/haunted-graveyard-189secs.mp3'
    },
    {
        'weight': 1,
        'file': '../../audio/graveyard/message-sound-47secs.mp3'
    },
    {
        'weight': 9,
        'file': '../../audio/graveyard/night-in-graveyard-133secs.mp3'
    },
    {
        'weight': 4,
        'file': '../../audio/graveyard/scary-ambience-47secs.mp3'
    },
    {
        'weight': 4,
        'file': '../../audio/graveyard/strangegong-85secs.mp3'
    },
]

from interactive.log import INFO

LOG_LEVEL = INFO
