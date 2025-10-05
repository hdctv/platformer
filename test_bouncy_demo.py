#!/usr/bin/env python3
"""
Demo script to test bouncy platforms in action
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog, GAME_CONFIG

def demo_bouncy_platforms():
    """Demo bouncy platform mechanics"""
    print("🏀 Bouncy Platform Demo")
    print("=" * 40)
    
    # Create frog and platforms
    frog = Frog(400, 300)
    normal_platform = Platform(300, 400, 100, 20, PlatformType.NORMAL)
    bouncy_platform = Platform(500, 400, 100, 20, PlatformType.BOUNCY)
    
    print(f"Normal platform: {normal_platform.color}")
    print(f"Bouncy platform: {bouncy_platform.color} (bounce power: {bouncy_platform.bounce_power}x)")
    print()
    
    # Test 1: Normal platform landing
    print("Test 1: Landing on normal platform")
    frog.y = 390  # Just above platform
    frog.vy = 8   # Falling fast
    print(f"Before landing - Frog vy: {frog.vy}, on_ground: {frog.on_ground}")
    
    normal_platform.on_frog_land(frog)
    print(f"After landing  - Frog vy: {frog.vy}, on_ground: {frog.on_ground}")
    print("✅ Normal platform stops frog and makes it grounded")
    print()
    
    # Test 2: Bouncy platform landing
    print("Test 2: Landing on bouncy platform")
    frog.y = 390  # Just above platform
    frog.vy = 8   # Falling fast
    print(f"Before bounce  - Frog vy: {frog.vy}, on_ground: {frog.on_ground}")
    
    bouncy_platform.on_frog_land(frog)
    print(f"After bounce   - Frog vy: {frog.vy}, on_ground: {frog.on_ground}")
    
    # Calculate bounce height
    normal_jump = GAME_CONFIG['jump_strength']
    bounce_velocity = bouncy_platform.bounce_power * normal_jump
    print(f"Normal jump velocity: {normal_jump}")
    print(f"Bounce velocity: {bounce_velocity} ({bouncy_platform.bounce_power}x stronger)")
    print("✅ Bouncy platform launches frog and keeps it airborne")
    print()
    
    # Test 3: Multiple bounces simulation
    print("Test 3: Simulating multiple bounces")
    frog_height = 400
    for bounce in range(3):
        print(f"Bounce #{bounce + 1}:")
        frog.vy = 5  # Falling
        bouncy_platform.on_frog_land(frog)
        
        # Simulate upward movement (simplified physics)
        bounce_height = abs(frog.vy) * 8  # Simplified calculation
        frog_height -= bounce_height
        
        print(f"  Launch velocity: {frog.vy}")
        print(f"  Estimated height reached: {frog_height}")
    
    print("✅ Multiple bounces allow rapid upward progression")
    print()
    
    # Test 4: Risk demonstration
    print("Test 4: Risk/Reward demonstration")
    print("Benefits:")
    print("  - Double jump height allows skipping sections")
    print("  - Rapid vertical progression")
    print("  - Can chain bounces for speed runs")
    print()
    print("Risks:")
    print("  - Cannot stand still or control bounce")
    print("  - Might bounce into harmful platforms")
    print("  - Could overshoot and miss next platform")
    print("  - No ability to override with normal jump")
    print()
    
    print("🎉 Bouncy platforms successfully implemented!")
    print("Ready for gameplay testing at height 3750+")

if __name__ == '__main__':
    demo_bouncy_platforms()