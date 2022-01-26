from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class Tower(Widget):
    """Manages a single tower. Is manipulated by the TowerManager"""

    arrow = Image(source='arrow.png')

    def __init__(self, index, max_discs_no, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.discs = []
        self.disc_data = []
        self.max_discs_no = max_discs_no  # == max radius
        self.target_tower = None
        self.select_marker = None
        self.disc_height = lambda: min((self.height * 0.06, self.height * 0.53 / self.max_discs_no))
        self.get_disc_y_pos = lambda n: self.height * 0.22 + n * self.disc_height()
        # Arranging Canvas
        with self.canvas:
            Color(190 / 256, 140 / 256, 54 / 256)  # set the pole color
            # Setting the size and position of canvas
            self.rod = Rectangle()
            self.rod_base = Rectangle()
            # Make the tower responsive
            self.bind(size=self._update_tower)

    # update function which makes the canvas adjustable.
    def _update_tower(self, *args):
        self.rod.pos = (self.center_x - self.width / 200, self.height * 0.2)
        self.rod.size = (self.width / 50, self.height * 0.6)
        self.rod_base.pos = (self.center_x - self.width * 0.4, self.height * 0.190)
        self.rod_base.size = (self.width * 0.8, self.height * 0.03)

        for i in range(len(self.discs)):
            self._update_disc(i, self.disc_data[i][0])

        if self.select_marker:
            self.select_marker.pos = (self.center_x - self.width * 0.1, self.height * .05)
            self.select_marker.size = (self.width * 0.2, self.height * 0.1)

    def add_disc(self, radius, hue):
        with self.canvas:
            Color(hue, .8, .95, mode='hsv')
            disc = Rectangle()
            self.discs.append(disc)
            self._update_disc(len(self.discs) - 1, radius)
            self.disc_data.append((radius, hue))

    def toggle_selected(self):
        if not self.select_marker:
            with self.canvas:
                Color(50/256, 195/256, 240/256)
                self.select_marker = Rectangle()
                self.select_marker.texture = Tower.arrow.texture
                self.select_marker.size = Tower.arrow.size
            self._update_tower()
        else:
            self.canvas.remove(self.select_marker)
            self.select_marker = None

    def _update_disc(self, index, radius):
        disc_width = self.width * 0.7 * radius / self.max_discs_no
        disc = self.discs[index]
        disc.pos = (self.center_x - disc_width * 0.5,
                    self.get_disc_y_pos(index))
        disc.size = (disc_width, self.disc_height())

    def remove_disc(self):
        if len(self.discs) == 0:
            raise IndexError('Tried to remove a disc from an empty tower')
        self.canvas.remove(self.discs.pop())
        self.disc_data.pop()

    def remove_all_discs(self):
        while self.discs:
            self.remove_disc()

    def _on_move_complete(self, instance, widget):
        if self.disc_data:  # make sure simulation was not stopped during animation
            self.target_tower.add_disc(*self.disc_data[-1])
            self.remove_disc()
            self.parent.step()

    def move_disc_to(self, target_tower):
        if not self.discs:
            print("Can't move a disc out of an empty tower :C")
            return
        disc = self.discs[-1]
        self.target_tower = target_tower
        dur = 0.05
        index_diff = target_tower.index - self.index
        anim = Animation(pos=(disc.pos[0], self.height * 0.85), duration=dur)
        anim += Animation(pos=(disc.pos[0] + index_diff * self.width, self.height * 0.85), duration=dur)
        anim += Animation(pos=(disc.pos[0] + index_diff * self.width, self.get_disc_y_pos(len(target_tower.discs))),
                          duration=dur)
        anim.bind(on_complete=self._on_move_complete)
        anim.start(disc)
