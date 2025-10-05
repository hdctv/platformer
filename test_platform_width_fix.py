#!/usr/bin/env python3
"""
Simple test for the platform width reuse bug fix
"""

import sys
sys.path.append('.')

from frog_platformer import PlatformGenerator, Platform, WIDTH

def test_platform_width_reuse_bug():
    """Test that the platform width reuse bug is fixed"""
    print("=== Platform Width Reuse Bug Fix Test ===")
    
    generator = PlatformGenerator()
    print(f"Generator standard width: {generator.platform_width}px")
    
    # Simulate the bug scenario:
    # 1. Create a full-width platform (like the starting platform)
    full_width_platform = Platform(WIDTH // 2, 100, WIDTH, 20)
    print(f"✓ Created full-width platform: {full_width_platform.width}px")
    
    # 2. Add it to inactive pool (simulating cleanup)
    generator.inactive_platforms.append(full_width_platform)
    full_width_platform.active = False
    print(f"✓ Added to inactive pool: {len(generator.inactive_platforms)} platforms")
    
    # 3. Create a new platform (should reuse the full-width one)
    print("Creating new platform (should reuse the full-width one)...")
    reused_platform = generator.create_platform(400, 200)
    
    print(f"✓ Reused platform width: {reused_platform.width}px")
    print(f"✓ Expected width: {generator.platform_width}px")
    
    # 4. Verify the bug is fixed
    if reused_platform.width == generator.platform_width:
        print("✅ BUG FIXED: Reused platform has correct width!")
        return True
    else:
        print(f"❌ BUG STILL EXISTS: Reused platform has width {reused_platform.width}px instead of {generator.platform_width}px")
        return False

def test_multiple_reuses():
    """Test multiple platform reuses to ensure consistency"""
    print("\n=== Multiple Reuse Test ===")
    
    generator = PlatformGenerator()
    
    # Create platforms with different widths and add to inactive pool
    widths_to_test = [WIDTH, 500, 300, 150]  # Various unusual widths
    
    for width in widths_to_test:
        platform = Platform(400, 100, width, 20)
        generator.inactive_platforms.append(platform)
        platform.active = False
        print(f"✓ Added {width}px wide platform to inactive pool")
    
    print(f"Inactive pool size: {len(generator.inactive_platforms)}")
    
    # Now reuse all of them
    all_correct = True
    for i in range(len(widths_to_test)):
        reused = generator.create_platform(400 + i*50, 200 + i*50)
        print(f"✓ Reused platform {i+1}: {reused.width}px (should be {generator.platform_width}px)")
        
        if reused.width != generator.platform_width:
            all_correct = False
    
    if all_correct:
        print("✅ All reused platforms have correct width!")
        return True
    else:
        print("❌ Some reused platforms have incorrect width!")
        return False

if __name__ == "__main__":
    try:
        test1_passed = test_platform_width_reuse_bug()
        test2_passed = test_multiple_reuses()
        
        if test1_passed and test2_passed:
            print("\n🎉 Platform width reuse bug is FIXED!")
            print("✓ Full-width starting platform will no longer appear repeatedly")
            print("✓ All reused platforms get correct standard width")
        else:
            print("\n❌ Platform width reuse bug still exists!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)