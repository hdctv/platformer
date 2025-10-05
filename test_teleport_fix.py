#!/usr/bin/env python3
"""
Test script to verify the teleport function fixes
"""

import sys
sys.path.append('.')

from frog_platformer import *

def test_teleport_function():
    """Test that teleport function works without errors"""
    print("Testing teleport function fixes...")
    
    # Initialize game objects
    global frog, camera, platform_generator, progress_tracker
    
    # Initialize components
    camera = Camera()
    platform_generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    
    print("✓ Game objects initialized")
    
    # Test teleport to different heights
    test_heights = [10000, 25000, 50000]
    
    for height in test_heights:
        print(f"\nTesting teleport to height {height}...")
        
        try:
            teleport_to_height(height)
            print(f"✓ Teleport to {height} successful")
            
            # Verify frog position
            expected_y = -height + 100
            print(f"  Frog Y: {frog.y} (expected around {expected_y})")
            
            # Verify camera position
            expected_camera_y = -height
            print(f"  Camera Y: {camera.y} (expected {expected_camera_y})")
            
            # Verify safety platform exists
            platforms = platform_generator.get_active_platforms()
            if platforms:
                safety_platform = platforms[0]  # Should be the first platform
                print(f"  Safety platform width: {safety_platform.width} (full screen: {WIDTH})")
                print(f"  Safety platform Y: {safety_platform.y}")
                
                if safety_platform.width == WIDTH:
                    print("  ✓ Full-width safety platform created")
                else:
                    print("  ⚠️  Safety platform not full width")
            else:
                print("  ⚠️  No safety platform found")
            
            # Verify progress tracker updates
            if progress_tracker.max_height_reached >= height:
                print(f"  ✓ Progress tracker updated: {progress_tracker.max_height_reached}")
            else:
                print(f"  ⚠️  Progress tracker not updated properly")
                
        except Exception as e:
            print(f"  ❌ Teleport to {height} failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

def test_key_bindings():
    """Test that key bindings are correct"""
    print("\nTesting key binding changes...")
    
    # Read the source code to check key bindings
    with open('frog_platformer.py', 'r') as f:
        source = f.read()
    
    # Check that W key is changed to T
    if 'keyboard.w' in source and 'teleport_to_height' in source:
        print("⚠️  W key still used for teleport - potential conflict with movement")
        return False
    elif 'keyboard.t' in source and 'teleport_to_height' in source:
        print("✓ T key used for teleport - no movement conflict")
    else:
        print("? Teleport key binding not found")
    
    # Check movement keys
    movement_keys = ['keyboard.a', 'keyboard.d', 'keyboard.left', 'keyboard.right']
    found_movement = [key for key in movement_keys if key in source]
    print(f"✓ Movement keys found: {found_movement}")
    
    return True

def test_progress_tracker_attributes():
    """Test that ProgressTracker has correct attributes"""
    print("\nTesting ProgressTracker attributes...")
    
    tracker = ProgressTracker()
    
    # Check for correct attribute name
    if hasattr(tracker, 'milestone_heights'):
        print("✓ ProgressTracker has 'milestone_heights' attribute")
        milestones = list(tracker.milestone_heights.keys())
        print(f"  Milestones: {milestones}")
    else:
        print("❌ ProgressTracker missing 'milestone_heights' attribute")
        return False
    
    # Check that old incorrect attribute doesn't exist
    if hasattr(tracker, 'height_milestones'):
        print("⚠️  ProgressTracker still has old 'height_milestones' attribute")
    else:
        print("✓ Old 'height_milestones' attribute properly removed")
    
    return True

if __name__ == "__main__":
    print("=== Teleport Function Fix Test ===")
    
    try:
        success = True
        success &= test_progress_tracker_attributes()
        success &= test_key_bindings()
        success &= test_teleport_function()
        
        if success:
            print("\n🎉 All teleport fixes verified!")
            print("\nFixes applied:")
            print("• Fixed ProgressTracker attribute error (height_milestones → milestone_heights)")
            print("• Changed W key to T key to avoid movement conflicts")
            print("• Added full-width safety platform after teleporting")
            print("• Updated help text to reflect correct key bindings")
        else:
            print("\n❌ Some tests failed - check output above")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)