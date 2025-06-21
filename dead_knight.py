import arcade
import os

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 3
TILE_SCALING = 1.8

class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.scene = None
        self.player = None
        self.camera = None
        self.physics_engine = None
        
        # Get the directory where this script is located
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
    def setup(self):
        # Path to your map file (in same directory as script)
        file_path = os.path.dirname(os.path.abspath(__file__)) 
        map_path = os.path.join(file_path, "Level_01.tmx") 
        
        
        # Load the map with collision layer
        tilemap = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options={
                "Walls": {"use_spatial_hash": True}
            }
        )
        
        self.scene = arcade.Scene.from_tilemap(tilemap)
        
        # Create player
        self.player = Player(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", 0.5)
        self.player.center_x = 1300
        self.player.center_y = 1300
        self.scene.add_sprite("Player", self.player)
        
        # Set up physics
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene["Walls"])
        
        # Set up camera
        self.camera = arcade.camera.Camera2D()
        
        # Initialize movement keys
        self.up = False
        self.down = False
        self.left = False
        self.right = False
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
    
    def on_update(self, delta_time):
        # Movement
        self.player.change_x = 0
        self.player.change_y = 0
        
        if self.up: self.player.change_y = PLAYER_SPEED
        if self.down: self.player.change_y = -PLAYER_SPEED
        if self.left: self.player.change_x = -PLAYER_SPEED
        if self.right: self.player.change_x = PLAYER_SPEED
        
        self.physics_engine.update()
        
        # Center camera
        self.camera.position = (
            self.player.center_x - SCREEN_WIDTH/2,
            self.player.center_y - SCREEN_HEIGHT/2
        )
    
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W): self.up = True
        if key in (arcade.key.DOWN, arcade.key.S): self.down = True
        if key in (arcade.key.LEFT, arcade.key.A): self.left = True
        if key in (arcade.key.RIGHT, arcade.key.D): self.right = True
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W): self.up = False
        if key in (arcade.key.DOWN, arcade.key.S): self.down = False
        if key in (arcade.key.LEFT, arcade.key.A): self.left = False
        if key in (arcade.key.RIGHT, arcade.key.D): self.right = False

if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()