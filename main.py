import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import *
from random import random as r
from hanoi import hanoi, bicolor_hanoi
from tower import Tower

kivy.require('2.0.0')


class Towers(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = None
        self.commands = []
        self.current_disc_count = 3  # no of discs currently on the screen
        self.current_comm_index = 0

    def init(self, dt):
        for i in range(self.parent.tower_count):
            self.add_widget(Tower(i, self.parent.disc_count))
        self.reset(self.parent.disc_count)  # hardcoded initial values for now
        return False  # to cancel the clock callback

    def reset(self, disc_count):
        self.current_disc_count = disc_count
        for tower in self.children:
            tower.remove_all_discs()
            tower.max_discs_no = disc_count

        left_tower = self.children[-1]
        if self.parent.mode == 'unicolor':
            get_hue = lambda no: r()
        else:
            hue = r()
            diff = r()
            get_hue = lambda no: hue if no % 2 else (hue+0.3+diff/3) % 1
        for i in range(disc_count):
            left_tower.add_disc(disc_count - i, get_hue(i))

    def init_complete(self, mode):
        try:
            if mode == 'unicolor':
                hanoi(*reversed(self.children), self.parent.disc_count, self.commands)
            elif mode == 'bicolor':
                bicolor_hanoi(*reversed(self.children), self.parent.disc_count, self.commands)
            print("Starting the solve")
            self.step()
        except AssertionError as e:
            print("Could not start the solve: " + str(e))

    def step(self):
        if self.commands:
            comm = self.commands[self.current_comm_index]
            self.current_comm_index += 1
            self.parent.move_count += 1
            comm[0].move_disc_to(comm[1])
            if self.current_comm_index == len(self.commands):  # it's the last command
                self.stop_complete()

    def stop_complete(self):
        self.commands = []
        self.current_comm_index = 0
        print("The solve has been completed")

    def on_touch_down(self, touch):
        for i, child in enumerate(self.children):
            if child.collide_point(*touch.pos):
                print(f"Ah im touched ,,^^,, {i}")
                if self.source is None:
                    self.source = child
                    self.source.toggle_selected()
                elif self.source == child:
                    self.source.toggle_selected()
                    self.source = None
                else:
                    self.source.move_disc_to(child)
                    self.parent.move_count += 1
                    self.source.toggle_selected()
                    self.source = None


class Controller(BoxLayout):
    move_count = NumericProperty(0)
    disc_count = NumericProperty(3)
    mode = StringProperty('unicolor')
    towers_object = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tower_count = 3
        Clock.schedule_interval(self.towers_object.init, 1)

    def reset(self):
        self.stop_complete()
        self.move_count = 0
        self.towers_object.reset(self.disc_count)

    def complete(self):
        if self.towers_object.current_disc_count != self.disc_count:
            self.reset()
        for child in self.towers_object.children[:-1]:
            if child.discs:
                self.reset()
                break
        self.towers_object.init_complete(self.mode)

    def stop_complete(self):
        if self.towers_object.commands:
            self.towers_object.stop_complete()


class HanoiApp(App):
    def build(self):
        return Controller()


if __name__ == '__main__':
    HanoiApp().run()
