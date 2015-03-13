import os


_curr_dir = os.path.dirname(__file__)


class Defaults(object):
    POMODORO_DURATION = 25
    SHORT_BREAK = 5
    LONG_BREAK = 15
    POMODORI_FOR_CYCLE = 4
    BELL_AFTER_POMODORO = True
    BELL_AFTER_BREAK = True


class Files(object):
    BELL_SOUND = os.path.join(_curr_dir, 'lib', 'audio', 'bell.wav')
    KV = os.path.join(_curr_dir, 'views.kv')
    SETTINGS = os.path.join(_curr_dir, 'settings.json')
