from datetime import timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class Timer(timedelta, object):
    def tick(self):
        seconds = self.seconds - 1
        if seconds == 0:
            return False
        else:
            return Timer(seconds=seconds)


class TimerModel(EventDispatcher):
    label = StringProperty('')

    def __init__(self):
        super(TimerModel, self).__init__()
        self.label = ''


class Ketchuporo(Widget):
    timer_model = TimerModel()
    timer = Timer(seconds=5)

    def __init__(self):
        super(Ketchuporo, self).__init__()
        self.timer_model.label = str(self.timer)
        self.start_pomodoro()

    def start_pomodoro(self):
        self.timer = Timer(seconds=5)
        Clock.schedule_interval(self.pomodoro_timer, 1)

    def start_short_break(self):
        self.timer = Timer(seconds=3)
        Clock.schedule_interval(self.short_break_timer, 1)

    def timer_tick(self):
        self.timer = self.timer.tick()
        self.timer_model.label = str(self.timer)

    def pomodoro_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.pomodoro_stop()
            return False

    def pomodoro_stop(self):
        self.timer_model.label = 'Time\'s up!'
        self.start_short_break()

    def short_break_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.short_break_stop()
            return False

    def short_break_stop(self):
        self.timer_model.label = 'Time\'s up!'
        self.start_pomodoro()


class KetchuporoApp(App):
    def build(self):
        return Ketchuporo()


if __name__ == '__main__':
    KetchuporoApp().run()
