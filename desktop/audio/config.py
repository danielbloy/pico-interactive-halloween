TRIGGER_DURATION = 10

# When set to a value, TRIGGER_AUDIO overrides TRIGGER_AUDIOS and
# allows for a simple method to simply display a single video. To
# use the more powerful TRIGGER_AUDIOS, set TRIGGER_AUDIO to None.
# TRIGGER_AUDIO = "../../audio/witch-thumbs.mp3"
TRIGGER_AUDIO = None

TRIGGER_AUDIOS = [
    {
        'weight': 1,
        'audios': [
            {'time': 4, 'file': '../../audio/dragon.mp3'}
        ]
    },
    {
        'weight': 3,
        'audios': [
            {'time': 0.5, 'file': '../../audio/witch-thumbs.mp3'},
            {'time': 7, 'file': '../../audio/bubbling.mp3'}
        ]
    },
    {
        'weight': 1,
        'audios': [
            {'time': 1.4, 'file': '../../audio/witch-laugh.mp3'},
            {'time': 7, 'file': '../../audio/lion.mp3'}
        ]
    },
    {
        'weight': 1,
        'audios': [
            {'time': 0, 'file': '../../audio/lion.mp3'},
        ]
    }
]

from interactive.log import INFO

LOG_LEVEL = INFO
