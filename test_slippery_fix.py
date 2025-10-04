#!/usr/bin/env python3
"""
Test to verify slippery platform fixes are working correctly
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


def test_slippery_platform_behavior():
    """Test that slippery platforms work correctly with proper timing"""
    print("Testing slippery platform behavior...")
    
    # Create frog and slippery platform
    frog = Frog(400, 300)
    slippery_platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
    normal_platform = Platform(500, 350, 100, 20, PlatformType.NORMAL)
    
    # Test 1: Visual appearance
    print(f"Slippery platform color: {slippery_platform.get_visual_color()}")
    assert slippery_platform.get_visual_color() == 'lightblue', "Slippery platform should be lightblue initially"
    
    # Test 2: Simulate game loop behavior
    print("Simulating game loop behavior...")
    
    # Set up frog falling onto slippery platform
    frog.y = 340  # Just above platform
    frog.vy = 5   # Falling downward
    frog.vx = 8   # Moving horizontally
    
    # Simulate collision detection (this should set slippery state)
    platforms = [slippery_platform]
    frog.check_platform_collision(platforms)
    
    print(f"After collision - on_slippery_surface: {frog.on_slippery_surface}")
    print(f"After collision - vx: {frog.vx}")
    
    # Frog should be on slippery surface and velocity should be reduced
    assert frog.on_slippery_surface, "Frog should be on slippery surface after collision"
    assert frog.vx < 8, "Horizontal velocity should be reduced by friction"
    
    # Test 3: Movement controls on slippery surface
    print("Testing movement controls on slippery surface...")
    
    original_vx = frog.vx
    frog.move_horizontal(1)  # Try to move right
    
    print(f"Before move_horizontal: {original_vx}")
    print(f"After move_horizontal: {frog.vx}")
    
    # Movement should be different (gradual acceleration instead of instant)
    # The exact value depends on the gradual acceleration formula
    
    # Test 4: Compare with normal platform
    print("Testing normal platform for comparison...")
    
    normal_frog = Frog(500, 300)
    normal_frog.y = 340
    normal_frog.vy = 5
    normal_frog.vx = 8
    
    normal_platforms = [normal_platform]
    normal_frog.check_platform_collision(normal_platforms)
    
    print(f"Normal platform - on_slippery_surface: {normal_frog.on_slippery_surface}")
    print(f"Normal platform - vx after collision: {normal_frog.vx}")
    
    assert not normal_frog.on_slippery_surface, "Normal platform should not set slippery state"
    assert normal_frog.vx == 8, "Normal platform should not reduce velocity"
    
    print("✅ All slippery platform behavior tests passed!")


def test_visual_color_consistency():
    """Test that slippery platforms show lightblue most of the time"""
    print("Testing visual color consistency...")
    
    platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
    
    # Test colors over multiple updates
    colors_seen = []
    for i in range(100):
        platform.update(0.1)
        color = platform.get_visual_color()
        colors_seen.append(color)
    
    lightblue_count = colors_seen.count('lightblue')
    total_count = len(colors_seen)
    lightblue_percentage = (lightblue_count / total_count) * 100
    
    print(f"Colors seen: {set(colors_seen)}")
    print(f"Lightblue percentage: {lightblue_percentage:.1f}%")
    
    # Should be lightblue most of the time (at least 70%)
    assert lightblue_percentage >= 70, f"Should be lightblue at least 70% of the time, got {lightblue_percentage:.1f}%"
    
    # Should occasionally show shine effects
    assert 'white' in colors_seen or 'lightcyan' in colors_seen, "Should occasionally show shine effects"
    
    print("✅ Visual color consistency test passed!")


if __name__ == '__main__':
    print("🧊 Testing Slippery Platform Fixes")
    print("=" * 50)
    
    test_slippery_platform_behavior()
    print()
    test_visual_color_consistency()
    
    print("\n" + "=" * 50)
    print("🎉 All slippery platform fixes verified!")