from datetime import timedelta
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget


class Timer(timedelta, object):
    pass


class Ketchuporo(Widget):
    timer = Timer(minutes=25)

    def __init__(self):
        super(Ketchuporo, self).__init__()
        Clock.schedule_interval(self.run_timer, 1)

    def run_timer(self, *args):
        self.timer = self.timer - timedelta(seconds=1)
        print(self.timer)


class KetchuporoApp(App):
    def build(self):
        return Ketchuporo()

if __name__ == '__main__':
    KetchuporoApp().run()
