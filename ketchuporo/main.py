from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from ketchuporo.const import Files
from ketchuporo.controllers import (
    BreakScreen,
    BreaksOverScreen,
    PomodorosOverScreen,
    SettingsScreen,
    WelcomeScreen,
)
from ketchuporo.controllers import TimerScreen


Builder.load_file(Files.KV)
LabelBase.register(name='RobotoLight', fn_regular='lib/fonts/roboto_light.ttf')


# Create the screen manager
screen_manager = ScreenManager()
screen_manager.add_widget(WelcomeScreen(name='welcome'))
screen_manager.add_widget(
    TimerScreen(screen_manager=screen_manager, name='timer'))
screen_manager.add_widget(PomodorosOverScreen(name='pomodoros_over'))
screen_manager.add_widget(
    BreakScreen(screen_manager=screen_manager, name='break'))
screen_manager.add_widget(BreaksOverScreen(name='breaks_over'))
screen_manager.add_widget(SettingsScreen(name='settings'))


class KetchuporoApp(App):
    def build(self):
        return screen_manager


if __name__ == '__main__':
    KetchuporoApp().run()
