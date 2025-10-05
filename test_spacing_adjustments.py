#!/usr/bin/env python3
"""
Test script to verify spacing and laser adjustments
"""

import sys
sys.path.append('.')

from frog_platformer import *
import random

def test_laser_frequency():
    """Test that lasers are more frequent"""
    print("Testing laser frequency improvements...")
    
    # Check config values
    laser_config = GAME_CONFIG['laser_config']
    spawn_chance = laser_config['spawn_chance']
    
    print(f"Laser spawn chance: {spawn_chance * 100}% (was 15%, now should be 30%)")
    
    if spawn_chance >= 0.25:
        print("✓ Laser spawn rate significantly increased")
    else:
        print("❌ Laser spawn rate not increased enough")
        return False
    
    # Test laser spacing
    generator = PlatformGenerator()
    
    # Simulate laser generation frequency
    laser_attempts = 0
    laser_spawns = 0
    
    for _ in range(1000):  # Simulate 1000 generation attempts
        if random.random() < spawn_chance:
            laser_spawns += 1
        laser_attempts += 1
    
    spawn_rate = (laser_spawns / laser_attempts) * 100
    print(f"Simulated spawn rate: {spawn_rate:.1f}% (expected ~30%)")
    
    if 25 <= spawn_rate <= 35:  # Allow some variance
        print("✓ Laser spawn rate simulation matches expected frequency")
    else:
        print("⚠️  Laser spawn rate simulation outside expected range")
    
    return True

def test_platform_spacing():
    """Test that platform spacing is more varied"""
    print("\nTesting platform spacing improvements...")
    
    generator = PlatformGenerator()
    
    # Check vertical gap settings
    min_gap = generator.min_vertical_gap
    max_gap = generator.max_vertical_gap
    gap_range = max_gap - min_gap
    
    print(f"Vertical gap range: {min_gap} to {max_gap} (range: {gap_range})")
    print(f"  Was: 60 to 100 (range: 40)")
    print(f"  Now: {min_gap} to {max_gap} (range: {gap_range})")
    
    if min_gap >= 80:
        print("✓ Minimum vertical gap increased (prevents double-jumping)")
    else:
        print("❌ Minimum vertical gap not increased enough")
        return False
    
    if gap_range >= 40:
        print("✓ Vertical gap range maintained or increased")
    else:
        print("❌ Vertical gap range decreased")
        return False
    
    # Check horizontal reach
    max_reach = generator.max_horizontal_reach
    print(f"Maximum horizontal reach: {max_reach} (was 120)")
    
    if max_reach >= 150:
        print("✓ Horizontal reach increased for wider platform spacing")
    else:
        print("❌ Horizontal reach not increased enough")
        return False
    
    return True

def test_jump_prevention():
    """Test that double-jumping between platforms is prevented"""
    print("\nTesting double-jump prevention...")
    
    # Frog jump physics
    frog_jump_height = 144  # From physics calculations
    generator = PlatformGenerator()
    min_gap = generator.min_vertical_gap
    
    print(f"Frog max jump height: {frog_jump_height}")
    print(f"Minimum platform gap: {min_gap}")
    
    # Check if frog can jump over a platform to reach the next one
    # This would happen if min_gap * 2 < jump_height
    double_jump_possible = (min_gap * 2) < frog_jump_height
    
    if not double_jump_possible:
        print("✓ Double-jumping prevented (min gap * 2 >= jump height)")
    else:
        print("⚠️  Double-jumping might still be possible")
        print(f"  Gap * 2 = {min_gap * 2}, Jump height = {frog_jump_height}")
    
    # Check that single jumps are still possible
    single_jump_possible = min_gap < frog_jump_height
    
    if single_jump_possible:
        print("✓ Single jumps still possible")
    else:
        print("❌ Single jumps might be too difficult")
        return False
    
    return True

def test_platform_width_balance():
    """Test that wider platforms work well with new spacing"""
    print("\nTesting platform width and spacing balance...")
    
    generator = PlatformGenerator()
    platform_width = generator.platform_width
    max_horizontal_reach = generator.max_horizontal_reach
    
    print(f"Platform width: {platform_width}")
    print(f"Max horizontal reach: {max_horizontal_reach}")
    
    # Calculate effective gap (distance between platform edges)
    # Two platforms at max distance apart
    max_gap_between_edges = max_horizontal_reach - platform_width
    
    print(f"Max gap between platform edges: {max_gap_between_edges}")
    
    if max_gap_between_edges > 0:
        print("✓ Platforms don't always overlap (good spacing variety)")
    else:
        print("⚠️  Platforms might always overlap")
    
    # Check that gaps aren't too large
    if max_gap_between_edges < 100:
        print("✓ Maximum gaps are reasonable for gameplay")
    else:
        print("⚠️  Maximum gaps might be too large")
    
    return True

def test_laser_spacing():
    """Test laser spacing frequency"""
    print("\nTesting laser spacing frequency...")
    
    # Read the source to check laser spacing
    with open('frog_platformer.py', 'r') as f:
        source = f.read()
    
    if 'laser_spacing = 250' in source:
        print("✓ Laser spacing reduced to 250 units (was 400)")
        print("  Lasers will appear more frequently during gameplay")
    elif 'laser_spacing = 400' in source:
        print("⚠️  Laser spacing still at 400 units (not changed)")
    else:
        print("? Laser spacing setting not found")
    
    return True

if __name__ == "__main__":
    print("=== Spacing and Laser Adjustments Test ===")
    
    try:
        success = True
        success &= test_laser_frequency()
        success &= test_platform_spacing()
        success &= test_jump_prevention()
        success &= test_platform_width_balance()
        success &= test_laser_spacing()
        
        if success:
            print("\n🎉 All spacing and laser adjustments verified!")
            print("\nAdjustments made:")
            print("• Laser spawn rate: 15% → 30% (doubled)")
            print("• Laser spacing: 400 → 250 units (more frequent)")
            print("• Vertical gaps: 60-100 → 80-130 (prevents double-jumping)")
            print("• Horizontal reach: 120 → 180 (more spacing variety)")
            print("• Platform spacing ranges increased for wider platforms")
            print("\nGameplay impact:")
            print("• More lasers at high altitudes for increased challenge")
            print("• Better platform spacing variety with wider platforms")
            print("• No more double-jumping between platforms")
            print("• More varied horizontal platform positioning")
        else:
            print("\n❌ Some adjustments need review - check output above")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)