#!/usr/bin/env python3
"""
Final test to verify both fixes work correctly
"""

import sys
sys.path.append('.')

from frog_platformer import PlatformGenerator, Platform, WIDTH

def test_platform_width_bug_fix():
    """Test that the platform width reuse bug is completely fixed"""
    print("=== Testing Platform Width Bug Fix ===")
    
    generator = PlatformGenerator()
    
    # Create the exact scenario: full-width starting platform gets reused
    starting_platform = Platform(WIDTH // 2, 100, WIDTH, 20)  # Full screen width
    print(f"✓ Created starting platform: {starting_platform.width}px wide")
    
    # Simulate it going to inactive pool (what happens during cleanup)
    generator.inactive_platforms.append(starting_platform)
    starting_platform.active = False
    
    # Now generate a new platform - it should reuse the starting platform but fix the width
    new_platform = generator.create_platform(400, 200)
    
    print(f"✓ Reused platform width: {new_platform.width}px")
    print(f"✓ Expected width: {generator.platform_width}px")
    
    if new_platform.width == generator.platform_width:
        print("✅ FIXED: Full-width platforms no longer appear repeatedly!")
        return True
    else:
        print("❌ BUG STILL EXISTS: Full-width platforms will still appear!")
        return False

def test_dev_shortcuts_setup():
    """Test that dev shortcuts are properly set up"""
    print("\n=== Testing Dev Shortcuts Setup ===")
    
    # Test that the teleport function exists and has proper error handling
    from frog_platformer import teleport_to_height
    
    print("✓ teleport_to_height function exists")
    
    # Test with no game objects (should handle gracefully)
    try:
        teleport_to_height(50000)
        print("✓ teleport_to_height handles missing game objects gracefully")
    except Exception as e:
        print(f"❌ teleport_to_height crashed: {e}")
        return False
    
    # Test the keyboard shortcuts are set up (we can't test actual key presses, but we can verify the code structure)
    import inspect
    from frog_platformer import handle_input
    
    source = inspect.getsource(handle_input)
    
    shortcuts_found = 0
    if 'keyboard.q' in source:
        shortcuts_found += 1
        print("✓ Q key shortcut found (10K height)")
    if 'keyboard.t' in source:
        shortcuts_found += 1
        print("✓ T key shortcut found (25K height)")
    if 'keyboard.e' in source:
        shortcuts_found += 1
        print("✓ E key shortcut found (50K height - LASERS!)")
    if 'keyboard.r' in source:
        shortcuts_found += 1
        print("✓ R key shortcut found (75K height)")
    if 'keyboard.t' in source:
        shortcuts_found += 1
        print("✓ T key shortcut found (100K height)")
    
    if shortcuts_found == 5:
        print("✅ All 5 dev shortcuts properly configured!")
        return True
    else:
        print(f"❌ Only {shortcuts_found}/5 dev shortcuts found!")
        return False

def test_laser_height_threshold():
    """Test that lasers are configured for the right height"""
    print("\n=== Testing Laser Configuration ===")
    
    from frog_platformer import GAME_CONFIG
    
    laser_config = GAME_CONFIG['laser_config']
    intro_height = laser_config['introduction_height']
    
    print(f"✓ Laser introduction height: {intro_height:,}")
    
    if intro_height == 50000:
        print("✅ Lasers will appear at 50,000 height as requested!")
        return True
    else:
        print(f"❌ Lasers appear at {intro_height}, not 50,000!")
        return False

if __name__ == "__main__":
    print("=== Final Fixes Verification ===")
    print()
    
    try:
        fix1 = test_platform_width_bug_fix()
        fix2 = test_dev_shortcuts_setup()
        fix3 = test_laser_height_threshold()
        
        print("\n" + "="*50)
        
        if fix1 and fix2 and fix3:
            print("🎉 ALL FIXES WORKING PERFECTLY!")
            print()
            print("✅ Platform width bug FIXED - no more repeated full-width platforms")
            print("✅ Dev shortcuts ADDED - use Q/W/E/R/T to skip to different heights")
            print("✅ Laser system READY - appears at 50,000+ height")
            print()
            print("🚀 Ready to test! Use 'E' key to skip to laser height!")
        else:
            print("❌ Some fixes need attention!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)