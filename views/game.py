import math

import arcade

from constants import *
from views.view import View
from entities.player import Player
from entities.enemy import Enemy


class GameView(View):
    def __init__(self):
        super().__init__()

        self.left_pressed: bool
        self.right_pressed: bool
        self.up_pressed: bool
        self.down_pressed: bool
        self.jump_needs_reset: bool
        self.shoot_pressed: bool

        self.camera: arcade.Camera
        self.gui_camera: arcade.Camera
        self.tile_map: arcade.TileMap
        self.scene: arcade.Scene
        self.player_sprite: Player
        self.physics_engine: arcade.PhysicsEnginePlatformer
        
        self.can_shoot: bool
        self.shoot_timer: int
        self.end_of_map: int

        self.selected_player: str
        self.difficulty: str
        self.lives: int

        self.score: int = 0
        self.reset_score: bool = True
        self.level: int = 1
        
        self.keys: list
        self.lock_pairs: dict

        self.jump_sound = arcade.load_sound(JUMP_SOUND_PATH)
        self.coin_sound = arcade.load_sound(COIN_SOUND_PATH)
        self.death_sound = arcade.load_sound(DEATH_SOUND_PATH)
        self.shoot_sound = arcade.load_sound(SHOOT_SOUND_PATH)
        self.hit_sound = arcade.load_sound(HIT_SOUND_PATH)

    #----- HELPER FUNCTIONS FOR setup() -----#

    def _setup_player(self):
        self.player_sprite = Player(self.selected_player)

        self.player_sprite.center_x = (
            self.tile_map.tiled_map.tile_size[0] * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tiled_map.tile_size[1] * TILE_SCALING * PLAYER_START_Y
        )

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

    def _setup_enemies(self):
        if LAYER_NAME_ENEMIES not in self.tile_map.object_lists:
            return

        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
        
        for object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                object.shape[0], object.shape[1]
            )

            enemy_type = object.properties["type"]
            enemy_health = (1 if self.difficulty == 'easy' 
                            else int(object.properties["health"]))
            enemy = Enemy(enemy_type, enemy_health)

            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1]+1) * TILE_SCALING * self.tile_map.tile_height
            )

            if bool(object.properties["change_x"]):
                enemy.change_x = int(object.properties["change_x"])
                enemy.boundary_left = int(object.properties["boundary_left"])
                enemy.boundary_right = int(object.properties["boundary_right"])
            
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

    #----- BASIC SETUP FUNCTIONS -----#

    def setup(self):
        super().setup()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.shoot_pressed = False

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.tile_map = arcade.load_tilemap(MAP_NAME(self.level), TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.can_shoot = True
        self.shoot_timer = 0
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE

        if self.reset_score:
            if self.difficulty == 'hard':
                self.lives = 1
            else:
                self.lives = 3
            self.score = 0
        self.reset_score = True

        self.keys = []
        self.lock_pairs = {}
        for tile in self.scene[LAYER_NAME_PLATFORMS]:
            if 'color' in tile.properties:
                self.lock_pairs[tile.properties['color']] = tile

        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self._setup_player()
        self._setup_enemies()
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite, 
            gravity_constant=GRAVITY, 
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )

        arcade.set_background_color(self.tile_map.tiled_map.background_color)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()

        text1 = f'Score: {self.score}, Level: {self.level}'
        text2 = f'Lives: {self.lives}, Keys: {self.keys}'

        arcade.draw_text(
            text=text1+', '+text2,
            start_x=10,
            start_y=10,
            color=arcade.csscolor.BLACK,
            font_size=18
        )

    #----- KEYS HANDLING -----#

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
        elif (
            self.down_pressed 
            and not self.up_pressed
            and self.physics_engine.is_on_ladder()
        ):
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
        match key:
            case arcade.key.UP:
                self.up_pressed = True
            case arcade.key.DOWN:
                self.down_pressed = True
            case arcade.key.LEFT:
                self.left_pressed = True
            case arcade.key.RIGHT:
                self.right_pressed = True
            case arcade.key.Q:
                self.shoot_pressed = True
            case arcade.key.ESCAPE:
                self.window.show_view(self.window.views['pause'])

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        match key:
            case arcade.key.UP:
                self.up_pressed = False
                self.jump_needs_reset = False
            case arcade.key.DOWN:
                self.down_pressed = False
            case arcade.key.LEFT:
                self.left_pressed = False
            case arcade.key.RIGHT:
                self.right_pressed = False
            case arcade.key.Q:
                self.shoot_pressed = False

        self.process_keychange()

    #----- HELPER FUCTIONS FOR on_update -----#

    def _update_player_animations(self):
        self.player_sprite.can_jump = not self.physics_engine.can_jump()

        self.player_sprite.is_on_ladder = (self.physics_engine.is_on_ladder() 
                                           and not self.physics_engine.can_jump())

        self.process_keychange()

    def _update_shoot_animations(self):
        if not self.can_shoot:
            self.shoot_timer += 1
            if self.shoot_timer == SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0
            return
        
        if not self.shoot_pressed: 
            return

        arcade.play_sound(self.shoot_sound)
        bullet = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png",
            SPRITE_SCALING_LASER,
        )

        if self.player_sprite.facing_direction == RIGHT_FACING:
            bullet.change_x = BULLET_SPEED
        else:
            bullet.change_x = -BULLET_SPEED

        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y

        self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

        self.can_shoot = False

    def _update_layers(self, time):
        self.scene.update_animation(
            time,
            [
                LAYER_NAME_PLAYER,
                LAYER_NAME_ENEMIES
            ],
        )

        self.scene.update(
            [
                LAYER_NAME_MOVING_PLATFORMS,
                LAYER_NAME_ENEMIES,
                LAYER_NAME_BULLETS
            ]
        )

    def _update_moving_walls(self):
        for wall in self.scene[LAYER_NAME_MOVING_PLATFORMS]:
            horizontal_flip = bool(wall.change_x) and (
                (wall.right > wall.boundary_right and wall.change_x > 0)
                or
                (wall.left < wall.boundary_left and wall.change_x < 0)
            )

            vertical_flip = bool(wall.change_y) and (
                (wall.top > wall.boundary_top and wall.change_y > 0)
                or
                (wall.bottom < wall.boundary_bottom and wall.change_y < 0)
            )

            if horizontal_flip:
                wall.change_x *= -1

            if vertical_flip:
                wall.change_y *= -1

    def _update_moving_enemies(self):
        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            flip = (
                (enemy.right > enemy.boundary_right and enemy.change_x > 0)
                or
                (enemy.left < enemy.boundary_left and enemy.change_x < 0)
            )

            if flip:
                enemy.change_x *= -1

    def _process_bullet_collision(self):
        for bullet in self.scene[LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene[LAYER_NAME_ENEMIES],
                    self.scene[LAYER_NAME_PLATFORMS],
                    self.scene[LAYER_NAME_MOVING_PLATFORMS]
                ]
            )

            if (bullet.right < 0) or (bullet.left > 
               (self.tile_map.width * SPRITE_PIXEL_SIZE) * TILE_SCALING):
                bullet.remove_from_sprite_lists()
                return
            
            if not hit_list:
                return

            bullet.remove_from_sprite_lists()
            for collision in hit_list:
                if not (self.scene[LAYER_NAME_ENEMIES]
                        in collision.sprite_lists):
                    continue
                
                collision.health -= BULLET_DAMAGE
                if collision.health <= 0:
                    collision.remove_from_sprite_lists()
                    self.score += 15
                arcade.play_sound(self.hit_sound)

    def _process_death(self):
        arcade.play_sound(self.death_sound)

        if self.lives == 1:
            self.window.views['ending'].success = False
            self.window.show_view(self.window.views['ending'])
            return
        
        self.reset_score = False
        self.lives -= 1
        self.setup()

    def _process_finish(self):
        if self.level == LEVELS_COUNT:
            self.window.views['ending'].success = True
            self.window.show_view(self.window.views['ending'])
            return

        self.level += 1
        self.reset_score = False
        self.setup()

    def _process_coin_pick_up(self, coll):
        points = int(coll.properties["Points"])
        self.score += points
        coll.remove_from_sprite_lists()
        arcade.play_sound(self.coin_sound)

    def _process_key_pick_up(self, coll):
        self.keys.append(coll.properties["color"])
        coll.remove_from_sprite_lists()

    def _process_lock_collision(self, coll):
        if coll.properties["color"] not in self.keys:
            return
        
        self.keys.remove(coll.properties["color"])
        coll.remove_from_sprite_lists()
        self.lock_pairs[coll.properties["color"]].remove_from_sprite_lists()

    def _process_player_collision(self):
        collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite, 
            [
                self.scene[LAYER_NAME_DEATH],
                self.scene[LAYER_NAME_ENEMIES],
                self.scene[LAYER_NAME_FINISH],
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_KEYS],
                self.scene[LAYER_NAME_LOCKS]
            ]
        )

        for collision in collision_list:
            if (self.scene[LAYER_NAME_DEATH] in collision.sprite_lists or 
                self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists):
                self._process_death()  
            elif self.scene[LAYER_NAME_FINISH] in collision.sprite_lists:
                self._process_finish()
            elif self.scene[LAYER_NAME_COINS] in collision.sprite_lists:
                self._process_coin_pick_up(collision)
            elif self.scene[LAYER_NAME_KEYS] in collision.sprite_lists:
                self._process_key_pick_up(collision)
            elif self.scene[LAYER_NAME_LOCKS] in collision.sprite_lists:
                self._process_lock_collision(collision)

    def _center_camera_to_player(self):
        screen_center_x = (
            self.player_sprite.center_x - self.camera.viewport_width / 2)
        screen_center_y = (
            self.player_sprite.center_y - self.camera.viewport_height / 2)
        
        screen_center_x = 0 if screen_center_x < 0 else screen_center_x
        screen_center_y = 0 if screen_center_y < 0 else screen_center_y

        if screen_center_x > (self.end_of_map - self.camera.viewport_width):
            screen_center_x = (self.end_of_map - self.camera.viewport_width)
        
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    #-----------------------------------------#

    def on_update(self, delta_time):
        self.physics_engine.update()

        self._update_player_animations()
        self._update_shoot_animations()

        self._update_layers(delta_time)

        self._update_moving_walls()
        self._update_moving_enemies()

        self._process_bullet_collision()
        self._process_player_collision()
        
        if self.player_sprite.center_y < -100:
            self._process_death()

        self._center_camera_to_player()
