import arcade
import os
import time
import sys


# GLOBAL CONSTANTS
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 5.5
PLAYER_SPEED_BOOST = 10.0
PLAYER_DASH_BOOST = 15.0
TILE_SCALING = 1.5
CHARACTER_SCALING = 2
UPDATES_PER_FRAME = 5
MAX_LEVEL = 3
KEY_COUNT = 6

# Health bar constants
HEALTHBAR_WIDTH = 100
HEALTHBAR_HEIGHT = 15
HEALTHBAR_OFFSET_Y = 50
HEALTH_NUMBER_OFFSET = 10

# Direction constants for player facing
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

# Character frame constants
HEAL_FRAMES = 12
IDLE_WALK_RUN_DEATH_FRAMES = 7

class PlayerCharacter(arcade.Sprite):
    """
    Present the player character with animation states and abilities
    like dashing, healing, and taking damage.
    
    Attributes:
        cur_texture (int): Current frame in animation sequence
        direction (int): Current movement direction
        facing_direction (int): Direction character is facing
        Various state flags (is_dashing, is_hurt, etc.)
        Animation texture dictionaries for different states
    """
    
    def __init__(self):
        """Initialize player with default state and load animation."""
        
        super().__init__()
        
        # Animation control
        self.cur_texture = 0
        self.direction = DIRECTION_DOWN
        self.facing_direction = DIRECTION_RIGHT
        
        # Dash ability properties
        self.is_dashing = False
        self.dash_cooldown = 0
        self.dash_duration = 0.2
        self.dash_speed = 13
        self.dash_cooldown_time = 0.5
        self.dash_start_time = 0
        self.original_speed = PLAYER_SPEED
        
        # Health/damage properties
        self.is_hurt = False
        self.hurt_start_time = 0
        self.hurt_duration = 0.5
        self.hurt_count = 0
        self.max_hits_before_death = 5
        self.is_dead = False
        self.invincible = False
        self.invincibility_duration = 1.0
        self.last_hurt_time = 0

        # Healing properties
        self.heal_amount = 1
        self.heal_cooldown = 0
        self.is_healing = False
        self.heal_start_time = 0
        self.heal_duration = 0.5

        # Speed boost properties
        self.is_speed_boosted = False
        self.speed_boost_start_time = 0
        self.speed_boost_duration = 4.0
        self.speed_multiplier = 1.5
        
        # Death state
        self.death_completed = False
        self.death_complete_time = 0
        
        # Load textures from files
        self._load_textures()
        
        # Set initial texture
        super().__init__(
            self.idle_textures[DIRECTION_RIGHT][0],
            scale=CHARACTER_SCALING
        )

    def _load_textures(self):
        """Load all animation textures from the Dead Knight File."""
        
        dir_name = os.path.dirname(os.path.abspath(__file__))
        character_path = os.path.join(dir_name, "knight_character",\
            "knight")

        # Initialize texture dictionaries
        self.idle_textures = {
            DIRECTION_UP: [], DIRECTION_DOWN: [], 
            DIRECTION_RIGHT: [], DIRECTION_LEFT: []
        }
        self.walk_textures = {
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
            DIRECTION_RIGHT: [], DIRECTION_LEFT: [],
            DIRECTION_UP: [], DIRECTION_DOWN: []
        }

        # Load healing textures (12 frames)
        for i in range(HEAL_FRAMES):
            self.heal_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_heal{i}.png")
            )
            self.heal_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_heal{i}.png")
            )
            self.heal_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_heal{i}.png")
            )
            self.heal_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_heal{i}.png")
            )

        # Load 7 frame animations (idle, walk, dash, death)
        for i in range(IDLE_WALK_RUN_DEATH_FRAMES):
            
            # Idle animations
            self.idle_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_idle{i}.png")
            )
            self.idle_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_idle{i}.png")
            )
            self.idle_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_idle{i}.png")
            )
            self.idle_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_idle{i}.png")
            )
            
            # Walk animations
            self.walk_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_run{i}.png")
            )
            self.walk_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_run{i}.png")
            )
            self.walk_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_run{i}.png")
            )
            self.walk_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_run{i}.png")
            )
            
            # Dash animations
            self.dash_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_dash{i}.png")
            )
            self.dash_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_dash{i}.png")
            )
            self.dash_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_dash{i}.png")
            )
            self.dash_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_dash{i}.png")
            )
            
            # Death animations
            self.death_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_death{i}.png")
            )
            self.death_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_death{i}.png")
            )
            self.death_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_death{i}.png")
            )
            self.death_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_death{i}.png")
            )
        
        # Load hurt animations (4 frames)
        for i in range(4):
            self.hurt_textures[DIRECTION_RIGHT].append(
                arcade.load_texture(f"{character_path}_right_hurt{i}.png")
            )
            self.hurt_textures[DIRECTION_LEFT].append(
                arcade.load_texture(f"{character_path}_left_hurt{i}.png")
            )
            self.hurt_textures[DIRECTION_UP].append(
                arcade.load_texture(f"{character_path}_up_hurt{i}.png")
            )
            self.hurt_textures[DIRECTION_DOWN].append(
                arcade.load_texture(f"{character_path}_down_hurt{i}.png")
            )

    def character_animation(self, delta_time: float = 1 / 60):
        """
        Update character animation based on current state.
        
        Args:
            delta_time (float): Time since last update
        """
        
        # Handle death animation
        if self.is_dead:
            self._handle_death_animation()
            return
        
        # Update cooldowns
        if self.heal_cooldown > 0:
            self.heal_cooldown -= delta_time
        
        # Handle healing animation
        if self.is_healing:
            self._handle_healing_animation()
            return
            
        # Handle hurt animation
        if self.is_hurt:
            self._handle_hurt_animation()
            return

        # Update facing direction based on movement
        self._update_facing_direction()

        # Update dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= delta_time

        # Handle dash animation
        if self.is_dashing:
            self._handle_dash_animation()
            return

        # Handle regular movement animations
        self._handle_standard_animation()
        
    def _handle_death_animation(self):
        """
        Manage death animation sequence.
        
        This method will:
        1. Initializes death timing on first call
        2. Calculates elapsed time since death started
        3. Determines current animation frame based on progress
        4. Sets final frame and marks death completion
        """
        
        # Initialize death timing if first frame of death animation
        if not hasattr(self, 'death_start_time'):
            self.death_start_time = time.time()
            self.death_completed = False
        
        # Calculate animation progress from 0.0 to 1.0
        elapsed = time.time() - self.death_start_time
        death_duration = 1.0  # Total time for death animation
        
        # Get number of frames in death animation for current direction
        death_frames = len(self.death_textures[self.facing_direction])
        
        if elapsed < death_duration:
            
            # Calculate current frame based on progress through 
            # animation
            frame = min(
                int(elapsed / death_duration * death_frames), 
                death_frames - 1
            )
            
            # Set texture to current death animation frame
            self.texture = self.death_textures[self.facing_direction][frame]
            
        else:
            
            # Animation complete - show final frame
            frame = death_frames - 1
            self.texture = self.death_textures[self.facing_direction][frame]
            
            # Mark death as completed if not already done
            if not self.death_completed:
                self.death_completed = True
                self.death_complete_time = time.time()

    def _handle_healing_animation(self):
        """
        Manage healing animation sequence.
        
        This method:
        1. Calculates elapsed time since healing started
        2. Ends animation when duration is reached
        3. Determines current frame based on progress
        4. Updates character texture
        """
        
        # Calculate time since healing started
        elapsed = time.time() - self.heal_start_time
        
        # Check if healing animation duration has completed
        if elapsed >= self.heal_duration:
            
            # Reset animation state
            self.is_healing = False
            self.cur_texture = 0
            
        else:
            
            # Calculate current animation frame
            num_frames = len(self.heal_textures[self.facing_direction])
            frame = min(
                int(elapsed / self.heal_duration * num_frames),
                num_frames - 1
            )
            
            # Update to current healing frame
            self.texture = self.heal_textures[self.facing_direction][frame]

    def _handle_hurt_animation(self):
        """
        Manage hurt animation sequence.
        
        This method:
        1. Calculates elapsed time since damage taken
        2. Ends animation when duration is reached
        3. Determines current frame based on progress
        4. Updates character texture
        """
        
        # Calculate time since hurt started
        elapsed = time.time() - self.hurt_start_time
        
        # Check if hurt animation duration has completed
        if elapsed >= self.hurt_duration:
            
            # Reset animation state
            self.is_hurt = False
            self.cur_texture = 0
            
        else:
            
            # Calculate current animation frame
            num_frames = len(self.hurt_textures[self.facing_direction])
            frame = min(
                int(elapsed / self.hurt_duration * num_frames),
                num_frames - 1
            )
            
            # Update to current hurt frame
            self.texture = self.hurt_textures[self.facing_direction][frame]

    def _update_facing_direction(self):
        """
        Update character's facing direction based on movement.
        
        This method:
        1. Determines primary movement direction
        2. Sets both direction and facing_direction properties
        Note: Facing direction takes precedence over movement direction
        for animations when not moving.
        """
        
        # Vertical movement takes precedence
        if self.change_y > 0:
            self.direction = DIRECTION_UP
            self.facing_direction = DIRECTION_UP
            
        elif self.change_y < 0:
            self.direction = DIRECTION_DOWN
            self.facing_direction = DIRECTION_DOWN
            
        # Horizontal movement
        elif self.change_x < 0:
            self.direction = DIRECTION_LEFT
            self.facing_direction = DIRECTION_LEFT
            
        elif self.change_x > 0:
            self.direction = DIRECTION_RIGHT
            self.facing_direction = DIRECTION_RIGHT

    def _handle_dash_animation(self):
        """
        Manage dash animation sequence.
        
        This method:
        1. Advances animation frame counter
        2. Checks for dash completion conditions
        3. Resets state when dash ends
        4. Updates texture to current dash frame
        """
        
        # Advance animation counter
        self.cur_texture += 1
        
        # Calculate total frames in dash animation
        dash_frames = len(self.dash_textures[self.facing_direction])\
            * UPDATES_PER_FRAME
        
        # Check dash completion conditions:
        # - Time-based expiration
        # - Animation cycle completion
        
        current_time = time.time()
        dash_time_expired = current_time - self.dash_start_time\
            >= self.dash_duration
        animation_complete = self.cur_texture >= dash_frames
        
        if dash_time_expired or animation_complete:
            
            # End dash state
            self.is_dashing = False
            self.cur_texture = 0
            self.change_x = 0
            self.change_y = 0
            
        else:
            
            # Calculate current animation frame
            frame = min(
                self.cur_texture // UPDATES_PER_FRAME,
                len(self.dash_textures[self.facing_direction]) - 1
            )
            
            # Update to current dash frame
            self.texture = self.dash_textures[self.facing_direction][frame]

    def _handle_standard_animation(self):
        """
        Manage standard idle and walking animations.
        
        This method:
        1. Advances animation frame counter
        2. Resets counter when animation cycle completes
        3. Selects appropriate animation set (idle or walk)
        4. Updates character texture
        """
        
        # Advance animation counter
        self.cur_texture += 1
        
        # Calculate maximum frames in animation cycle
        max_frame = 7 * UPDATES_PER_FRAME
        
        # Handle idle animation (no movement)
        if self.change_x == 0 and self.change_y == 0:
            # Reset counter when animation cycle completes
            if self.cur_texture >= max_frame:
                self.cur_texture = 0
            
            # Convert counter to frame index
            frame = self.cur_texture // UPDATES_PER_FRAME
            # Set idle texture for current direction
            self.texture = self.idle_textures[self.direction][frame]
        
        # Handle walking animation
        else:
            # Reset counter when animation cycle completes
            if self.cur_texture >= max_frame:
                self.cur_texture = 0
            
            # Convert counter to frame index
            frame = self.cur_texture // UPDATES_PER_FRAME
            # Set walking texture for current direction
            self.texture = self.walk_textures[self.direction][frame]
    
    def heal(self):
        """
        Initiate healing process if possible.
        
        Conditions:
        - Player not dead
        - Not currently in special state (dash/hurt/heal)
        - Heal cooldown expired
        """
        
        if (not self.is_dead and not self.is_healing 
            and not self.is_hurt and not self.is_dashing 
            and self.heal_cooldown <= 0):
            
            self.is_healing = True
            self.heal_start_time = time.time()
            self.hurt_count = max(0, self.hurt_count - self.heal_amount)
            self.change_x = 0
            self.change_y = 0

    def dash(self):
        """
        Initiate dash ability if possible.
        
        Conditions:
        - Player not dead
        - Not currently dashing
        - Dash cooldown expired
        """
        
        if (not self.is_dead and not self.is_dashing 
            and self.dash_cooldown <= 0):
                
            self.is_dashing = True
            self.dash_cooldown = self.dash_cooldown_time
            self.cur_texture = 0
            self.dash_start_time = time.time()
            self.is_hurt = False
            self.cur_texture = 0

            # Set dash vector based on facing direction
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

            # Play dash sound if available
            if hasattr(self, "dash_sound"):
                self.dash_sound.play()

    def hurt(self, damage_amount=1):
        """
        Apply damage to player if conditions met.
        
        Args:
            damage_amount (int): Amount of damage to apply
            
        Returns:
            bool: True if damage was applied, False otherwise
        """
        
        current_time = time.time()
        invincible_period = current_time - self.last_hurt_time <= self.invincibility_duration
        
        if (not self.is_dead and not self.is_hurt 
            and not self.is_dashing and not self.is_healing 
            and not invincible_period
            and not self.invincible):
            
            # Set hurt state
            self.is_hurt = True
            self.hurt_start_time = current_time
            self.last_hurt_time = current_time
            self.hurt_count += damage_amount
            self.change_x = 0
            self.change_y = 0
            
            # Apply knockback based on facing direction
            knockback = 20
            if self.facing_direction == DIRECTION_RIGHT:
                self.center_x -= knockback
            elif self.facing_direction == DIRECTION_LEFT:
                self.center_x += knockback
            elif self.facing_direction == DIRECTION_UP:
                self.center_y -= knockback
            elif self.facing_direction == DIRECTION_DOWN:
                self.center_y += knockback
                
            # Check for death
            if self.hurt_count >= self.max_hits_before_death:
                self.die()
            
            # Damage applied
            return True
        
        # No damage applied
        return False
                
    def die(self):
        """Set player to death state."""
        
        self.is_dead = True
        self.death_start_time = time.time()
        self.change_x = 0
        self.change_y = 0
        self.is_dashing = False
        self.cur_texture = 0
        self.texture = self.death_textures[self.facing_direction][0]

    def apply_speed_boost(self):
        """Apply speed boost effect to player."""
        
        if not self.is_dead:
            self.is_speed_boosted = True
            self.speed_boost_start_time = time.time()

    def update_speed_boost(self):
        """Update speed boost duration and expiration."""
        
        if self.is_speed_boosted:
            elapsed = time.time() - self.speed_boost_start_time
            if elapsed >= self.speed_boost_duration:
                self.is_speed_boosted = False


