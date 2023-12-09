import arcade

from constants import CHARACTER_SCALING


class Entity(arcade.Sprite):
    def __init__(self, name):
        super().__init__()

        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        path = f':resources:images/animated_characters/{name}'

        self.idle_texture = arcade.load_texture(f'{path}/{name}_idle.png')

        self.texture = self.idle_texture

        self.set_hit_box(self.texture.hit_box_points)
