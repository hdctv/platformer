#!/usr/bin/env python3
"""
Demo script to test laser obstacles in-game at high altitude
"""

import sys
sys.path.append('.')

import pygame
import pgzero.game
from frog_platformer import *

# Override the game initialization to start at high altitude with lasers
def demo_init():
    """Initialize game at high altitude to test lasers"""
    global frog, platforms, camera, platform_generator, progress_tracker, game_state
    
    # Initialize camera system
    camera = Camera()
    
    # Initialize platform generator
    platform_generator = PlatformGenerator()
    
    # Initialize progress tracker
    progress_tracker = ProgressTracker()
    
    # Start the frog at high altitude (above laser introduction height)
    start_height = -55000  # Well above 50,000 laser introduction
    frog = Frog(WIDTH // 2, start_height)
    
    # Set camera to high altitude
    camera.y = start_height
    
    # Create some platforms at high altitude
    for i in range(10):
        platform_y = start_height + (i * 100)
        platform_x = WIDTH // 2 + (i % 3 - 1) * 150  # Spread platforms
        platform = Platform(platform_x, platform_y, 100, 20)
        platform_generator.active_platforms.append(platform)
    
    # Force generate some lasers for testing
    for i in range(3):
        laser_y = start_height - (i * 300) - 200
        side = 'left' if i % 2 == 0 else 'right'
        laser = Laser(laser_y, side)
        # Start some lasers in different states for demo
        if i == 1:
            laser.timer = 1.0  # Mid-warning
        elif i == 2:
            laser.timer = 2.1  # Just started firing
            laser.state = LaserState.FIRING
        platform_generator.active_lasers.append(laser)
    
    platform_generator.highest_platform_y = start_height
    
    # Get platforms from generator
    platforms = platform_generator.get_active_platforms()
    
    game_state = GameState.PLAYING
    
    print("🚀 Demo started at high altitude!")
    print(f"Frog position: {frog.y}")
    print(f"Camera position: {camera.y}")
    print(f"Active lasers: {len(platform_generator.get_active_lasers())}")
    print("Look for red/blue warning circles and red laser beams!")
    print("Press SPACE to jump, arrow keys to move, ESC to quit")

if __name__ == "__main__":
    print("=== Laser Demo ===")
    print("Starting high-altitude laser demonstration...")
    
    # Replace the normal init with our demo init
    original_init = init_game
    init_game = demo_init
    
    # Start the game
    try:
        pgzero.game.run()
    except KeyboardInterrupt:
        print("\nDemo ended by user")
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()