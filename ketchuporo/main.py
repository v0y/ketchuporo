from datetime import timedelta
from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class Timer(timedelta, object):
    def tick(self):
        seconds = self.seconds - 1
        return Timer(seconds=seconds)


class TimerModel(EventDispatcher):
    label = StringProperty('')

    def __init__(self):
        super(TimerModel, self).__init__()
        self.label = ''


class Ketchuporo(Widget):
    timer_model = TimerModel()
    timer = Timer(minutes=25)

    def __init__(self):
        super(Ketchuporo, self).__init__()
        self.timer_model.label = str(self.timer)
        Clock.schedule_interval(self.timer_run, 1)

    def timer_tick(self):
        self.timer = self.timer.tick()

    def timer_run(self, _):
        self.timer_tick()
        self.timer_model.label = str(self.timer)


class KetchuporoApp(App):
    def build(self):
        return Ketchuporo()

if __name__ == '__main__':
    KetchuporoApp().run()
