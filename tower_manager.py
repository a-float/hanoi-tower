from random import random as r
from kivy.uix.boxlayout import BoxLayout
from hanoi import hanoi, bicolor_hanoi
from tower import Tower


class TowerManager(BoxLayout):
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
        clamp = lambda x: min(0.1, max(0.9, x))
        if self.parent.mode == 'unicolor':
            start_hue = r()
            step = clamp(r())
            get_hue = lambda no: (step* no + start_hue) % 1
        else:
            hue = r()
            diff = clamp(r())
            get_hue = lambda no: hue if no % 2 else (hue + 0.3 + diff / 3) % 1
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
                if self.source is None:
                    if child.discs:
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
