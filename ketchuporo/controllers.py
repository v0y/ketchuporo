from datetime import timedelta
import json

from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from plyer import notification

from ketchuporo import Audio
from ketchuporo.const import (
    APP_NAME,
    Files,
)
from ketchuporo.models import TimerModel


notifications_kwargs = {
    'pomodoros_over': {
        'title': 'Pomodoro is over!',
        'message': 'Take a break.',
        'app_name': APP_NAME,
        'app_icon': '',
        'timeout': 20,
    },
    'breaks_over': {
        'title': 'Break is over!',
        'message': 'Get back to work.',
        'app_name': APP_NAME,
        'app_icon': '',
        'timeout': 20,
    }
}


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


class TimerMixin(object):
    duration = 0
    timer = None  # Timer object
    timer_event = None  # Clock object
    model = TimerModel()
    countdown = True

    def is_break_short(self):
        return bool(
            self.model.pomodori_counter % self.model.pomodori_for_cycle
        )

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

    def __init__(self, screen_manager, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

    @property
    def duration(self):
        return self.model.pomodoro_duration

    def timer_pre_start(self):
        Logger.debug('Pre-starting pomodoro')
        self.model.pomodori_counter += 1
        self.timer_reset()

    def update_break_button_label(self):
        if self.is_break_short():
            self.start_break_label.label = 'Start short break'
        else:
            self.start_break_label.label = 'Start long break'

    def timer_start(self):
        Logger.debug('Starting pomodoro')
        self.model.timer_label = str(self.timer)
        super(TimerScreen, self).timer_start()

    def timer_stop(self):
        Logger.debug('Stopping pomodoro')
        super(TimerScreen, self).timer_stop()
        notification.notify(**notifications_kwargs['pomodoros_over'])
        if self.model.bell_after_pomodoro:
            Audio.bell.play()
        self.screen_manager.current = 'pomodoros_over'


class PomodorosOverScreen(TimerMixin, Screen):
    button_label = DynamicLabel()
    countdown = False

    def __init__(self, **kwargs):
        super(PomodorosOverScreen, self).__init__(**kwargs)

    def update_button_label(self):
        if self.is_break_short():
            self.button_label.label = 'Start short break'
        else:
            self.button_label.label = 'Start long break'

    def timer_pre_start(self):
        Logger.debug('Pre-starting pomodoro is over')
        self.timer_reset()

    def timer_start(self):
        Logger.debug('Starting pomodoro is over')
        self.model.timer_label = str(self.timer)
        super(PomodorosOverScreen, self).timer_start()


class BreakScreen(TimerMixin, Screen):
    button = None
    short_duration = 3
    long_duration = 10
    break_label = DynamicLabel()

    def __init__(self, screen_manager, **kwargs):
        self.timer = Timer(minutes=self.duration)
        self.screen_manager = screen_manager
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
        if self.model.bell_after_break:
            Audio.bell.play()
        notification.notify(**notifications_kwargs['breaks_over'])
        self.screen_manager.current = 'breaks_over'


class BreaksOverScreen(TimerMixin, Screen):
    countdown = False

    def __init__(self, **kwargs):
        super(BreaksOverScreen, self).__init__(**kwargs)

    def timer_pre_start(self):
        Logger.debug('Pre-starting break is over')
        self.timer_reset()

    def timer_start(self):
        Logger.debug('Starting break is over')
        self.model.timer_label = str(self.timer)
        super(BreaksOverScreen, self).timer_start()


class SettingsScreen(TimerMixin, Screen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # load settings
        self.prepare_settings_file()
        self.settings = {}
        self.load_settings()

    @staticmethod
    def prepare_settings_file():
        Logger.debug('Preparing settins file...')
        try:
            settings_file = open(Files.SETTINGS, 'r')
        except IOError:
            Logger.debug('Settins file not found, creating from defaults')
            default_settings_file = open(Files.SETTINGS_DEFAULT, 'r')
            settings_file = open(Files.SETTINGS, 'w')
            settings_file.write(default_settings_file.read())
            settings_file.close()
            default_settings_file.close()
        else:
            settings_file.close()

    def reset_settings(self):
        Logger.debug('Reset settings to default')
        self.load_settings(Files.SETTINGS_DEFAULT)

    def load_settings(self, file_=None):
        file_ = file_ or Files.SETTINGS
        Logger.debug('Loading settings from file {}...'.format(file_))
        settings_file = open(file_, 'r')
        self.settings = json.loads(settings_file.read())
        settings_file.close()

        update_value_for = [
            'pomodoro_duration',
            'short_break_duration',
            'long_break_duration',
            'pomodori_for_cycle',
        ]

        update_active_for = [
            'bell_after_pomodoro',
            'bell_after_break',
        ]

        for k, v in self.settings.items():
            Logger.debug(' * set {} to {}'.format(k, v))

            if k in update_value_for:
                self.ids[k].value = v
            elif k in update_active_for:
                self.ids[k].active = v

            setattr(self.model, k, v)
        Logger.debug('Settings loaded!')

    def save_settings(self):
        Logger.debug('Saving settings...')
        self.settings['pomodoro_duration'] \
            = self.ids['pomodoro_duration'].value
        self.settings['short_break_duration'] \
            = self.ids['short_break_duration'].value
        self.settings['long_break_duration'] \
            = self.ids['long_break_duration'].value
        self.settings['pomodori_for_cycle'] \
            = self.ids['pomodori_for_cycle'].value
        self.settings['bell_after_pomodoro'] \
            = self.ids['bell_after_pomodoro'].active
        self.settings['bell_after_break'] \
            = self.ids['bell_after_break'].active

        settings_file = open(Files.SETTINGS, 'w')
        settings_file.write(json.dumps(self.settings))
        settings_file.close()
        Logger.debug('Saved!')

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
