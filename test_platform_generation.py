"""
Test script to verify platform generation creates reachable platforms
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import generate_reachable_platforms, GAME_CONFIG

def test_platform_reachability():
    """Test that generated platforms are within jumping reach of each other"""
    
    # Generate test platforms
    platforms = generate_reachable_platforms(400, 550, 10)
    
    print(f"Generated {len(platforms)} platforms")
    print("Platform positions (x, y):")
    
    # Physics constants
    max_jump_height = (GAME_CONFIG['jump_strength'] ** 2) / (2 * GAME_CONFIG['gravity'])
    max_horizontal_reach = abs(GAME_CONFIG['jump_strength']) * GAME_CONFIG['horizontal_speed'] * 2 / GAME_CONFIG['gravity']
    
    print(f"Frog max jump height: {max_jump_height:.1f}")
    print(f"Frog max horizontal reach: {max_horizontal_reach:.1f}")
    print()
    
    reachable_count = 0
    
    for i, platform in enumerate(platforms):
        print(f"Platform {i}: ({platform.x:.1f}, {platform.y:.1f})")
        
        if i > 0:
            prev_platform = platforms[i-1]
            
            # Calculate distance to previous platform
            horizontal_distance = abs(platform.x - prev_platform.x)
            vertical_distance = prev_platform.y - platform.y  # Should be positive (going up)
            
            # Check if reachable
            horizontal_reachable = horizontal_distance <= max_horizontal_reach
            vertical_reachable = vertical_distance <= max_jump_height and vertical_distance > 0
            
            if horizontal_reachable and vertical_reachable:
                reachable_count += 1
                status = "✅ REACHABLE"
            else:
                status = "❌ TOO FAR"
                
            print(f"  Distance from prev: H={horizontal_distance:.1f}, V={vertical_distance:.1f} - {status}")
    
    print(f"\nReachability: {reachable_count}/{len(platforms)-1} platforms reachable")
    
    if reachable_count == len(platforms) - 1:
        print("🎉 All platforms are reachable!")
        return True
    else:
        print("⚠️  Some platforms may be unreachable")
        return False

if __name__ == "__main__":
    test_platform_reachability()