import arcade
import os

# The constants for Dead Knight Top down game
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dead Knight"
PLAYER_SPEED = 3
TILE_SCALING = 1

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
    

if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()