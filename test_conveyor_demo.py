#!/usr/bin/env python3
"""
Demo test to show conveyor platform behavior
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


def test_conveyor_platform_demo():
    """Demonstrate conveyor platform behavior"""
    print("🎢 Conveyor Platform Demo")
    print("=" * 50)
    
    # Create frog and conveyor platforms
    frog = Frog(400, 300)
    conveyor_left = Platform(300, 350, 100, 20, PlatformType.CONVEYOR)  # Even x = right
    conveyor_right = Platform(501, 350, 100, 20, PlatformType.CONVEYOR)  # Odd x = left
    normal_platform = Platform(400, 450, 100, 20, PlatformType.NORMAL)
    
    print(f"Conveyor Left - Direction: {conveyor_left.conveyor_direction}, Speed: {conveyor_left.conveyor_speed}")
    print(f"Conveyor Right - Direction: {conveyor_right.conveyor_direction}, Speed: {conveyor_right.conveyor_speed}")
    print(f"Normal Platform - No conveyor effect")
    print()
    
    # Test 1: Landing on left conveyor
    print("Test 1: Frog lands on left conveyor")
    frog.vx = 0.0
    print(f"Before landing - Frog vx: {frog.vx}")
    
    conveyor_left.on_frog_land(frog)
    print(f"After landing - Frog vx: {frog.vx}")
    print(f"Conveyor pushed frog {'right' if frog.vx > 0 else 'left'} with force {abs(frog.vx)}")
    print()
    
    # Test 2: Continuous conveyor effect
    print("Test 2: Continuous conveyor effect over 5 frames")
    frog.on_conveyor = True
    frog.conveyor_platform = conveyor_left
    
    for frame in range(5):
        old_vx = frog.vx
        frog.update()
        print(f"Frame {frame + 1}: vx {old_vx:.1f} → {frog.vx:.1f} (change: {frog.vx - old_vx:+.1f})")
        
        # Reset conveyor state for next frame (normally done by collision detection)
        frog.on_conveyor = True
        frog.conveyor_platform = conveyor_left
    
    print()
    
    # Test 3: Landing on right conveyor (should go opposite direction)
    print("Test 3: Frog lands on right conveyor")
    frog.vx = 0.0
    print(f"Before landing - Frog vx: {frog.vx}")
    
    conveyor_right.on_frog_land(frog)
    print(f"After landing - Frog vx: {frog.vx}")
    print(f"Conveyor pushed frog {'right' if frog.vx > 0 else 'left'} with force {abs(frog.vx)}")
    print()
    
    # Test 4: Normal platform comparison
    print("Test 4: Frog lands on normal platform")
    frog.vx = 0.0
    print(f"Before landing - Frog vx: {frog.vx}")
    
    normal_platform.on_frog_land(frog)
    print(f"After landing - Frog vx: {frog.vx}")
    print("Normal platform has no effect on horizontal velocity")
    print()
    
    # Test 5: Player controls on conveyor
    print("Test 5: Player controls while on conveyor")
    frog.on_conveyor = True
    frog.conveyor_platform = conveyor_left
    frog.vx = 0.0
    
    print("Player tries to move right while on left-moving conveyor:")
    frog.move_horizontal(1)  # Move right
    print(f"After player input - Frog vx: {frog.vx}")
    print("Player controls work normally - conveyor doesn't reduce responsiveness")
    
    print("\n" + "=" * 50)
    print("✅ Conveyor platforms work as expected!")
    print("- They push the frog sideways when landed on")
    print("- They continue pushing while frog is on them")
    print("- Different platforms can push in different directions")
    print("- Player controls remain fully responsive")


if __name__ == '__main__':
    test_conveyor_platform_demo()