from datetime import timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


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
    button = None

    def __init__(self):
        super(TimerWidget, self).__init__()
        self.model.timer_label = str(self.timer)

    def start_pomodoro(self, *_):
        self.model.pomodoros_counter += 1
        self.timer = Timer(seconds=5)
        self.model.timer_label = str(self.timer)
        try:
            self.remove_widget(self.button)
        except AttributeError:
            pass
        Clock.schedule_interval(self.pomodoro_timer, 1)

    def start_short_break(self, _):
        self.timer = Timer(seconds=3)
        self.model.timer_label = str(self.timer)
        self.remove_widget(self.button)
        Clock.schedule_interval(self.break_timer, 1)

    def start_long_break(self, _):
        self.timer = Timer(seconds=10)
        self.model.timer_label = str(self.timer)
        self.remove_widget(self.button)
        Clock.schedule_interval(self.break_timer, 1)

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
        self.button = Button()
        if self.model.pomodoros_counter % 4:
            self.button.text = 'Start short break'
            self.button.bind(on_release=self.start_short_break)
        else:
            self.button.text = 'Start long break'
            self.button.bind(on_release=self.start_long_break)
        self.add_widget(self.button)

    def break_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.break_stop()
            return False

    def break_stop(self):
        self.model.timer_label = 'Time\'s up!'
        self.button = Button()
        self.button.text = 'Start pomodoro'
        self.button.bind(on_release=self.start_pomodoro)
        self.add_widget(self.button)


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
