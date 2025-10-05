#!/usr/bin/env python3
"""
Test bouncy platform mechanics
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog, GAME_CONFIG

def test_bouncy_platform_creation():
    """Test that bouncy platforms are created correctly"""
    platform = Platform(400, 350, 100, 20, PlatformType.BOUNCY)
    print(f"Platform type: {platform.platform_type}")
    print(f"Platform color: {platform.color}")
    print(f"Bounce power: {platform.bounce_power}")
    assert platform.platform_type == PlatformType.BOUNCY
    assert platform.color == 'pink'
    assert platform.bounce_power == 2.0
    print("✅ Bouncy platform creation test passed!")

def test_bouncy_platform_behavior():
    """Test that bouncy platforms launch the frog"""
    frog = Frog(400, 300)
    platform = Platform(400, 350, 100, 20, PlatformType.BOUNCY)
    
    # Set frog falling onto platform
    frog.y = 340  # Just above platform
    frog.vy = 5   # Falling downward
    
    print(f"Before bounce - Frog vy: {frog.vy}, on_ground: {frog.on_ground}")
    
    # Land on bouncy platform
    platform.on_frog_land(frog)
    
    print(f"After bounce - Frog vy: {frog.vy}, on_ground: {frog.on_ground}")
    
    # Check that frog was launched upward
    expected_velocity = GAME_CONFIG['jump_strength'] * 2.0
    assert frog.vy == expected_velocity, f"Expected {expected_velocity}, got {frog.vy}"
    assert not frog.on_ground, "Frog should not be grounded after bouncing"
    assert frog.vy < 0, "Frog should be moving upward (negative velocity)"
    
    print("✅ Bouncy platform behavior test passed!")

def test_bouncy_vs_normal_platform():
    """Test difference between bouncy and normal platforms"""
    frog1 = Frog(400, 300)
    frog2 = Frog(400, 300)
    
    normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
    bouncy_platform = Platform(400, 350, 100, 20, PlatformType.BOUNCY)
    
    # Both frogs falling
    frog1.vy = 5
    frog2.vy = 5
    
    # Land on different platforms
    normal_platform.on_frog_land(frog1)
    bouncy_platform.on_frog_land(frog2)
    
    print(f"Normal platform - Frog vy: {frog1.vy}, on_ground: {frog1.on_ground}")
    print(f"Bouncy platform - Frog vy: {frog2.vy}, on_ground: {frog2.on_ground}")
    
    # Normal platform should stop frog
    assert frog1.vy == 0
    assert frog1.on_ground
    
    # Bouncy platform should launch frog
    assert frog2.vy < 0  # Moving upward
    assert not frog2.on_ground
    
    print("✅ Bouncy vs normal platform test passed!")

if __name__ == '__main__':
    print("Testing bouncy platforms...")
    test_bouncy_platform_creation()
    test_bouncy_platform_behavior()
    test_bouncy_vs_normal_platform()
    print("\n🎉 All bouncy platform tests passed!")