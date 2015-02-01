from kivy import Logger
from kivy.core.audio import SoundLoader

from ketchuporo.const import Files


class _LoadAudio(object):
    def __init__(self):
        self.bell = SoundLoader.load(Files.BELL_SOUND)
        Logger.debug('Sound {} loaded'.format(self.bell.source))


Audio = _LoadAudio()
