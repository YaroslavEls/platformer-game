import arcade

from constants import RIGHT_FACING, CHARACTER_SCALING, ASSETS_PATH


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name):
        super().__init__()

        self.facing_direction = RIGHT_FACING
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        path = f'{ASSETS_PATH}/images/characters/{name}'

        self.idle_texture_pair = load_texture_pair(f'{path}/{name}_idle.png')
        self.jump_texture_pair = load_texture_pair(f'{path}/{name}_jump.png')
        self.fall_texture_pair = load_texture_pair(f'{path}/{name}_fall.png')

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f'{path}/{name}_walk{i}.png')
            self.walk_textures.append(texture)

        self.climb_textures = []
        for i in range(2):
            texture = arcade.load_texture(f'{path}/{name}_climb{i}.png')
            self.climb_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

        self.set_hit_box(self.texture.hit_box_points)
