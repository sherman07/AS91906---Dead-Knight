import arcade
import os

# Constants
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 3
TILE_SCALING = 1
CHARACTER_SCALING = 1.3
UPDATES_PER_FRAME = 5

# Movement directions
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        self.cur_texture = 0
        self.direction = DIRECTION_DOWN  # Default facing

        dir_name = os.path.dirname(os.path.abspath(__file__))
        character_path = os.path.join(dir_name, "knight_character", "knight")

        # Load idle textures (5 frames)
        self.idle_textures = {
            DIRECTION_UP: [],
            DIRECTION_DOWN: [],
            DIRECTION_LEFT: [],
            DIRECTION_RIGHT: []
        }
        for i in range(5):
            texture_path_idle = f"{character_path}_idle{i}.png"
            texture = arcade.load_texture(texture_path_idle)
            self.idle_textures[DIRECTION_RIGHT].append(texture)
            self.idle_textures[DIRECTION_LEFT].append(texture)
            self.idle_textures[DIRECTION_UP].append(texture)
            self.idle_textures[DIRECTION_DOWN].append(texture)

        # Load walk textures (7 frames)
        self.walk_textures = {
            DIRECTION_UP: [],
            DIRECTION_DOWN: [],
            DIRECTION_LEFT: [],
            DIRECTION_RIGHT: []
        }
        
        for i in range(7):
            texture_path_walk = f"{character_path}_walk{i}.png"
            texture = arcade.load_texture(texture_path_walk)
            self.walk_textures[DIRECTION_RIGHT].append(texture)
            self.walk_textures[DIRECTION_LEFT].append(texture)
            self.walk_textures[DIRECTION_UP].append(texture)
            self.walk_textures[DIRECTION_DOWN].append(texture)

        super().__init__(self.idle_textures[DIRECTION_DOWN][0], scale=CHARACTER_SCALING)

    def update_animation(self, delta_time: float = 1 / 60):
        # Detect direction
        if self.change_y > 0:
            self.direction = DIRECTION_UP
        elif self.change_y < 0:
            self.direction = DIRECTION_DOWN
        elif self.change_x < 0:
            self.direction = DIRECTION_LEFT
        elif self.change_x > 0:
            self.direction = DIRECTION_RIGHT

        self.cur_texture += 1

        if self.change_x == 0 and self.change_y == 0:
            # Animate idle (5 frames)
            if self.cur_texture >= 5 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.idle_textures[self.direction][frame]
        else:
            # Animate walking (7 frames)
            if self.cur_texture >= 7 * UPDATES_PER_FRAME:
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

        # Track which keys are being held down
        self.held_keys = set()

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
        self.player.center_x = 1200
        self.player.center_y = 300
        self.scene.add_sprite("Player", self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene["Walls"])
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time):
        # Reset movement each frame
        self.player.change_x = 0
        self.player.change_y = 0

        # Apply movement based on held keys
        if arcade.key.W in self.held_keys:
            self.player.change_y = PLAYER_SPEED
        if arcade.key.S in self.held_keys:
            self.player.change_y = -PLAYER_SPEED
        if arcade.key.A in self.held_keys:
            self.player.change_x = -PLAYER_SPEED
        if arcade.key.D in self.held_keys:
            self.player.change_x = PLAYER_SPEED

        self.physics_engine.update()
        self.player.update_animation(delta_time)
        self.camera.position = self.player.position

    def on_key_press(self, key, modifiers):
        self.held_keys.add(key)

    def on_key_release(self, key, modifiers):
        self.held_keys.discard(key)

if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
