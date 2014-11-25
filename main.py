import math
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class Player(Widget):
    direction_x = NumericProperty(0.0)
    direction_y = NumericProperty(0.0)

    mask_x = NumericProperty(0)
    mask_y = NumericProperty(0)

    rotation = NumericProperty(90.0)
    rotation_factor = NumericProperty(5)

    max_vel_coef = NumericProperty(.1)

    direction = ReferenceListProperty(direction_x, direction_y)
    mask = ReferenceListProperty(mask_x, mask_y)


    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        # TODO: Create the movement binary vector, in order to know in which directions it's moving.
        # self.mask_y = 0
        # self.mask_x = 0

    def update(self):
        self.center = (Vector(*self.direction) * [self.mask_x, self.mask_y]) + self.center

    def forward(self):
        self.mask_x = 1
        self.mask_y = 1

    def backward(self):
        self.mask_x = -1
        self.mask_y = -1

    def turnRight(self):
        self.rotation = (self.rotation - self.rotation_factor) % 360

    def turnLeft(self):
        self.rotation = (self.rotation + self.rotation_factor) % 360

    def strafeRight(self):
        self.mask_x *= -1

    def strafeLeft(self):
        self.mask_y *= -1

    def on_rotation(self, instance, value):
        self.direction_x = math.degrees(math.cos(math.radians(value))) * self.max_vel_coef * self.mask[0]
        self.direction_y = math.degrees(math.sin(math.radians(value))) * self.max_vel_coef * self.mask[1]

class StealthyGame(Widget):

    player = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        super(StealthyGame, self).__init__(**kwargs)
        self.app = app
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "f4" and modifiers == ['alt']:
            self.app.stop()
        else:
            player_moves = {
                "up": self.player.forward,
                "down": self.player.backward,
                "a": self.player.strafeLeft,
                "d": self.player.strafeRight,
                "left": self.player.turnLeft,
                "right": self.player.turnRight
            }
            move = player_moves.get(keycode[1])
            if move:
                move()
                print(self.player.mask_x, self.player.mask_y)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        pass

    def update(self, dt):
        print(self.player.mask_x, self.player.mask_y)
        self.player.update()

class StealthyApp(App):

    def build(self):
        game = StealthyGame(self)
        Clock.schedule_interval(game.update, 10.0/60.0)
        return game


if __name__ == '__main__':
    StealthyApp().run()