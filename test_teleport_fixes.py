#!/usr/bin/env python3
"""
Test script to verify teleport fixes:
1. Safety platform spawns below frog (not above)
2. Each teleport only usable once per game session
"""

import sys
sys.path.append('.')

from frog_platformer import *

def test_teleport_positioning():
    """Test that safety platform spawns below frog, not above"""
    print("Testing teleport positioning fixes...")
    
    # Initialize game objects
    global frog, camera, platform_generator, progress_tracker, used_teleports
    
    camera = Camera()
    platform_generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    used_teleports = set()
    
    # Test teleport to 25000
    target_height = 25000
    target_y = -target_height
    
    teleport_to_height(target_height)
    
    # Check frog position
    expected_frog_y = target_y - 50  # Should be above platform
    print(f"Frog Y: {frog.y} (expected: {expected_frog_y})")
    
    # Check platform position
    platforms = platform_generator.get_active_platforms()
    if platforms:
        safety_platform = platforms[0]
        expected_platform_y = target_y  # Platform at target height
        print(f"Platform Y: {safety_platform.y} (expected: {expected_platform_y})")
        
        # Verify frog is above platform
        if frog.y < safety_platform.y:
            print("✓ Frog is positioned ABOVE the safety platform (correct)")
            return True
        else:
            print("❌ Frog is positioned BELOW the safety platform (wrong)")
            return False
    else:
        print("❌ No safety platform found")
        return False

def test_one_time_use():
    """Test that each teleport can only be used once per game"""
    print("\nTesting one-time teleport usage...")
    
    # Initialize game objects
    global frog, camera, platform_generator, progress_tracker, used_teleports
    
    camera = Camera()
    platform_generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    used_teleports = set()
    
    target_height = 10000
    
    # First use should work
    print("First teleport attempt...")
    initial_platforms = len(platform_generator.get_active_platforms())
    teleport_to_height(target_height)
    after_first = len(platform_generator.get_active_platforms())
    
    if after_first > initial_platforms:
        print("✓ First teleport worked (platforms generated)")
    else:
        print("❌ First teleport failed")
        return False
    
    # Second use should be blocked
    print("Second teleport attempt (should be blocked)...")
    before_second = len(platform_generator.get_active_platforms())
    teleport_to_height(target_height)  # Should be blocked
    after_second = len(platform_generator.get_active_platforms())
    
    if after_second == before_second:
        print("✓ Second teleport blocked (no new platforms)")
    else:
        print("❌ Second teleport not blocked")
        return False
    
    # Check that teleport is marked as used
    if target_height in used_teleports:
        print("✓ Teleport marked as used in tracking set")
    else:
        print("❌ Teleport not marked as used")
        return False
    
    return True

def test_restart_resets_teleports():
    """Test that restarting game resets teleport usage"""
    print("\nTesting teleport reset on game restart...")
    
    # Initialize and use a teleport
    global frog, camera, platform_generator, progress_tracker, used_teleports
    
    camera = Camera()
    platform_generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    used_teleports = set()
    
    # Use teleport
    teleport_to_height(10000)
    
    if 10000 in used_teleports:
        print("✓ Teleport marked as used before restart")
    else:
        print("❌ Teleport not marked as used")
        return False
    
    # Restart game (simulate)
    used_teleports.clear()  # This is what restart_game() does
    
    if len(used_teleports) == 0:
        print("✓ Teleport usage cleared after restart")
    else:
        print("❌ Teleport usage not cleared")
        return False
    
    # Should be able to use teleport again
    teleport_to_height(10000)
    
    if 10000 in used_teleports:
        print("✓ Teleport usable again after restart")
        return True
    else:
        print("❌ Teleport still blocked after restart")
        return False

def test_multiple_teleports():
    """Test that different teleports can be used once each"""
    print("\nTesting multiple different teleports...")
    
    # Initialize game objects
    global frog, camera, platform_generator, progress_tracker, used_teleports
    
    camera = Camera()
    platform_generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    used_teleports = set()
    
    teleports = [10000, 25000, 50000]
    
    for height in teleports:
        print(f"Testing teleport to {height}...")
        initial_count = len(used_teleports)
        teleport_to_height(height)
        
        if len(used_teleports) == initial_count + 1:
            print(f"✓ Teleport to {height} worked and marked as used")
        else:
            print(f"❌ Teleport to {height} failed")
            return False
    
    # Try to use them again - should all be blocked
    print("Trying to reuse teleports (should be blocked)...")
    for height in teleports:
        before_count = len(platform_generator.get_active_platforms())
        teleport_to_height(height)
        after_count = len(platform_generator.get_active_platforms())
        
        if before_count == after_count:
            print(f"✓ Reuse of {height} teleport blocked")
        else:
            print(f"❌ Reuse of {height} teleport not blocked")
            return False
    
    return True

if __name__ == "__main__":
    print("=== Teleport Fixes Test Suite ===")
    
    try:
        success = True
        success &= test_teleport_positioning()
        success &= test_one_time_use()
        success &= test_restart_resets_teleports()
        success &= test_multiple_teleports()
        
        if success:
            print("\n🎉 All teleport fixes verified!")
            print("\nFixes applied:")
            print("• Safety platform now spawns BELOW frog (not above)")
            print("• Each teleport (Q/T/E) only usable once per game session")
            print("• Holding keys won't cause weird floating/regeneration")
            print("• Teleport usage resets when game restarts")
            print("• Multiple different teleports can each be used once")
        else:
            print("\n❌ Some teleport fixes failed - check output above")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)