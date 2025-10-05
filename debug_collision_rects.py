#!/usr/bin/env python3
"""
Debug collision rectangle calculations
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog
from pygame import Rect


def debug_collision_rectangles():
    """Debug the collision rectangle calculations"""
    print("🔍 DEBUG: Collision Rectangle Calculations")
    print("=" * 60)
    
    frog = Frog(400, 334)  # Position frog on platform
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    
    print(f"Frog details:")
    print(f"  Position: ({frog.x}, {frog.y})")
    print(f"  Size: {frog.width} x {frog.height}")
    print()
    
    print(f"Platform details:")
    print(f"  Position: ({conveyor.x}, {conveyor.y})")
    print(f"  Size: {conveyor.width} x {conveyor.height}")
    print()
    
    # Get collision rectangles
    platform_rect = conveyor.get_rect()
    frog_rect = Rect(frog.x - frog.width//2, frog.y - frog.height//2, 
                    frog.width, frog.height)
    
    print(f"Platform rectangle:")
    print(f"  Left: {platform_rect.left}, Right: {platform_rect.right}")
    print(f"  Top: {platform_rect.top}, Bottom: {platform_rect.bottom}")
    print(f"  Size: {platform_rect.width} x {platform_rect.height}")
    print()
    
    print(f"Frog rectangle:")
    print(f"  Left: {frog_rect.left}, Right: {frog_rect.right}")
    print(f"  Top: {frog_rect.top}, Bottom: {frog_rect.bottom}")
    print(f"  Size: {frog_rect.width} x {frog_rect.height}")
    print()
    
    # Check overlap
    overlap = platform_rect.colliderect(frog_rect)
    print(f"Rectangles overlap: {overlap}")
    
    if not overlap:
        print("No overlap detected. Checking distances:")
        
        # Check horizontal separation
        if frog_rect.right < platform_rect.left:
            h_gap = platform_rect.left - frog_rect.right
            print(f"  Horizontal gap: {h_gap} pixels (frog is {h_gap} pixels to the left)")
        elif frog_rect.left > platform_rect.right:
            h_gap = frog_rect.left - platform_rect.right
            print(f"  Horizontal gap: {h_gap} pixels (frog is {h_gap} pixels to the right)")
        else:
            print(f"  Horizontal overlap: OK")
        
        # Check vertical separation
        if frog_rect.bottom < platform_rect.top:
            v_gap = platform_rect.top - frog_rect.bottom
            print(f"  Vertical gap: {v_gap} pixels (frog is {v_gap} pixels above)")
        elif frog_rect.top > platform_rect.bottom:
            v_gap = frog_rect.top - platform_rect.bottom
            print(f"  Vertical gap: {v_gap} pixels (frog is {v_gap} pixels below)")
        else:
            print(f"  Vertical overlap: OK")
    
    print()
    
    # Test with frog in different positions
    test_positions = [
        (400, 334, "Center of platform"),
        (350, 334, "Left edge of platform"),
        (450, 334, "Right edge of platform"),
        (400, 350, "At platform Y level"),
        (400, 366, "Just below platform"),
    ]
    
    print("Testing different frog positions:")
    print("Position | Frog Rect | Platform Rect | Overlap")
    print("-" * 55)
    
    for x, y, desc in test_positions:
        frog.x = x
        frog.y = y
        
        frog_rect = Rect(frog.x - frog.width//2, frog.y - frog.height//2, 
                        frog.width, frog.height)
        overlap = platform_rect.colliderect(frog_rect)
        
        print(f"{desc:20s} | ({frog_rect.left:3d},{frog_rect.top:3d},{frog_rect.right:3d},{frog_rect.bottom:3d}) | ({platform_rect.left:3d},{platform_rect.top:3d},{platform_rect.right:3d},{platform_rect.bottom:3d}) | {overlap}")


if __name__ == '__main__':
    print("🐛 COLLISION RECTANGLE DEBUG")
    print("=" * 70)
    
    debug_collision_rectangles()
    
    print("=" * 70)
    print("🔍 Rectangle debug complete!")