class Game(arcade.Window):
    """
    Main game class managing game state, levels, and rendering.
    
    Attributes:
        current_level (int): Current level number
        keys_collected (int): Number of keys collected
        scene (arcade.Scene): Current game scene
        player (PlayerCharacter): Player instance
        physics_engine: Physics system
        Various sprite lists for game objects
        Sound effects and music
    """
    
    def __init__(self):
        """Initialize game window and resources."""
        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Game state
        self.current_level = 1
        self.keys_collected = 0

        # Scene and physics
        self.scene = None
        self.player = None
        self.physics_engine = None

        # Camera system
        self.camera = arcade.Camera2D()

        # Input handling
        self.held_keys = set()

        # Sprite lists
        self.peak_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.flamethrower_list = arcade.SpriteList()
        self.slow_list = arcade.SpriteList()
        self.flask_list = arcade.SpriteList()
        self.speed_flask_list = arcade.SpriteList()
        self.keys_list = arcade.SpriteList()
        self.tunnel_door_list = arcade.SpriteList()

        # UI elements
        self.health_label = arcade.Text(
            "", 0, 0, arcade.color.WHITE, 12, 
            anchor_x="center", anchor_y="center"
        )
        self.key_label = arcade.Text(
            "", 0, 0, arcade.color.GOLD, 12,
            anchor_x="center", anchor_y="center"
        )

        # Load sound effects
        self._load_sounds()

        # Trap system timers
        self.peak_timer = 0.0
        self.peak_state = "wait"  # States: "wait", "active", "cooldown"
        self.arrow_timer = 0.0
        self.arrow_state = "wait"  # States: "short", "wait", "long"
        self.flame_timer = 0.0
        self.flame_state = "wait"  # States: "short", "wait", "long"

        # Initialize game
        self.setup()

    def _load_sounds(self):
        """Load all game sound effects."""
        
        self.heal_sound = arcade.Sound("music_and_sound/heal.wav")
        self.key_sound = arcade.Sound("music_and_sound/key.wav")
        self.speed_sound = arcade.Sound("music_and_sound/speed.wav")
        self.dash = arcade.Sound("music_and_sound/dash.wav")
        self.hurt_peak = arcade.Sound("music_and_sound/hurt_peak.mp3")
        self.hurt_arrow = arcade.Sound("music_and_sound/hurt_arrow.mp3")
        self.peak = arcade.Sound("music_and_sound/peak.mp3")
        self.arrow = arcade.Sound("music_and_sound/arrow.mp3")
        self.flamethrower = arcade.Sound("music_and_sound/flamethrower.mp3")
        self.background_music = arcade.Sound\
            ("music_and_sound/background_music.mp3")
        self.level_complete = arcade.Sound\
            ("music_and_sound/level_complete.wav")
        self.background_music_player = None

    def setup(self):
        """Initialize game state and load first level."""
        
        self.load_level(self.current_level)

    def load_level(self, level_number):
        """
        Load specified game level.
        
        Args:
            level_number (int): Level number to load
        """
        
        # Reset keys for new level
        self.keys_collected = 0
        
        # Reset trap timers
        self.peak_timer = 0.0
        self.peak_state = "wait"
        self.arrow_timer = 0.0
        self.arrow_state = "wait"
        self.flame_timer = 0.0
        self.flame_state = "wait"
        
        # Build map path
        map_path = os.path.join(
            os.path.dirname(__file__),
            f"Level_{level_number}.tmx"
        )

        # Configure tilemap layers
        layer_options = {
            "Foreground Fake Walls": {},
            "Walls": {"use_spatial_hash": True},
            "Collision Items": {"use_spatial_hash": True},
            "Boundary Walls": {"use_spatial_hash": True},
            "Non Collision Items": {},
            "Peaks": {},
            "Arrow": {},
            "Slow Speed Items": {},
            "Small Health Flasks": {},
            "Small Speed Flasks": {},
            "Keys": {},
            "Walls On Top of Boundary": {},
            "Tunnel Door": {},
            "Flamethrower": {},
            "Background": {},
            "Floor": {},
            "Tunnel": {}
        }
        
        # Load tilemap
        tilemap = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options=layer_options
        )
        
        # Initialize scene
        self.scene = arcade.Scene.from_tilemap(tilemap)
        
        # Handle foreground layers
        self._process_foreground_layers(tilemap)
        
        # Initialize game objects
        self._initialize_game_objects(tilemap)
        
        # Initialize player
        self._initialize_player(level_number)
        
        # Set up physics engine
        self._setup_physics()
        
        # Initialize camera
        self.camera = arcade.Camera2D()

        # Play background music
        self._play_background_music()

    def _process_foreground_layers(self, tilemap):
        """Process foreground layers for proper rendering."""
        
        # Extract foreground layers
        foreground_fake_walls = tilemap.sprite_lists.get(
            "Foreground Fake Walls", arcade.SpriteList()
        )
        walls_on_top = tilemap.sprite_lists.get(
            "Walls On Top of Boundary", arcade.SpriteList()
        )

        # Combine into single sprite list
        self.foreground_layers = arcade.SpriteList()
        self.foreground_layers.extend(foreground_fake_walls)
        self.foreground_layers.extend(walls_on_top)
        
        # Remove from main scene to prevent double rendering
        self.scene.remove_sprite_list_by_name("Foreground Fake Walls")
        self.scene.remove_sprite_list_by_name("Walls On Top of Boundary")

    def _initialize_game_objects(self, tilemap):
        """Initialize game objects from tilemap."""
        
        # Peaks (damage traps)
        self.peak_list = tilemap.sprite_lists.get(
            "Peaks", arcade.SpriteList()
        )
        for peak in self.peak_list:
            peak.properties = {"damage": True, "damage_amount": 1}

        # Arrows (damage traps)
        self.arrow_list = tilemap.sprite_lists.get(
            "Arrow", arcade.SpriteList()
        )
        for arrow in self.arrow_list:
            arrow.properties = {"damage": True, "damage_amount": 1}

        # Flamethrowers (damage traps)
        self.flamethrower_list = tilemap.sprite_lists.get(
            "Flamethrower", arcade.SpriteList()
        )
        for flame in self.flamethrower_list:
            flame.properties = {"damage": True, "damage_amount": 1}

        # Other objects inside of the tilemap
        self.slow_list = tilemap.sprite_lists.get(
            "Slow Speed Items", arcade.SpriteList()
        )
        
        self.flask_list = tilemap.sprite_lists.get(
            "Small Health Flasks", arcade.SpriteList()
        )
        
        self.speed_flask_list = tilemap.sprite_lists.get(
            "Small Speed Flasks", arcade.SpriteList()
        )
        
        self.keys_list = tilemap.sprite_lists.get(
            "Keys", arcade.SpriteList()
        )
        
        self.tunnel_door_list = tilemap.sprite_lists.get(
            "Tunnel Door", arcade.SpriteList()
        )
        
        self.total_keys = len(self.keys_list)

    def _initialize_player(self, level_number):
        """Initialize or reset player for current level."""
        
        # Hide tunnel until keys collected
        if (self.player is not None 
            and not self.player.is_dead 
            and self.keys_collected >= KEY_COUNT
            and "Tunnel" in self.scene
            and arcade.check_for_collision_with_list(
                self.player, self.scene["Tunnel"]
            )):
            for tunnel in self.scene["Tunnel"]:
                tunnel.visible = False

        # Create new player if needed
        if not hasattr(self, 'player') or self.player is None:
            self.player = PlayerCharacter()
            self.player.center_x = 1700
            self.player.center_y = 350
            self.player.dash_sound = self.dash
            
        else:
            # Reset existing player
            self.player.is_dead = False
            self.player.is_hurt = False
            self.player.is_dashing = False
            self.player.cur_texture = 0
            self.player.change_x = 0
            self.player.change_y = 0

            # Set position based on level
            if level_number == 1:
                self.player.center_x = 1700
                self.player.center_y = 350
                
            elif level_number == 2:
                self.player.center_x = 250
                self.player.center_y = 1300
                
            elif level_number == 3:
                self.player.center_x = 1650
                self.player.center_y = 2850

        # Add player to scene
        self.scene.add_sprite("Player", self.player)

    def _setup_physics(self):
        """Set up physics engine for collision detection."""
        
        # Combine collision layers
        collision_layers = arcade.SpriteList()
        collision_layers.extend(self.scene["Walls"])
        collision_layers.extend(self.scene["Collision Items"])
        collision_layers.extend(self.scene["Boundary Walls"])

        # Create physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, 
            collision_layers
        )

    def _play_background_music(self):
        """Play background music if not already playing."""
        
        should_play = (
            not self.background_music_player or 
            not self.background_music_player.playing
        )
        if should_play:
            self.background_music_player = self.background_music.play(loop=True)

    def draw_health_bar(self):
        """Draw player health bar above character."""
        
        # Calculate bar position
        bar_left = self.player.center_x - HEALTHBAR_WIDTH / 2
        bar_bottom = (
            self.player.center_y + 
            HEALTHBAR_OFFSET_Y - 
            HEALTHBAR_HEIGHT / 2
        )

        # Draw background (red)
        arcade.draw_lbwh_rectangle_filled(
            bar_left,
            bar_bottom,
            HEALTHBAR_WIDTH,
            HEALTHBAR_HEIGHT,
            arcade.color.RED
        )

        # Calculate health width
        health_percent = 1 - (
            self.player.hurt_count / 
            self.player.max_hits_before_death
        )
        
        health_width = HEALTHBAR_WIDTH * health_percent
            
        # Draw health (green)
        arcade.draw_lbwh_rectangle_filled(
            bar_left,
            bar_bottom,
            health_width,
            HEALTHBAR_HEIGHT,
            arcade.color.GREEN
        )

        # Position and draw health text
        self.health_label.x = self.player.center_x
        self.health_label.y = self.player.center_y + HEALTHBAR_OFFSET_Y
        self.health_label.draw()
    
    def draw_key_count(self):
        """Draw key count UI element."""
        
        self.key_label.text = f"Keys: {self.keys_collected}/{self.total_keys}"
        self.key_label.x = self.player.center_x
        self.key_label.y = self.player.center_y + HEALTHBAR_OFFSET_Y + 20
        self.key_label.draw()

    def on_draw(self):
        """Render the game scene."""
        
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.foreground_layers.draw()
        self.draw_health_bar()
        self.draw_key_count()

    def on_update(self, delta_time):
        """Update game state each frame.
        
        Args:
            delta_time (float): Time since last update
        """
        
        # Handle player movement input
        self._handle_player_movement()
        
        # Update physics and animations
        self.physics_engine.update()
        self.scene.update_animation(delta_time)
        self.player.character_animation(delta_time)
        self.player.update_speed_boost()
        
        # Update trap systems
        self.update_peak_system(delta_time)
        self.update_arrow_system(delta_time)
        self.update_flame_system(delta_time)

        # Handle key collection
        self._handle_key_collection()
        
        # Handle death state
        self._handle_death()
        
        # Handle level progression
        self._handle_level_progression()
        
        # Update camera position
        self.camera.position = self.player.position
        
    def _handle_player_movement(self):
        """Process player movement based on input."""
        
        if self.player.is_dead:
            # Disable movement when dead
            self.player.change_x = 0
            self.player.change_y = 0
            
        elif (
            not self.player.is_dashing and 
            not self.player.is_healing and
            not self.player.is_hurt
        ):
            # Reset movement
            self.player.change_x = 0
            self.player.change_y = 0

            # Change speed based on boost state
            if self.player.is_speed_boosted:
                current_speed = PLAYER_SPEED_BOOST
                self.player.dash_speed = PLAYER_DASH_BOOST
                
            else:
                current_speed = PLAYER_SPEED
                self.player.dash_speed = PLAYER_SPEED_BOOST

            # Apply slow effect in slow zones
            if arcade.check_for_collision_with_list(
                self.player, self.slow_list
            ):
                current_speed /= 2.0

            # Process movement keys
            if arcade.key.W in self.held_keys or arcade.key.UP \
                in self.held_keys:
                self.player.change_y = current_speed
                
            if arcade.key.S in self.held_keys or arcade.key.DOWN \
                in self.held_keys:
                self.player.change_y = -current_speed
                
            if arcade.key.A in self.held_keys or arcade.key.LEFT \
                in self.held_keys:
                self.player.change_x = -current_speed
                
            if arcade.key.D in self.held_keys or arcade.key.RIGHT \
                in self.held_keys:
                self.player.change_x = current_speed

    def _handle_key_collection(self):
        """Handle key collection mechanics."""
        
        if not self.player.is_dead and self.keys_list:
            
            # Check for collisions with keys
            keys_collected = arcade.check_for_collision_with_list(
                self.player, self.keys_list
            )
                
            for key_sprite in keys_collected:
                
                # Collect key
                key_sprite.remove_from_sprite_lists()
                self.keys_collected += 1
                self.key_sound.play()

                # Remove tunnel doors when enough keys collected
                if self.keys_collected >= KEY_COUNT and self.tunnel_door_list:
                    
                    for door in self.tunnel_door_list:
                        door.remove_from_sprite_lists()
                    self.tunnel_door_list = arcade.SpriteList()

            # Reveal tunnel when enough keys collected
            if self.keys_collected >= KEY_COUNT and "Tunnel" in self.scene:
                for tunnel in self.scene["Tunnel"]:
                    tunnel.visible = True

    def _handle_death(self):
        """Handle player death state."""
        
        if self.player.is_dead and self.player.death_completed:
            
            # Wait 1 second after death animation completes
            if time.time() - self.player.death_complete_time >= 1.0:
                arcade.close_window()
                sys.exit(0)

    def _handle_level_progression(self):
        """Handle level progression through tunnels."""
        
        if (
            self.player is not None and
            not self.player.is_dead and 
            self.keys_collected >= KEY_COUNT and 
            "Tunnel" in self.scene and 
            arcade.check_for_collision_with_list(
                self.player, self.scene["Tunnel"]
            )
        ):
            
            if self.current_level < MAX_LEVEL:
                # Advance to next level
                self.level_complete.play()
                self.current_level += 1
                self.load_level(self.current_level)
                
            else:
                # Game completed
                arcade.close_window()
                sys.exit()
        
    def update_peak_system(self, delta_time):
        """
        Update peak trap activation cycle.
        
        Args:
            delta_time (float): Time since last update
        """
        
        if self.player.is_dead:
            return

        # State durations and transitions
        durations = {
            # Waiting period
            "wait": 4.2,
            
            # Damage period
            "active": 2.0,
            
            # Recovery period
            "cooldown": 0.2
        }
        
        next_state = {
            "wait": "active",
            "active": "cooldown",
            "cooldown": "wait"
        }

        # Update timer
        self.peak_timer += delta_time

        # Process current state
        if self.peak_timer < durations[self.peak_state]:
            
            # Damage during active phase
            if (self.peak_state == "active" and 
                arcade.check_for_collision_with_list(
                    self.player, self.peak_list)
                ):
                
                if self.player.hurt():
                    self.hurt_peak.play()
                    
        else:
            
            # Transition to next state
            self.peak_timer -= durations[self.peak_state]
            self.peak_state = next_state[self.peak_state]

            # Handle state-specific actions
            if self.peak_state == "active":
                
                # Activate peaks
                for p in self.peak_list:
                    p.visible = True
                self.peak.play()
                
                
            elif self.peak_state == "cooldown":
                # Deactivate peaks
                for p in self.peak_list:
                    p.visible = False
                    
    def update_arrow_system(self, delta_time):
        """
        Update arrow trap activation cycle.
        
        Args:
            delta_time (float): Time since last update
        """
        
        # State durations and transitions
        durations = {
            
            # Brief damage window
            "short": 0.1,
            
            # Waiting period
            "wait": 2.0,
            
            # Longer damage window
            "long": 0.3
        }
        
        next_state = {
            "short": "wait",
            "wait": "long",
            "long": "short"
        }

        # Update timer
        self.arrow_timer += delta_time

        # Process current state
        if self.arrow_timer < durations[self.arrow_state]:
            
            # Damage during active phases
            if self.arrow_state in ("short", "long"):
                
                if arcade.check_for_collision_with_list(
                    self.player, self.arrow_list
                ):
                    
                    if self.player.hurt():
                        self.hurt_arrow.play()
        else:
            
            # Transition to next state
            self.arrow_timer -= durations[self.arrow_state]
            self.arrow_state = next_state[self.arrow_state]

            # Play sound when entering long state
            if self.arrow_state == "long":
                self.arrow.play()

    def update_flame_system(self, delta_time):
        """
        Update flamethrower trap activation cycle.
        
        Args:
            delta_time (float): Time since last update
        """
        
        # State durations and transitions
        durations = {
            # Brief flame burst
            "short": 0.15,
            
            # Waiting period
            "wait": 2.0,
            
            # Sustained flame
            "long": 0.3
        }
        
        next_state = {
            "short": "wait",
            "wait": "long",
            "long": "short"
        }

        # Update timer
        self.flame_timer += delta_time

        # Process current state
        if self.flame_timer < durations[self.flame_state]:
            
            # Damage during active phases
            if self.flame_state in ("short", "long"):
                
                if arcade.check_for_collision_with_list(
                    self.player, self.flamethrower_list
                ):
                    
                    if self.player.hurt():
                        
                        # Reuse arrow hurt sound
                        self.hurt_arrow.play()
                        
        else:
            
            # Transition to next state
            self.flame_timer -= durations[self.flame_state]
            self.flame_state = next_state[self.flame_state]

            # Play sound when entering long state
            if self.flame_state == "long":
                self.flamethrower.play()

    def on_key_press(self, key, modifiers):
        """
        Handle keyboard press events.
        
        Args:
            key (int): Keycode of pressed key
            modifiers (int): Modifier keys state
        """
        
        self.held_keys.add(key)
        
        # Dash ability
        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.player.dash()
            
        # Interaction key (E)
        elif key == arcade.key.E:
            self._handle_interactions()

    def _handle_interactions(self):
        """Handle player interactions (healing, speed boosts)."""
        
        # Health flask collection
        if self.flask_list:
            flasks_nearby = arcade.check_for_collision_with_list(
                self.player, self.flask_list
            )
            
            if flasks_nearby:
                self.player.heal()
                self.heal_sound.play()
                
                for flask in flasks_nearby:
                    flask.remove_from_sprite_lists()

        # Speed flask collection
        if self.speed_flask_list:
            speed_flasks_nearby = arcade.check_for_collision_with_list(
                self.player, self.speed_flask_list
            )
            
            if speed_flasks_nearby:
                self.player.apply_speed_boost()
                self.player.is_healing = True
                self.player.heal_start_time = time.time()
                self.player.change_x = 0
                self.player.change_y = 0
                self.speed_sound.play()
                
                for flask in speed_flasks_nearby:
                    flask.remove_from_sprite_lists()

    def on_key_release(self, key, modifiers):
        """
        Handle keyboard release events.
        
        Args:
            key (int): Keycode of released key
            modifiers (int): Modifier keys state
        """
        
        self.held_keys.discard(key)

if __name__ == "__main__":
    """Main entry point for the game."""
    
    window = Game()
    arcade.run()