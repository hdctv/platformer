#!/usr/bin/env python3
"""
Demo to test dev shortcuts for skipping to high altitudes
Run this to test the laser system and other high-altitude features
"""

import sys
sys.path.append('.')

import pygame
import pgzero.game
from frog_platformer import *

# Override the game initialization to show dev shortcuts info
original_draw = draw

def enhanced_draw():
    """Enhanced draw function with dev shortcuts info"""
    original_draw()
    
    # Add dev shortcuts info overlay
    if game_state == GameState.PLAYING:
        # Draw dev shortcuts help
        help_y = 120
        screen.draw.text("DEV SHORTCUTS:", topleft=(15, help_y), fontsize=18, color="yellow")
        screen.draw.text("Q = 10K height (conveyors)", topleft=(15, help_y + 25), fontsize=16, color="lightblue")
        screen.draw.text("W = 25K height (moving)", topleft=(15, help_y + 45), fontsize=16, color="lightblue")
        screen.draw.text("E = 50K height (LASERS!)", topleft=(15, help_y + 65), fontsize=16, color="red")
        screen.draw.text("R = 75K height (more lasers)", topleft=(15, help_y + 85), fontsize=16, color="red")
        screen.draw.text("T = 100K height (extreme!)", topleft=(15, help_y + 105), fontsize=16, color="orange")

# Replace the draw function
draw = enhanced_draw

if __name__ == "__main__":
    print("=== Dev Shortcuts Demo ===")
    print("Starting Frog Platformer with dev shortcuts enabled!")
    print()
    print("🎮 Controls:")
    print("  SPACE/UP = Jump")
    print("  ARROW KEYS/WASD = Move")
    print("  ESC = Quit")
    print()
    print("🚀 Dev Shortcuts:")
    print("  Q = Skip to 10,000 height (conveyor platforms)")
    print("  W = Skip to 25,000 height (moving platforms)")
    print("  E = Skip to 50,000 height (LASER INTRODUCTION!)")
    print("  R = Skip to 75,000 height (high laser activity)")
    print("  T = Skip to 100,000 height (extreme altitude)")
    print()
    print("💡 Tips:")
    print("  - Use key E to test the new laser system!")
    print("  - Watch for red/blue warning circles on screen edges")
    print("  - Red laser beams = instant death!")
    print("  - Starting platform is now full-width (can't fall off)")
    print("  - All platforms are now 2x wider for easier gameplay")
    print()
    print("Press any key to start...")
    
    try:
        pgzero.game.run()
    except KeyboardInterrupt:
        print("\nDemo ended by user")
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()