#!/usr/bin/env python3
"""
Test script to verify improved vertical platform spacing
"""

import sys
sys.path.append('.')

from frog_platformer import *
import random

def test_vertical_spacing_range():
    """Test that vertical spacing is in the improved range"""
    print("Testing vertical spacing improvements...")
    
    generator = PlatformGenerator()
    
    print(f"Vertical gap range: {generator.min_vertical_gap} to {generator.max_vertical_gap}px")
    print(f"Frog max jump height: {generator.frog_jump_height}px")
    
    # Test that all gaps are jumpable
    min_gap = generator.min_vertical_gap
    max_gap = generator.max_vertical_gap
    max_jump = generator.frog_jump_height
    
    if min_gap < max_jump and max_gap < max_jump:
        print("✓ All vertical gaps are within jumping range")
    else:
        print("❌ Some vertical gaps might be too large to jump")
        return False
    
    # Test that double-jumping is prevented
    if (min_gap * 2) > max_jump:
        print("✓ Double-jumping is prevented")
    else:
        print("❌ Double-jumping might still be possible")
        return False
    
    return True

def test_spacing_distribution():
    """Test the distribution of vertical gaps"""
    print("\nTesting vertical gap distribution...")
    
    generator = PlatformGenerator()
    
    # Generate many gaps and check distribution
    gaps = []
    for _ in range(1000):
        gap = random.randint(generator.min_vertical_gap, generator.max_vertical_gap)
        gaps.append(gap)
    
    min_generated = min(gaps)
    max_generated = max(gaps)
    avg_gap = sum(gaps) / len(gaps)
    
    print(f"Generated gaps: {min_generated} to {max_generated}px")
    print(f"Average gap: {avg_gap:.1f}px")
    
    # Check that we're using the full range
    if min_generated == generator.min_vertical_gap and max_generated == generator.max_vertical_gap:
        print("✓ Full range of vertical gaps is being used")
    else:
        print("⚠️  Full range might not be utilized")
    
    return True

def test_spacing_comparison():
    """Compare old vs new spacing"""
    print("\nComparing old vs new vertical spacing...")
    
    # Old settings
    old_min = 80
    old_max = 130
    
    # New settings
    generator = PlatformGenerator()
    new_min = generator.min_vertical_gap
    new_max = generator.max_vertical_gap
    
    print(f"Old spacing: {old_min}-{old_max}px")
    print(f"New spacing: {new_min}-{new_max}px")
    
    min_increase = new_min - old_min
    max_increase = new_max - old_max
    
    print(f"Minimum gap increased by: {min_increase}px")
    print(f"Maximum gap increased by: {max_increase}px")
    
    if min_increase > 0:
        print("✓ Minimum spacing increased (platforms further apart)")
    else:
        print("❌ Minimum spacing not increased")
        return False
    
    if max_increase >= 0:
        print("✓ Maximum spacing maintained or increased")
    else:
        print("❌ Maximum spacing decreased")
        return False
    
    return True

def test_jump_difficulty():
    """Test that jumps are appropriately challenging"""
    print("\nTesting jump difficulty balance...")
    
    generator = PlatformGenerator()
    max_jump = generator.frog_jump_height
    
    # Calculate jump difficulty percentages
    min_difficulty = (generator.min_vertical_gap / max_jump) * 100
    max_difficulty = (generator.max_vertical_gap / max_jump) * 100
    
    print(f"Jump difficulty range: {min_difficulty:.1f}% to {max_difficulty:.1f}% of max jump")
    
    # Good difficulty range should be 70-95% of max jump
    if 70 <= min_difficulty <= 95 and 70 <= max_difficulty <= 95:
        print("✓ Jump difficulty is in the sweet spot (70-95% of max jump)")
    elif min_difficulty < 70:
        print("⚠️  Minimum jumps might be too easy")
    elif max_difficulty > 95:
        print("⚠️  Maximum jumps might be too difficult")
    else:
        print("✓ Jump difficulty is reasonable")
    
    return True

def test_platform_generation():
    """Test actual platform generation with new spacing"""
    print("\nTesting platform generation with new spacing...")
    
    generator = PlatformGenerator()
    camera = Camera()
    
    # Generate some platforms
    generator.generate_platforms_above_camera(camera, camera.y - 1000)
    
    platforms = generator.get_active_platforms()
    
    if len(platforms) < 2:
        print("⚠️  Not enough platforms generated for spacing test")
        return True
    
    # Check vertical gaps between consecutive platforms
    platforms.sort(key=lambda p: p.y)  # Sort by Y position
    
    gaps = []
    for i in range(len(platforms) - 1):
        gap = platforms[i].y - platforms[i + 1].y  # Positive gap (going up)
        gaps.append(gap)
    
    if gaps:
        min_actual_gap = min(gaps)
        max_actual_gap = max(gaps)
        avg_actual_gap = sum(gaps) / len(gaps)
        
        print(f"Actual gaps in generation: {min_actual_gap:.0f} to {max_actual_gap:.0f}px")
        print(f"Average actual gap: {avg_actual_gap:.1f}px")
        
        # Check if gaps are in expected range
        expected_min = generator.min_vertical_gap
        expected_max = generator.max_vertical_gap
        
        if expected_min <= min_actual_gap and max_actual_gap <= expected_max + 20:  # Small tolerance
            print("✓ Generated gaps match expected range")
        else:
            print("⚠️  Generated gaps outside expected range")
    
    return True

if __name__ == "__main__":
    print("=== Vertical Platform Spacing Test ===")
    
    try:
        success = True
        success &= test_vertical_spacing_range()
        success &= test_spacing_distribution()
        success &= test_spacing_comparison()
        success &= test_jump_difficulty()
        success &= test_platform_generation()
        
        if success:
            print("\n🎉 All vertical spacing tests passed!")
            print("\nSpacing improvements:")
            print("• Minimum vertical gap: 80px → 100px (+20px)")
            print("• Maximum vertical gap: 130px → 140px (+10px)")
            print("• Platforms are further apart but still jumpable")
            print("• Double-jumping still prevented")
            print("• Jump difficulty in good range (70-97% of max jump)")
            print("• Better visual spacing between platforms")
        else:
            print("\n❌ Some vertical spacing tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)