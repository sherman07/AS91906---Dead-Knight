import arcade
import os

# The constants for Dead Knight Top down game
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 3
TILE_SCALING = 1
CHARACTER_SCALING = 1
UPDATES_PER_FRAME = 5

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        self.cur_texture = 0
        self.direction = DIRECTION_DOWN  # Default facing

        dir_name = os.path.dirname(os.path.abspath(__file__))
        character_path = dir_name + "/knight_character/knight"  # Replace with your own sprite path
        print(f"CHARACTER PATH: {character_path}")

        # Load idle textures
        self.idle_textures = {
            DIRECTION_UP: arcade.load_texture(f"{character_path}_idle.png"),
            DIRECTION_DOWN: arcade.load_texture(f"{character_path}_idle.png"),
            DIRECTION_LEFT: arcade.load_texture(f"{character_path}_idle.png"),
            DIRECTION_RIGHT: arcade.load_texture(f"{character_path}_idle.png")
        }

        # Load walk textures
        self.walk_textures = {
            DIRECTION_UP: [],
            DIRECTION_DOWN: [],
            DIRECTION_LEFT: [],
            DIRECTION_RIGHT: []
        }
        for i in range(4):
            self.walk_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_walk{i}.png"))
            self.walk_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_walk{i}.png"))
            self.walk_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_walk{i}.png"))
            self.walk_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_walk{i}.png"))

        super().__init__(self.idle_textures[DIRECTION_DOWN], scale=CHARACTER_SCALING)

    def update_animation(self, delta_time: float = 1 / 60):
        # Detect direction based on movement
        if self.change_y > 0:
            self.direction = DIRECTION_UP
        elif self.change_y < 0:
            self.direction = DIRECTION_DOWN
        elif self.change_x < 0:
            self.direction = DIRECTION_LEFT
        elif self.change_x > 0:
            self.direction = DIRECTION_RIGHT

        # Idle
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.direction]
            return

        # Walk animation
        self.cur_texture += 1
        if self.cur_texture >= 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.walk_textures[self.direction][frame]


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.scene = None
        self.player = None
        self.camera = None
        self.physics_engine = None

    def setup(self):
        map_path = os.path.join(os.path.dirname(__file__), "Level_01.tmx")

        tilemap = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options={
                "Walls": {"use_spatial_hash": True}
            }
        )
        self.scene = arcade.Scene.from_tilemap(tilemap)

        self.player = PlayerCharacter()
        self.player.center_x = 400
        self.player.center_y = 300
        self.scene.add_sprite("Player", self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene["Walls"])
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player.update_animation(delta_time)
        self.camera.position = self.player.position

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
