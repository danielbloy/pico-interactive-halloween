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
            {'time': 0, 'file': '../../audio/dragon/dragon-1.mp3'}
        ]
    },
    {
        'weight': 1,
        'audios': [
            {'time': 0, 'file': '../../audio/dragon/dragon-2.mp3'}
        ]
    },
    {
        'weight': 1,
        'audios': [
            {'time': 0, 'file': '../../audio/dragon/dragon-3.mp3'}
        ]
    },
    {
        'weight': 1,
        'audios': [
            {'time': 0, 'file': '../../audio/dragon/dragon-4.mp3'}
        ]
    },
    {
        'weight': 1,
        'audios': [
            {'time': 0, 'file': '../../audio/dragon/dragon-5.mp3'}
        ]
    },
]

from interactive.log import INFO

LOG_LEVEL = INFO
