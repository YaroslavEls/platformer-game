from constants import RIGHT_FACING, LEFT_FACING
from entities.entity import Entity


class Enemy(Entity):
    def __init__(self, name):
        super().__init__(name)

        self.should_update_walk = 0
        self.health = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1
