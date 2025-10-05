#!/usr/bin/env python3
"""
Debug conveyor position and collision issues
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


def debug_position_tracking():
    """Debug detailed position tracking during conveyor interaction"""
    print("🔍 DEBUG: Detailed Position Tracking")
    print("=" * 60)
    
    frog = Frog(400, 300)
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    
    print(f"Conveyor details:")
    print(f"  Position: ({conveyor.x}, {conveyor.y})")
    print(f"  Size: {conveyor.width} x {conveyor.height}")
    print(f"  Left edge: {conveyor.x - conveyor.width//2}")
    print(f"  Right edge: {conveyor.x + conveyor.width//2}")
    print(f"  Top: {conveyor.y}")
    print(f"  Bottom: {conveyor.y + conveyor.height}")
    print()
    
    # Position frog above conveyor
    frog.y = 340
    frog.vy = 5
    frog.vx = 0
    
    print("Detailed frame-by-frame analysis:")
    print("Frame | Frog X  | Frog Y  | Frog VX | Frog VY | On Platform | Collision | Distance from Platform")
    print("-" * 95)
    
    for frame in range(8):
        # Update frog physics
        frog.update()
        
        # Check collision
        collision = conveyor.check_collision(frog)
        
        # Calculate distance from platform center
        distance_x = abs(frog.x - conveyor.x)
        distance_y = abs(frog.y - frog.height//2 - conveyor.y)
        
        # Check if frog is within platform bounds
        on_platform_x = (conveyor.x - conveyor.width//2) <= frog.x <= (conveyor.x + conveyor.width//2)
        
        print(f"{frame:5d} | {frog.x:7.1f} | {frog.y:7.1f} | {frog.vx:7.1f} | {frog.vy:7.1f} | {str(on_platform_x):11s} | {str(collision):9s} | X:{distance_x:.1f} Y:{distance_y:.1f}")
        
        # Handle collision if detected
        if collision:
            conveyor.on_collision(frog)
        else:
            # Reset conveyor state if no collision
            frog.on_conveyor = False
            frog.conveyor_platform = None
    
    print()


def debug_collision_conditions():
    """Debug the specific collision detection conditions"""
    print("🔍 DEBUG: Collision Detection Conditions")
    print("=" * 60)
    
    frog = Frog(400, 334)  # Position frog on platform
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    
    # Test different frog states
    test_cases = [
        ("Falling onto platform", 0, 5),
        ("Standing on platform", 0, 0),
        ("Moving right on platform", 5, 0),
        ("Slight upward velocity", 0, -0.5),
        ("Jumping off platform", 0, -5),
    ]
    
    for description, vx, vy in test_cases:
        frog.vx = vx
        frog.vy = vy
        
        # Get collision rectangles
        platform_rect = conveyor.get_rect()
        frog_rect = conveyor.get_rect()  # This is wrong, should be frog rect
        from pygame import Rect
        frog_rect = Rect(frog.x - frog.width//2, frog.y - frog.height//2, 
                        frog.width, frog.height)
        
        # Check collision conditions
        rects_overlap = platform_rect.colliderect(frog_rect)
        falling_condition = frog.vy > 0 and frog.y - frog.height//2 <= conveyor.y + conveyor.height
        conveyor_condition = (conveyor.platform_type == PlatformType.CONVEYOR and 
                            frog.vy >= 0 and  
                            abs(frog.y - frog.height//2 - conveyor.y) <= 5)
        
        collision_result = conveyor.check_collision(frog)
        
        print(f"{description}:")
        print(f"  Frog velocity: ({vx}, {vy})")
        print(f"  Rectangles overlap: {rects_overlap}")
        print(f"  Falling condition: {falling_condition}")
        print(f"  Conveyor condition: {conveyor_condition}")
        print(f"  Final collision: {collision_result}")
        print()


if __name__ == '__main__':
    print("🐛 CONVEYOR POSITION DEBUG")
    print("=" * 70)
    
    debug_position_tracking()
    debug_collision_conditions()
    
    print("=" * 70)
    print("🔍 Position debug complete!")