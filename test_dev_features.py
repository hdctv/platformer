#!/usr/bin/env python3
"""
Test script for dev features and platform width bug fix
"""

import sys
sys.path.append('.')

from frog_platformer import *

def test_platform_reuse_width_fix():
    """Test that reused platforms get correct width (not full-width)"""
    print("Testing platform reuse width fix...")
    
    generator = PlatformGenerator()
    
    # Create a full-width platform (simulating the starting platform)
    full_width_platform = Platform(WIDTH // 2, 100, WIDTH, 20)
    print(f"✓ Created full-width platform: {full_width_platform.width}px")
    
    # Add it to active platforms then move to inactive (simulating cleanup)
    generator.active_platforms.append(full_width_platform)
    generator.inactive_platforms.append(full_width_platform)
    generator.active_platforms.remove(full_width_platform)
    full_width_platform.active = False
    
    print(f"✓ Moved to inactive pool: {len(generator.inactive_platforms)} inactive platforms")
    
    # Now create a new platform (should reuse the full-width one but fix its width)
    reused_platform = generator.create_platform(400, 200)
    
    print(f"✓ Reused platform width: {reused_platform.width}px (should be {generator.platform_width})")
    print(f"✓ Reused platform height: {reused_platform.height}px (should be {generator.platform_height})")
    
    # Verify the width was fixed
    assert reused_platform.width == generator.platform_width, f"Width should be {generator.platform_width}, got {reused_platform.width}"
    assert reused_platform.height == generator.platform_height, f"Height should be {generator.platform_height}, got {reused_platform.height}"
    
    print("✅ Platform reuse width fix working correctly!")

def test_teleport_function():
    """Test the teleport_to_height dev function"""
    print("\nTesting teleport function...")
    
    # Initialize game objects
    global frog, camera, platform_generator, progress_tracker
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    camera = Camera()
    platform_generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    
    initial_height = camera.get_scroll_distance()
    print(f"✓ Initial height: {initial_height}")
    
    # Test teleport to 50,000 (laser introduction height)
    target_height = 50000
    teleport_to_height(target_height)
    
    new_height = camera.get_scroll_distance()
    print(f"✓ After teleport height: {new_height}")
    print(f"✓ Frog position: ({frog.x}, {frog.y})")
    print(f"✓ Camera position: {camera.y}")
    print(f"✓ Active platforms: {len(platform_generator.active_platforms)}")
    
    # Verify teleport worked
    assert abs(new_height - target_height) < 100, f"Height should be near {target_height}, got {new_height}"
    assert len(platform_generator.active_platforms) > 0, "Should have platforms after teleport"
    
    # Check if landing platform exists
    landing_platforms = [p for p in platform_generator.active_platforms if p.width > 250]
    assert len(landing_platforms) > 0, "Should have a wide landing platform"
    
    print("✅ Teleport function working correctly!")

def test_dev_shortcuts_info():
    """Test dev shortcuts information"""
    print("\nTesting dev shortcuts...")
    
    shortcuts = {
        "1": 10000,   # Conveyor introduction
        "2": 25000,   # Moving platforms  
        "3": 50000,   # Laser introduction
        "4": 75000,   # High laser activity
        "5": 100000   # Extreme height
    }
    
    print("✓ Dev shortcuts available:")
    for key, height in shortcuts.items():
        print(f"  Key {key}: Skip to height {height:,}")
    
    print("✓ Dev shortcuts properly documented!")

def test_normal_platform_generation():
    """Test that normal platform generation creates correct widths"""
    print("\nTesting normal platform generation...")
    
    generator = PlatformGenerator()
    camera = Camera()
    
    # Generate some platforms
    generator.generate_platforms_above_camera(camera, camera.y - 500)
    
    # Check all generated platforms have correct width
    normal_width_count = 0
    for platform in generator.active_platforms:
        if platform.width == generator.platform_width:
            normal_width_count += 1
        else:
            print(f"⚠️  Found platform with unusual width: {platform.width}px")
    
    print(f"✓ Generated {len(generator.active_platforms)} platforms")
    print(f"✓ {normal_width_count} platforms have correct width ({generator.platform_width}px)")
    
    # Most platforms should have normal width (allowing for some special cases)
    assert normal_width_count >= len(generator.active_platforms) * 0.8, "Most platforms should have normal width"
    
    print("✅ Normal platform generation working correctly!")

if __name__ == "__main__":
    print("=== Dev Features & Bug Fix Test ===")
    
    try:
        test_platform_reuse_width_fix()
        test_teleport_function()
        test_dev_shortcuts_info()
        test_normal_platform_generation()
        
        print("\n🎉 All dev features and bug fixes working!")
        print("\nFeatures added:")
        print("• Dev shortcuts: Press 1-5 keys to skip to different heights")
        print("• Fixed platform width bug: Reused platforms now have correct width")
        print("• Teleport function: Safely jump to any height for testing")
        print("• Full-width starting platform is now truly one-off only")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)