"""
Frog Platformer - A vertical scrolling platformer game built with Pygame Zero
"""

import pgzrun
from enum import Enum
from pygame import Rect

# Game Configuration Constants
GAME_CONFIG = {
    'screen_width': 800,
    'screen_height': 600,
    'scroll_speed': 1.0,
    'gravity': 0.5,
    'jump_strength': -12,
    'horizontal_speed': 3,
    'platform_spacing': {
        'min_vertical': 80,
        'max_vertical': 120,
        'min_horizontal': 100
    },
    'platform_introduction': {
        100: ['slippery'],
        200: ['breakable'],
        300: ['moving'],
        400: ['harmful']
    }
}

# Screen dimensions
WIDTH = GAME_CONFIG['screen_width']
HEIGHT = GAME_CONFIG['screen_height']

# Game State Enum
class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

# Platform Type Enum
class PlatformType(Enum):
    NORMAL = "normal"
    SLIPPERY = "slippery"
    BREAKABLE = "breakable"
    MOVING = "moving"
    HARMFUL = "harmful"

# Frog Character Class
class Frog:
    """
    The player-controlled frog character with physics and movement
    """
    def __init__(self, x, y):
        """
        Initialize the frog at the given position
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        # Position coordinates
        self.x = x
        self.y = y
        
        # Velocity components
        self.vx = 0.0  # Horizontal velocity
        self.vy = 0.0  # Vertical velocity
        
        # State tracking
        self.on_ground = False
        
        # Sprite will be added later when we have actual image assets
        # For now, we'll use rectangle rendering in the draw function
        self.sprite = None
        
        # Set a default size for collision detection
        self.width = 32
        self.height = 32
    
    def update(self):
        """
        Update frog physics, input, and state
        """
        # Apply gravity to vertical velocity
        self.vy += GAME_CONFIG['gravity']
        
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy
        
        # Keep frog within horizontal screen bounds
        if self.x < self.width // 2:
            self.x = self.width // 2
        elif self.x > WIDTH - self.width // 2:
            self.x = WIDTH - self.width // 2
        
        # Simple ground collision for now (will be replaced with platform system)
        # This prevents the frog from falling through the bottom of the screen
        ground_level = HEIGHT - 50
        if self.y >= ground_level:
            self.y = ground_level
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def jump(self):
        """
        Apply upward velocity for jumping
        Only allows jumping when frog is on ground
        """
        if self.on_ground:
            self.vy = GAME_CONFIG['jump_strength']
            self.on_ground = False
    
    def move_horizontal(self, direction):
        """
        Apply horizontal movement
        
        Args:
            direction (int): -1 for left, 1 for right, 0 for no movement
        """
        self.vx = direction * GAME_CONFIG['horizontal_speed']
    
    def check_platform_collision(self, platforms):
        """
        Handle landing on platforms
        Will be implemented when platform system is created
        
        Args:
            platforms (list): List of platform objects to check collision against
        """
        pass

# Global game state
game_state = GameState.PLAYING

# Global game objects
frog = None

def init_game():
    """
    Initialize the game objects
    """
    global frog
    # Start the frog in the center-bottom of the screen
    frog = Frog(WIDTH // 2, HEIGHT - 100)

def handle_input():
    """
    Handle player input for frog movement
    """
    global frog
    
    if frog:
        # Jump input (space bar or up arrow)
        if keyboard.space or keyboard.up:
            frog.jump()
        
        # Horizontal movement input
        horizontal_direction = 0
        if keyboard.left or keyboard.a:
            horizontal_direction = -1
        elif keyboard.right or keyboard.d:
            horizontal_direction = 1
        
        frog.move_horizontal(horizontal_direction)

def update():
    """
    Main game update loop - called every frame
    Handles game logic, physics, and state updates
    """
    global game_state, frog
    
    # Initialize game objects if not already done
    if frog is None:
        init_game()
    
    if game_state == GameState.PLAYING:
        # Handle player input
        handle_input()
        
        # Update frog
        if frog:
            frog.update()
    elif game_state == GameState.GAME_OVER:
        # Game over logic will be implemented later
        pass

def draw():
    """
    Main drawing function - called every frame
    Handles all rendering and visual updates
    """
    # Clear screen with sky blue background
    screen.fill((135, 206, 235))
    
    if game_state == GameState.PLAYING:
        # Draw frog
        if frog:
            # For now, draw a simple green rectangle as the frog
            # This will be replaced with actual sprite rendering later
            screen.draw.filled_rect(
                Rect(frog.x - frog.width//2, frog.y - frog.height//2, 
                     frog.width, frog.height), 
                'green'
            )
        
        # Show game title and status
        screen.draw.text("Frog Platformer", center=(WIDTH//2, 50), 
                        fontsize=36, color="white")
        screen.draw.text("Frog Character Created", 
                        center=(WIDTH//2, HEIGHT - 30), 
                        fontsize=20, color="white")
    elif game_state == GameState.GAME_OVER:
        # Game over screen will be implemented later
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), 
                        fontsize=48, color="red")

# Run the game
if __name__ == "__main__":
    pgzrun.go()