"""
Frog Platformer - A vertical scrolling platformer game built with Pygame Zero
"""

import pgzrun
from enum import Enum

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

# Global game state
game_state = GameState.PLAYING

def update():
    """
    Main game update loop - called every frame
    Handles game logic, physics, and state updates
    """
    global game_state
    
    if game_state == GameState.PLAYING:
        # Game logic will be implemented in subsequent tasks
        pass
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
        # Game rendering will be implemented in subsequent tasks
        # For now, just show a placeholder message
        screen.draw.text("Frog Platformer", center=(WIDTH//2, HEIGHT//2), 
                        fontsize=48, color="white")
        screen.draw.text("Game setup complete - Ready for implementation", 
                        center=(WIDTH//2, HEIGHT//2 + 60), 
                        fontsize=24, color="white")
    elif game_state == GameState.GAME_OVER:
        # Game over screen will be implemented later
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), 
                        fontsize=48, color="red")

# Run the game
if __name__ == "__main__":
    pgzrun.go()