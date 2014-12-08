import math
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Line

class Bullet(Widget):

    rotation = NumericProperty(0.0)

    def __init__(self, shooter, length, **kwargs):
        self.shooter = shooter
        self.rotation = self.shooter.rotation
        self.pos = self.shooter.center
        self.points = [self.x, self.y, self.x + length, self.y]
        self.rotcenter = [self.x, self.y]
        super(Bullet, self).__init__(**kwargs)
    

class Player(Widget):
    triangleImage = ObjectProperty(None)

    direction_x = NumericProperty(0.0)
    direction_y = NumericProperty(0.0)
    direction_i = NumericProperty(0.0)
    direction_j = NumericProperty(0.0)

    rotation = NumericProperty(0.0)
    rotation_factor = NumericProperty(2.8)

    max_vel_coef = NumericProperty(.07)

    direction = ReferenceListProperty(direction_x, direction_y)

    FORWARD = 0
    BACKWARD = 1
    LEFT = 2
    RIGHT = 3
    TURN_R = 4
    TURN_L = 5
    SHOOTING = 6

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rotation = 90.0
        self.last_bullet = None

    def update(self):
        # Update x, y system
        x = self.center[0] + (self.direction_x * -self.state[Player.BACKWARD]) + (self.direction_x * self.state[Player.FORWARD])
        y = self.center[1] + (self.direction_y * -self.state[Player.BACKWARD]) + (self.direction_y * self.state[Player.FORWARD])
        # Update i, j system
        x += (self.direction_i * -self.state[Player.LEFT]) + (self.direction_i * self.state[Player.RIGHT])
        y += (self.direction_j * -self.state[Player.LEFT]) + (self.direction_j * self.state[Player.RIGHT])
        # Update rotation
        self.rotation = (self.rotation - (self.rotation_factor * self.state[Player.TURN_R]) + (self.rotation_factor * self.state[Player.TURN_L])) % 360
        self.center = [x, y]
        if self.last_bullet:
            self.remove_widget(self.last_bullet)
        if (self.state[Player.SHOOTING]):
            self.last_bullet = Bullet(self, 200)
            self.add_widget(self.last_bullet)
        # Update the bulletLine

    def startMove(self, action):
        self.state[action] = 1;

    def stopMove(self, action):
        self.state[action] = 0;

    def on_rotation(self, instance, value):
        self.direction_x = math.degrees(math.cos(math.radians(value))) * self.max_vel_coef
        self.direction_y = math.degrees(math.sin(math.radians(value))) * self.max_vel_coef
        self.direction_i = math.degrees(math.cos(math.radians(value - 90))) * self.max_vel_coef * .5
        self.direction_j = math.degrees(math.sin(math.radians(value - 90))) * self.max_vel_coef * .5

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
                "up": lambda x: self.player.startMove(Player.FORWARD),
                "down": lambda x: self.player.startMove(Player.BACKWARD),
                "a": lambda x: self.player.startMove(Player.LEFT),
                "d": lambda x: self.player.startMove(Player.RIGHT),
                "left": lambda x: self.player.startMove(Player.TURN_L),
                "right": lambda x: self.player.startMove(Player.TURN_R),
                "spacebar": lambda x: self.player.startMove(Player.SHOOTING)
            }
            move = player_moves.get(keycode[1])
            if move:
                move(0)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        player_moves = {
            "up": lambda x: self.player.stopMove(Player.FORWARD),
            "down": lambda x: self.player.stopMove(Player.BACKWARD),
            "a": lambda x: self.player.stopMove(Player.LEFT),
            "d": lambda x: self.player.stopMove(Player.RIGHT),
            "left": lambda x: self.player.stopMove(Player.TURN_L),
            "right": lambda x: self.player.stopMove(Player.TURN_R),
            "spacebar": lambda x: self.player.stopMove(Player.SHOOTING)
        }
        move = player_moves.get(keycode[1])
        if move:
            move(0)
        pass

    def update(self, dt):
        self.player.update()

class StealthyApp(App):

    def build(self):
        game = StealthyGame(self)
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    StealthyApp().run()