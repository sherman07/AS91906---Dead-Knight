import arcade
import os
import time

# Constants
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 3.5
TILE_SCALING = 1.5
CHARACTER_SCALING = 2
UPDATES_PER_FRAME = 5

# Health bar constants
HEALTHBAR_WIDTH = 100
HEALTHBAR_HEIGHT = 15
HEALTHBAR_OFFSET_Y = 50
HEALTH_NUMBER_OFFSET = 10

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
        self.facing_direction = DIRECTION_RIGHT
        self.is_attacking = False
        self.current_attack = 0 
        self.attack_cooldown = 0
        self.combo_window = 0.3
        self.can_combo = False
        
        # Dash properties
        self.is_dashing = False
        self.dash_cooldown = 0
        self.dash_duration = 0.2
        self.dash_speed = 9
        self.dash_cooldown_time = 0.5
        self.dash_start_time = 0
        self.original_speed = PLAYER_SPEED
        
        # Hurt/death properties
        self.is_hurt = False
        self.hurt_start_time = 0
        self.hurt_duration = 0.5
        self.hurt_count = 0
        self.max_hits_before_death = 5
        self.is_dead = False
        self.invincible = False
        self.invincibility_duration = 1.0
        self.last_hurt_time = 0

        self.heal_amount = 1
        self.heal_cooldown = 0
        self.heal_cooldown_time = 1.0
        self.is_healing = False
        self.heal_start_time = 0
        self.heal_duration = 0.5

        dir_name = os.path.dirname(os.path.abspath(__file__))
        character_path = os.path.join(dir_name, "knight_character", "knight")

        # Load all textures
        self.idle_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }
        self.walk_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }
        self.attack_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }
        self.attack2_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }
        self.dash_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }

        self.death_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }

        self.hurt_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }

        self.heal_textures = {
            DIRECTION_RIGHT: [],
            DIRECTION_LEFT: [],
            DIRECTION_UP: [],
            DIRECTION_DOWN: []
        }

        for i in range(12):
            self.heal_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_heal{i}.png"))
            self.heal_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_heal{i}.png"))
            self.heal_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_heal{i}.png"))
            self.heal_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_heal{i}.png"))

        # Load 7-frame animations
        for i in range(7):
            self.idle_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_idle{i}.png"))
            self.idle_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_idle{i}.png"))
            self.idle_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_idle{i}.png"))
            self.idle_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_idle{i}.png"))
            
            self.walk_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_run{i}.png"))
            self.walk_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_run{i}.png"))
            self.walk_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_run{i}.png"))
            self.walk_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_run{i}.png"))
            
            self.attack_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_attack{i}.png"))
            self.attack_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_attack{i}.png"))
            self.attack_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_attack{i}.png"))
            self.attack_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_attack{i}.png"))
            
            self.attack2_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_attack2_{i}.png"))
            self.attack2_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_attack2_{i}.png"))
            self.attack2_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_attack2_{i}.png"))
            self.attack2_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_attack2_{i}.png"))
            
            self.dash_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_dash{i}.png"))
            self.dash_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_dash{i}.png"))
            self.dash_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_dash{i}.png"))
            self.dash_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_dash{i}.png"))
                        
            self.death_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_death{i}.png"))
            self.death_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_death{i}.png"))
            self.death_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_death{i}.png"))
            self.death_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_death{i}.png"))

        for i in range(4):
            # Hurt and death animations (assuming same 7 frames)
            self.hurt_textures[DIRECTION_RIGHT].append(arcade.load_texture(f"{character_path}_right_hurt{i}.png"))
            self.hurt_textures[DIRECTION_LEFT].append(arcade.load_texture(f"{character_path}_left_hurt{i}.png"))
            self.hurt_textures[DIRECTION_UP].append(arcade.load_texture(f"{character_path}_up_hurt{i}.png"))
            self.hurt_textures[DIRECTION_DOWN].append(arcade.load_texture(f"{character_path}_down_hurt{i}.png"))

        super().__init__(self.idle_textures[DIRECTION_RIGHT][0], scale=CHARACTER_SCALING)

    def character_animation(self, delta_time: float = 1 / 60):
        if self.is_dead:
            if not hasattr(self, 'death_start_time'):
                self.death_start_time = time.time()
                
            elapsed = time.time() - self.death_start_time
            death_duration = 1.0  # 1 second for full death animation
            death_frames = len(self.death_textures[self.facing_direction])
            
            # Calculate current frame
            if elapsed < death_duration:
                frame = min(int(elapsed / death_duration * death_frames), death_frames - 1)
                self.texture = self.death_textures[self.facing_direction][frame]
            else:
                # After animation completes, stay on last frame
                frame = death_frames - 1
                self.texture = self.death_textures[self.facing_direction][frame]
            return
        
        if self.heal_cooldown > 0:
            self.heal_cooldown -= delta_time
        
        if self.is_healing:
            elapsed = time.time() - self.heal_start_time
            if elapsed >= self.heal_duration:
                self.is_healing = False
                self.cur_texture = 0
            else:
                frame = min(int(elapsed / self.heal_duration * len(self.heal_textures[self.facing_direction])), 
                           len(self.heal_textures[self.facing_direction]) - 1)
                self.texture = self.heal_textures[self.facing_direction][frame]
            return
            
        # Hurt animation comes next
        if self.is_hurt:
            elapsed = time.time() - self.hurt_start_time
            if elapsed >= self.hurt_duration:
                self.is_hurt = False
                self.cur_texture = 0
            else:
                frame = min(int(elapsed / self.hurt_duration * len(self.hurt_textures[self.facing_direction])), 
                           len(self.hurt_textures[self.facing_direction]) - 1)
                self.texture = self.hurt_textures[self.facing_direction][frame]
            return

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

        # Handle dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= delta_time

        # Dash animation and movement
        if self.is_dashing:
            self.cur_texture += 1
            dash_frames = len(self.dash_textures[self.facing_direction]) * UPDATES_PER_FRAME
            
            if (time.time() - self.dash_start_time) >= self.dash_duration or self.cur_texture >= dash_frames:
                self.is_dashing = False
                self.cur_texture = 0
                self.change_x = 0
                self.change_y = 0
            else:
                frame = min(self.cur_texture // UPDATES_PER_FRAME, 
                           len(self.dash_textures[self.facing_direction]) - 1)
                self.texture = self.dash_textures[self.facing_direction][frame]
            return

        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        # Attack animation logic
        if self.current_attack > 0:
            self.cur_texture += 1
            
            attack_textures = self.attack_textures if self.current_attack == 1 else self.attack2_textures
            attack_frames = 5 * UPDATES_PER_FRAME
            
            if self.cur_texture >= attack_frames:
                self.current_attack = 0
                self.cur_texture = 0
                self.attack_cooldown = 0.1
            else:
                frame = min(self.cur_texture // UPDATES_PER_FRAME, 6)
                self.texture = attack_textures[self.facing_direction][frame]
            
            if self.cur_texture >= 3 * UPDATES_PER_FRAME:
                self.can_combo = True
            return

        # Movement animations
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
    
    def heal(self):
        if (not self.is_dead and not self.is_healing 
            and not self.is_hurt and not self.is_dashing 
            and self.current_attack == 0 and self.heal_cooldown <= 0):
            
            self.is_healing = True
            self.heal_start_time = time.time()
            self.heal_cooldown = self.heal_cooldown_time
            self.hurt_count = max(0, self.hurt_count - self.heal_amount)
            self.change_x = 0
            self.change_y = 0

    def attack(self):
        if not self.is_dead and self.current_attack == 0 and self.attack_cooldown <= 0:
            self.current_attack = 1
            self.cur_texture = 0
            self.can_combo = False
        elif not self.is_dead and self.current_attack == 1 and self.can_combo:
            self.current_attack = 2
            self.cur_texture = 0
            self.can_combo = False
        elif not self.is_dead and self.current_attack == 2 and self.can_combo:
            self.current_attack = 1
            self.cur_texture = 0
            self.can_combo = False

    def dash(self):
        if not self.is_dead and not self.is_dashing and self.dash_cooldown <= 0 and self.current_attack == 0:
            self.is_dashing = True
            self.dash_cooldown = self.dash_cooldown_time
            self.cur_texture = 0
            self.dash_start_time = time.time()
            
            if self.facing_direction == DIRECTION_RIGHT:
                self.change_x = self.dash_speed
                self.change_y = 0
            elif self.facing_direction == DIRECTION_LEFT:
                self.change_x = -self.dash_speed
                self.change_y = 0
            elif self.facing_direction == DIRECTION_UP:
                self.change_x = 0
                self.change_y = self.dash_speed
            elif self.facing_direction == DIRECTION_DOWN:
                self.change_x = 0
                self.change_y = -self.dash_speed

    def hurt(self, damage_amount=1):
        current_time = time.time()
        if (not self.is_dead and not self.is_hurt 
            and not self.is_dashing and not self.is_healing
            and self.current_attack == 0 
            and current_time - self.last_hurt_time > self.invincibility_duration
            and not self.invincible):
            
            self.is_hurt = True
            self.hurt_start_time = current_time
            self.last_hurt_time = current_time
            self.hurt_count += damage_amount
            self.change_x = 0
            self.change_y = 0
            
            # Knockback effect
            if self.facing_direction == DIRECTION_RIGHT:
                self.center_x -= 20
            elif self.facing_direction == DIRECTION_LEFT:
                self.center_x += 20
            elif self.facing_direction == DIRECTION_UP:
                self.center_y -= 20
            elif self.facing_direction == DIRECTION_DOWN:
                self.center_y += 20
                
            if self.hurt_count >= self.max_hits_before_death:
                self.die()

    def die(self):
        self.is_dead = True
        self.death_start_time = time.time()
        self.change_x = 0
        self.change_y = 0
        self.is_dashing = False
        self.current_attack = 0
        self.cur_texture = 0
        self.texture = self.death_textures[self.facing_direction][0]


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.scene = None
        self.player = None
        self.camera = None
        self.physics_engine = None
        self.held_keys = set()
        self.peak_list = None
        self.last_damage_time = 0
        self.damage_cooldown = 0.5
        self.flash_red = False
        self.flash_end_time = 0

    def setup(self):
        map_path = os.path.join(os.path.dirname(__file__), "Level_01.tmx")
        tilemap = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options={
                "Walls": {"use_spatial_hash": True},
                "Collision Items": {"use_spatial_hash": True},
                "Non Collision Items": {},
                "Peaks": {}  # Enable spatial hash for performance
            }
        )

        self.scene = arcade.Scene.from_tilemap(tilemap)

        self.player = PlayerCharacter()
        self.player.center_x = 1700
        self.player.center_y = 350
        self.scene.add_sprite("Player", self.player)

        walls_and_collision_items = arcade.SpriteList()
        walls_and_collision_items.extend(self.scene["Walls"])
        walls_and_collision_items.extend(self.scene["Collision Items"])

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, 
            walls_and_collision_items
        )
        self.camera = arcade.Camera2D()

        if "Peaks" in tilemap.sprite_lists:
            self.peak_list = tilemap.sprite_lists["Peaks"]
            # Set damage properties for all peak tiles
            for peak in self.peak_list:
                peak.properties = {"damage": True, "damage_amount": 1}
            self.scene.add_sprite_list("Peaks", sprite_list=self.peak_list)
        else:
            self.peak_list = arcade.SpriteList()


    def draw_health_bar(self):
    # Calculate positions - bottom left corner of the health bar
        bar_left = self.player.center_x - HEALTHBAR_WIDTH / 2
        bar_bottom = self.player.center_y + HEALTHBAR_OFFSET_Y - HEALTHBAR_HEIGHT / 2
        
        # Draw background of health bar (empty)
        arcade.draw_lbwh_rectangle_filled(
            bar_left,
            bar_bottom,
            HEALTHBAR_WIDTH,
            HEALTHBAR_HEIGHT,
            arcade.color.RED
        )
        
        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (1 - self.player.hurt_count / self.player.max_hits_before_death)
        
        # Draw filled part of health bar
        arcade.draw_lbwh_rectangle_filled(
            bar_left,
            bar_bottom,
            health_width,
            HEALTHBAR_HEIGHT,
            arcade.color.GREEN
        )
        
        # Draw health number
        health_text = f"{self.player.max_hits_before_death - self.player.hurt_count}/{self.player.max_hits_before_death}"
        arcade.draw_text(
            health_text,
            self.player.center_x,
            self.player.center_y + HEALTHBAR_OFFSET_Y,
            arcade.color.WHITE,
            12,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.draw_health_bar()

    def on_update(self, delta_time):
        # Don't process movement if dead
        if self.player.is_dead:
            self.player.change_x = 0
            self.player.change_y = 0
        else:
            # Reset movement if not dashing or hurt
            if not self.player.is_dashing and not self.player.is_healing and not self.player.is_hurt:
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
        self.scene.update_animation(delta_time)
        self.player.character_animation(delta_time)
        self.camera.position = self.player.position

        if not self.player.is_dead:
            current_time = time.time()
            if current_time - self.last_damage_time > self.damage_cooldown:
                peaks_hit = arcade.check_for_collision_with_list(self.player, self.peak_list)
                if peaks_hit:
                    self.last_damage_time = current_time
                    self.player.hurt()
                    self.flash_red = True
                    self.flash_end_time = current_time + 0.2  # Flash for 0.2 seconds

        self.camera.position = self.player.position

    def on_key_press(self, key, modifiers):
        self.held_keys.add(key)
        if key == arcade.key.SPACE:
            self.player.attack()
        elif key == arcade.key.LSHIFT:  # Left Shift for dash
            self.player.dash()
        elif key == arcade.key.F:  # F key for hurt animation
            self.player.hurt()
        elif key == arcade.key.E:  # Heal button
            self.player.heal()

    def on_key_release(self, key, modifiers):
        self.held_keys.discard(key)

if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()