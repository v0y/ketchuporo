from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    NumericProperty,
)


class TimerModel(EventDispatcher):
    timer_label = StringProperty('')
    pomodori_counter = NumericProperty(0)
    pomodoro_duration = NumericProperty(25)
    short_break_duration = NumericProperty(5)
    long_break_duration = NumericProperty(15)
    pomodori_for_cycle = NumericProperty(4)
    bell_after_pomodoro = True
    bell_after_break = True

    def __init__(self):
        super(TimerModel, self).__init__()
        self.timer_label = ''
