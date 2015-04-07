import os


_curr_dir = os.path.dirname(__file__)


APP_NAME = 'Ketchuporo'


class Files(object):
    BELL_SOUND = os.path.join(_curr_dir, 'lib', 'audio', 'bell.wav')
    KV = os.path.join(_curr_dir, 'views.kv')
    SETTINGS = os.path.join(_curr_dir, 'settings.json')
    SETTINGS_DEFAULT = os.path.join(_curr_dir, 'settings_default.json')
