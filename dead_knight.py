import arcade
import os

# Constants
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 3
TILE_SCALING = 1
CHARACTER_SCALING = 1.35
UPDATES_PER_FRAME = 5

# Directions
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.cur_texture = 0
        self.direction = DIRECTION_DOWN
        self.facing_direction = DIRECTION_RIGHT  # For attack only
        self.is_attacking = False
        self.current_attack = 0  # 0 = none, 1 = attack1, 2 = attack2
        self.attack_cooldown = 0
        self.combo_window = 0.3  # Time to chain next attack

        dir_name = os.path.dirname(os.path.abspath(__file__))
        character_path = os.path.join(dir_name, "knight_character", "knight")

        # Load idle textures
        self.idle_textures = {
            DIRECTION_UP: [],
            DIRECTION_DOWN: [],
            DIRECTION_RIGHT: [],
            DIRECTION_LEFT: []
        }
        for i in range(7):
            self.idle_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_idle{i}.png"))
            self.idle_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_idle{i}.png"))
            self.idle_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_idle{i}.png"))
            self.idle_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_idle{i}.png"))

        # Load walk textures
        self.walk_textures = {
            DIRECTION_RIGHT: [],
            DIRECTION_LEFT: [],
            DIRECTION_UP: [],
            DIRECTION_DOWN: []
        }
        for i in range(7):
            self.walk_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_run{i}.png"))
            self.walk_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_run{i}.png"))
            self.walk_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_run{i}.png"))
            self.walk_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_run{i}.png"))

        # Load attack textures (only left/right)
        self.attack_textures = {
            DIRECTION_RIGHT: [],
            DIRECTION_LEFT: [],
            DIRECTION_UP: [],
            DIRECTION_DOWN: []
        }
        self.attack2_textures = {
            DIRECTION_RIGHT: [],
            DIRECTION_LEFT: [],
            DIRECTION_UP: [],
            DIRECTION_DOWN: []
        }
        for i in range(7):
            self.attack_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_attack{i}.png"))
            self.attack_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_attack{i}.png"))
            self.attack_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_attack{i}.png"))
            self.attack_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_attack{i}.png"))
            
             # Second attack animation
            self.attack2_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_attack2_{i}.png"))
            self.attack2_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_attack2_{i}.png"))
            self.attack2_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_attack2_{i}.png"))
            self.attack2_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_attack2_{i}.png"))

        super().__init__(self.idle_textures[DIRECTION_RIGHT][0], scale=CHARACTER_SCALING)

    def character_animation(self, delta_time: float = 1 / 60):
        # Update direction based on movement
        if self.change_y > 0:
            self.direction = DIRECTION_UP
            self.facing_direction = DIRECTION_UP
        elif self.change_y < 0:
            self.direction = DIRECTION_DOWN
            self.facing_direction = DIRECTION_DOWN
        elif self.change_x < 0:
            self.direction = DIRECTION_LEFT
            self.facing_direction = DIRECTION_LEFT
        elif self.change_x > 0:
            self.direction = DIRECTION_RIGHT
            self.facing_direction = DIRECTION_RIGHT

       # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        # Attack animation logic
        if self.current_attack > 0:
            self.cur_texture += 1
            
            # Determine which attack animation to use
            attack_textures = self.attack_textures if self.current_attack == 1 else self.attack2_textures
            attack_frames = 5 * UPDATES_PER_FRAME  # 5 frames per attack
            
            # Check if attack animation is complete
            if self.cur_texture >= attack_frames:
                self.current_attack = 0
                self.cur_texture = 0
                self.attack_cooldown = 0.1  # Small cooldown between attacks
            else:
                frame = min(self.cur_texture // UPDATES_PER_FRAME, 6)
                self.texture = attack_textures[self.facing_direction][frame]
            
            # Enable combo during last part of attack
            if self.cur_texture >= 3 * UPDATES_PER_FRAME:
                self.can_combo = True
            return

        # Movement animations (only if not attacking)
        self.cur_texture += 1
        if self.change_x == 0 and self.change_y == 0:
            if self.cur_texture >= 7 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.idle_textures[self.direction][frame]
        else:
            if self.cur_texture >= 7 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.walk_textures[self.direction][frame]

    def attack(self):
        if self.current_attack == 0 and self.attack_cooldown <= 0:
            # Start first attack
            self.current_attack = 1
            self.cur_texture = 0
            self.can_combo = False
        elif self.current_attack == 1 and self.can_combo:
            # Chain into second attack
            self.current_attack = 2
            self.cur_texture = 0
            self.can_combo = False
        elif self.current_attack == 2 and self.can_combo:
            # Reset back to first attack
            self.current_attack = 1
            self.cur_texture = 0
            self.can_combo = False


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.scene = None
        self.player = None
        self.camera = None
        self.physics_engine = None
        self.held_keys = set()

    def setup(self):
        map_path = os.path.join(os.path.dirname(__file__), "Level_01.tmx")
        tilemap = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options={"Walls": {"use_spatial_hash": True}}
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
        self.player.change_x = 0
        self.player.change_y = 0

        if self.player.current_attack == 0:  # Only move when not attacking
            if arcade.key.W in self.held_keys or arcade.key.UP in self.held_keys:
                self.player.change_y = PLAYER_SPEED
            if arcade.key.S in self.held_keys or arcade.key.DOWN in self.held_keys:
                self.player.change_y = -PLAYER_SPEED
            if arcade.key.A in self.held_keys or arcade.key.LEFT in self.held_keys:
                self.player.change_x = -PLAYER_SPEED
            if arcade.key.D in self.held_keys or arcade.key.RIGHT in self.held_keys:
                self.player.change_x = PLAYER_SPEED


        self.physics_engine.update()
        self.player.character_animation(delta_time)
        self.camera.position = self.player.position

    def on_key_press(self, key, modifiers):
        self.held_keys.add(key)
        if key == arcade.key.SPACE:
            self.player.attack()

    def on_key_release(self, key, modifiers):
        self.held_keys.discard(key)

if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()


