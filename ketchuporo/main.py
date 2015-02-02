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

from ketchuporo import Audio
from ketchuporo.const import (
    Defaults,
    Files,
)


Builder.load_file(Files.KV)


class Timer(timedelta, object):
    def tick(self):
        seconds = self.seconds - 1
        return Timer(seconds=seconds)

    def tick_up(self):
        seconds = self.seconds + 1
        return Timer(seconds=seconds)


class DynamicLabel(EventDispatcher):
    label = StringProperty('')

    def __init__(self):
        super(DynamicLabel, self).__init__()
        self.label = ''


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

model = TimerModel()


class TimerMixin(object):
    duration = 0
    timer = None  # Timer object
    timer_event = None  # Clock object
    model = model  # TimerModel object
    countdown = True

    @classmethod
    def is_break_short(cls):
        return bool(model.pomodori_counter % model.pomodori_for_cycle)

    def timer_reset(self):
        Logger.debug('Reset timer')
        self.timer = Timer(minutes=self.duration)
        self.model.timer_label = str(self.timer)

    def reset_pomodori_counter(self):
        Logger.debug('Reset pomodori counter')
        self.model.pomodori_counter = 0

    def timer_tick(self):
        if self.countdown:
            self.timer = self.timer.tick()
        else:
            self.timer = self.timer.tick_up()
        self.model.timer_label = str(self.timer)

    def timer_start(self):
        Clock.unschedule(self.timer_runner)
        self.timer_event = Clock.schedule_interval(self.timer_runner, 1)

    def timer_stop(self):
        self.timer_unschedule()

    def timer_unschedule(self):
        Logger.debug('Unscheduling timer')
        Clock.unschedule(self.timer_runner)

    def timer_runner(self, _):
        self.timer_tick()
        if not self.timer and self.countdown:
            self.timer_stop()
            return False


class WelcomeScreen(TimerMixin, Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

    @staticmethod
    def exit():
        Logger.debug('Exiting')
        App.get_running_app().stop()


class TimerScreen(TimerMixin, Screen):
    timer = None
    start_break_label = DynamicLabel()

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)

    @property
    def duration(self):
        return self.model.pomodoro_duration

    def timer_pre_start(self):
        Logger.debug('Pre-starting pomodoro')
        model.pomodori_counter += 1
        self.timer_reset()

    def update_break_button_label(self):
        if self.is_break_short():
            self.start_break_label.label = 'Start short break'
        else:
            self.start_break_label.label = 'Start long break'

    def timer_start(self):
        Logger.debug('Starting pomodoro')
        model.timer_label = str(self.timer)
        super(TimerScreen, self).timer_start()

    def timer_stop(self):
        Logger.debug('Stopping pomodoro')
        super(TimerScreen, self).timer_stop()
        if model.bell_after_pomodoro:
            Audio.bell.play()
        screen_manager.current = 'pomodoros_over'


class PomodorosOverScreen(TimerMixin, Screen):
    button_label = DynamicLabel()
    countdown = False

    def update_button_label(self):
        if model.pomodori_counter % model.pomodori_for_cycle:
            self.button_label.label = 'Start short break'
        else:
            self.button_label.label = 'Start long break'

    def timer_pre_start(self):
        Logger.debug('Pre-starting pomodoro is over')
        self.timer_reset()

    def timer_start(self):
        Logger.debug('Starting pomodoro is over')
        model.timer_label = str(self.timer)
        super(PomodorosOverScreen, self).timer_start()


class BreakScreen(TimerMixin, Screen):
    button = None
    short_duration = 3
    long_duration = 10
    break_label = DynamicLabel()

    def __init__(self, **kwargs):
        self.timer = Timer(seconds=self.duration)
        super(BreakScreen, self).__init__(**kwargs)

    @property
    def duration(self):
        if self.is_break_short():
            return self.model.short_break_duration
        else:
            return self.model.long_break_duration

    def update_break_label(self):
        if self.is_break_short():
            self.break_label.label = 'Short break'
        else:
            self.break_label.label = 'Long break'

    def timer_pre_start(self):
        Logger.debug('Pre-starting break')
        self.timer_reset()

    def timer_start(self):
        if self.is_break_short():
            Logger.debug('Starting short break')
        else:
            Logger.debug('Starting long break')
        super(BreakScreen, self).timer_start()

    def timer_stop(self):
        Logger.debug('Stopping break')
        super(BreakScreen, self).timer_stop()
        if model.bell_after_break:
            Audio.bell.play()
        screen_manager.current = 'breaks_over'


class BreaksOverScreen(TimerMixin, Screen):
    countdown = False

    def timer_pre_start(self):
        Logger.debug('Pre-starting break is over')
        self.timer_reset()

    def timer_start(self):
        Logger.debug('Starting break is over')
        model.timer_label = str(self.timer)
        super(BreaksOverScreen, self).timer_start()


class SettingsScreen(Screen):
    model = model

    def reset_settings(self):
        Logger.debug('Reset settings to default')
        self.ids['pomodoro_duration'].value = Defaults.POMODORO_DURATION
        self.ids['short_break_duration'].value = Defaults.SHORT_BREAK
        self.ids['long_break_duration'].value = Defaults.LONG_BREAK
        self.ids['pomodori_for_cycle'].value = Defaults.POMODORI_FOR_CYCLE
        self.ids['bell_after_pomodoro'].active = Defaults.BELL_AFTER_POMODORO
        self.ids['bell_after_break'].active = Defaults.BELL_AFTER_BREAK

    def set_pomodoro_duration(self, _, value):
        self.model.pomodoro_duration = value

    def set_short_break_duration(self, _, value):
        self.model.short_break_duration = value

    def set_long_break_duration(self, _, value):
        self.model.long_break_duration = value

    def set_pomodori_for_cycle(self, _, value):
        self.model.pomodori_for_cycle = value

    def set_bell_after_pomodoro(self, _, value):
        self.model.bell_after_pomodoro = value

    def set_bell_after_break(self, _, value):
        self.model.bell_after_break = value


# Create the screen manager
screen_manager = ScreenManager()
screen_manager.add_widget(WelcomeScreen(name='welcome'))
screen_manager.add_widget(TimerScreen(name='timer'))
screen_manager.add_widget(PomodorosOverScreen(name='pomodoros_over'))
screen_manager.add_widget(BreakScreen(name='break'))
screen_manager.add_widget(BreaksOverScreen(name='breaks_over'))
screen_manager.add_widget(SettingsScreen(name='settings'))


class KetchuporoApp(App):
    def build(self):
        return screen_manager


if __name__ == '__main__':
    KetchuporoApp().run()
