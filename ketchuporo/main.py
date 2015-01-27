from datetime import timedelta

from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import (
    NumericProperty,
    StringProperty,
)
from kivy.uix.screenmanager import (
    Screen,
    ScreenManager,
)


# TODO: why kv file doesn't load automatically?
kv_file = open('ketchuporo.kv')
Builder.load_string(kv_file.read())


class Timer(timedelta, object):
    def tick(self):
        seconds = self.seconds - 1
        return Timer(seconds=seconds)


class DynamicLabel(EventDispatcher):
    label = StringProperty('')

    def __init__(self):
        super(DynamicLabel, self).__init__()
        self.label = ''


class TimerModel(EventDispatcher):
    timer_label = StringProperty('')
    pomodoros_counter = NumericProperty(0)

    def __init__(self):
        super(TimerModel, self).__init__()
        self.timer_label = ''

model = TimerModel()


class TimerMixin(object):
    duration = 0
    timer = None
    model = model

    def reset_timer(self, duration=None):
        self.timer = Timer(seconds=duration or self.duration)
        self.model.timer_label = str(self.timer)

    def timer_tick(self):
        self.timer = self.timer.tick()
        self.model.timer_label = str(self.timer)


class WelcomeScreen(Screen):
    pass


class TimerScreen(TimerMixin, Screen):
    duration = 1
    timer = None

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)

    def pomodoro_start(self, *_):
        Logger.debug('Starting pomodoro')
        model.pomodoros_counter += 1
        self.reset_timer()
        model.timer_label = str(self.timer)
        Clock.schedule_interval(self.pomodoro_timer, 1)

    def pomodoro_stop(self):
        Logger.debug('Stopping pomodoro')
        screen_manager.current = 'pomodoros_over'

    def pomodoro_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.pomodoro_stop()
            return False


class PomodorosOverScreen(Screen):
    button_label = DynamicLabel()

    def update_button_label(self):
        if model.pomodoros_counter % 4:
            self.button_label.label = 'Start short break'
        else:
            self.button_label.label = 'Start long break'


class BreakScreen(TimerMixin, Screen):
    button = None
    short_duration = 3
    long_duration = 10

    def __init__(self, **kwargs):
        self.timer = Timer(seconds=self.duration)
        super(BreakScreen, self).__init__(**kwargs)

    @property
    def is_short(self):
        return bool(model.pomodoros_counter % 4)

    @property
    def duration(self):
        return self.short_duration if self.is_short else self.long_duration

    def break_start(self):
        if self.is_short:
            Logger.debug('Starting short break')
        else:
            Logger.debug('Starting long break')

        self.reset_timer()
        Clock.schedule_interval(self.break_timer, 1)

    def break_timer(self, _):
        self.timer_tick()
        if not self.timer:
            self.break_stop()
            return False

    def break_stop(self):
        Logger.debug('Stopping break')
        screen_manager.current = 'breaks_over'


class BreaksOverScreen(Screen):
    pass


# Create the screen manager
screen_manager = ScreenManager()
screen_manager.add_widget(WelcomeScreen(name='welcome'))
screen_manager.add_widget(TimerScreen(name='timer'))
screen_manager.add_widget(PomodorosOverScreen(name='pomodoros_over'))
screen_manager.add_widget(BreakScreen(name='break'))
screen_manager.add_widget(BreaksOverScreen(name='breaks_over'))


class KetchuporoApp(App):
    def build(self):
        return screen_manager


if __name__ == '__main__':
    KetchuporoApp().run()
