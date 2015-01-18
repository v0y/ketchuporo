from datetime import timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class Timer(timedelta, object):
    def tick(self):
        seconds = self.seconds - 1
        if seconds == 0:
            return False
        else:
            return Timer(seconds=seconds)


class KetchuporoModel(EventDispatcher):
    timer_label = StringProperty('')
    pomodoros_counter = NumericProperty(0)

    def __init__(self):
        super(KetchuporoModel, self).__init__()
        self.timer_label = ''


class WelcomeWidget(BoxLayout):
    def __init__(self, layout):
        super(WelcomeWidget, self).__init__()
        self.layout = layout

    def start(self):
        self.layout.start()


class TimerWidget(BoxLayout):
    model = KetchuporoModel()
    timer = Timer(seconds=5)

    def __init__(self):
        super(TimerWidget, self).__init__()
        self.model.timer_label = str(self.timer)

    def start_pomodoro(self):
        self.model.pomodoros_counter += 1
        self.timer = Timer(seconds=5)
        Clock.schedule_interval(self.pomodoro_timer, 1)

    def start_short_break(self):
        self.timer = Timer(seconds=3)
        Clock.schedule_interval(self.short_break_timer, 1)

    def start_long_break(self):
        self.timer = Timer(seconds=10)
        Clock.schedule_interval(self.long_break_timer, 1)

    def timer_tick(self):
        self.timer = self.timer.tick()
        self.model.timer_label = str(self.timer)

    def pomodoro_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.pomodoro_stop()
            return False

    def pomodoro_stop(self):
        self.model.timer_label = 'Time\'s up!'
        if self.model.pomodoros_counter % 4:
            self.start_short_break()
        else:
            self.start_long_break()

    def short_break_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.short_break_stop()
            return False

    def short_break_stop(self):
        self.model.timer_label = 'Time\'s up!'
        self.start_pomodoro()

    def long_break_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.long_break_stop()
            return False

    def long_break_stop(self):
        self.model.timer_label = 'Time\'s up!'
        self.start_pomodoro()


class KetchuporoLayout(BoxLayout):
    def __init__(self):
        super(KetchuporoLayout, self).__init__()
        self.welcome_widget = WelcomeWidget(self)
        self.timer_widget = TimerWidget()
        self.add_widget(self.welcome_widget)

    def start(self):
        self.remove_widget(self.welcome_widget)
        self.add_widget(self.timer_widget)
        self.timer_widget.start_pomodoro()



class KetchuporoApp(App):
    def build(self):
        return KetchuporoLayout()


if __name__ == '__main__':
    KetchuporoApp().run()
