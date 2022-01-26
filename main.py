import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import *
from tower_manager import TowerManager  # needed for kivy layout

kivy.require('2.0.0')


class Controller(BoxLayout):
    move_count = NumericProperty(0)
    disc_count = NumericProperty(3)
    mode = StringProperty('unicolor')
    tower_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tower_count = 3
        Clock.schedule_interval(self.tower_manager.init, 1)

    def set_mode(self, new_mode):
        self.mode = new_mode
        self.reset()

    def reset(self):
        self.stop_complete()
        self.move_count = 0
        self.tower_manager.reset(self.disc_count)

    def start_complete(self):
        self.stop_complete()
        for child in self.tower_manager.children[:-1]:
            if child.discs:
                self.reset()
                break
        self.tower_manager.init_complete(self.mode)

    def stop_complete(self):
        if self.tower_manager.commands:
            self.tower_manager.stop_complete()


class HanoiApp(App):
    def build(self):
        return Controller()


if __name__ == '__main__':
    HanoiApp().run()
