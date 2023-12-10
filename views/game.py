import math

import arcade

from constants import *
from entities.player import Player
from entities.enemy import Enemy
from views.view import View


class GameView(View):
    def __init__(self):
        super().__init__()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.end_of_map = 0

        self.score = 0
        self.reset_score = True
        self.level = 1
        self.lives = 0
        self.selected_player = None
        self.difficulty = None

        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover3.wav")

    def setup(self):
        super().setup()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        map_name = ':resources:tiled_maps/level_1.json'

        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DEATH: {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.reset_score:
            if self.difficulty == 'hard':
                self.lives = 1
            else:
                self.lives = 3
            self.score = 0
        self.reset_score = True

        self.scene.add_sprite_list_after(LAYER_NAME_PLAYER, LAYER_NAME_BACKGROUND)

        self.player_sprite = Player(self.selected_player)
        self.player_sprite.center_x = (
            self.tile_map.tiled_map.tile_size[0] * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tiled_map.tile_size[1] * TILE_SCALING * PLAYER_START_Y
        )
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE

        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        for object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                object.shape[0], object.shape[1]
            )
            enemy_type = object.properties["type"]
            enemy = Enemy(enemy_type)
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            if object.properties["change_x"]:
                enemy.change_x = int(object.properties["change_x"])
                enemy.boundary_left = int(object.properties["boundary_left"])
                enemy.boundary_right = int(object.properties["boundary_right"])
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant=GRAVITY, 
            walls=self.scene[LAYER_NAME_PLATFORMS],
            ladders=self.scene[LAYER_NAME_LADDERS],
        )

    def on_show_view(self):
        arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()

        text = f"Score: {self.score}, Level: {self.level}, Lives: {self.lives}"
        arcade.draw_text(
            text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

    def process_keychange(self):
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views['pause'])

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > (self.end_of_map - self.camera.viewport_width):
            screen_center_x = (self.end_of_map - self.camera.viewport_width)
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_PLAYER,
                LAYER_NAME_ENEMIES
            ],
        )

        self.scene.update(
            [LAYER_NAME_ENEMIES]
        )

        for enemy in self.scene.get_sprite_list(LAYER_NAME_ENEMIES):
            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1

        collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite, 
            [
                self.scene[LAYER_NAME_DEATH],
                self.scene[LAYER_NAME_ENEMIES],
                self.scene[LAYER_NAME_FINISH],
                self.scene[LAYER_NAME_COINS]
            ]
        )

        for collision in collision_list:
            if self.scene.get_sprite_list(LAYER_NAME_DEATH) in collision.sprite_lists \
               or self.scene.get_sprite_list(LAYER_NAME_ENEMIES) in collision.sprite_lists:
                arcade.play_sound(self.death_sound)
                if self.lives > 1:
                    self.reset_score = False
                    self.lives -= 1
                    self.setup()
                else:
                    self.window.show_view(self.window.views['ending'])
            elif self.scene.get_sprite_list(LAYER_NAME_FINISH) in collision.sprite_lists:
                self.level += 1
                self.reset_score = False
                self.setup()
            elif self.scene.get_sprite_list(LAYER_NAME_COINS) in collision.sprite_lists:
                points = int(collision.properties["Points"])
                self.score += points

                collision.remove_from_sprite_lists()
                arcade.play_sound(self.coin_sound)

        if self.player_sprite.center_y < -100:
            self.setup()
            arcade.play_sound(self.death_sound)

        self.center_camera_to_player()
