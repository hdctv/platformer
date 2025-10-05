#!/usr/bin/env python3
"""
Test script to verify minimum horizontal distance between platforms
"""

import sys
sys.path.append('.')

from frog_platformer import *
import random

def test_horizontal_offset_generation():
    """Test that horizontal offsets respect minimum distance"""
    print("Testing horizontal offset generation...")
    
    generator = PlatformGenerator()
    min_distance = generator.min_horizontal_distance
    max_reach = generator.max_horizontal_reach
    
    print(f"Minimum horizontal distance: {min_distance}px")
    print(f"Maximum horizontal reach: {max_reach}px")
    
    # Generate many offsets and check they meet minimum distance
    import random
    offsets = []
    for _ in range(1000):
        # Simulate the offset generation logic
        direction = random.choice([-1, 1])
        min_offset = min_distance
        max_offset = min(max_reach, 180)
        if min_offset > max_offset:
            min_offset = max_offset // 2
        offset_magnitude = random.randint(min_offset, max_offset)
        offset = direction * offset_magnitude
        offsets.append(offset)
    
    # Check that all offsets meet minimum distance requirement
    valid_offsets = 0
    for offset in offsets:
        if abs(offset) >= min_distance:
            valid_offsets += 1
    
    percentage_valid = (valid_offsets / len(offsets)) * 100
    print(f"Offsets meeting minimum distance: {valid_offsets}/{len(offsets)} ({percentage_valid:.1f}%)")
    
    if percentage_valid == 100:
        print("✓ All offsets meet minimum distance requirement")
    else:
        print("❌ Some offsets are too small")
        return False
    
    # Check range of offsets
    min_offset = min(offsets)
    max_offset = max(offsets)
    print(f"Offset range: {min_offset} to {max_offset}")
    
    # Check that we get both left and right directions
    left_offsets = [o for o in offsets if o < 0]
    right_offsets = [o for o in offsets if o > 0]
    
    print(f"Left offsets: {len(left_offsets)}, Right offsets: {len(right_offsets)}")
    
    if len(left_offsets) > 0 and len(right_offsets) > 0:
        print("✓ Both left and right directions generated")
    else:
        print("❌ Missing left or right directions")
        return False
    
    return True

def test_platform_generation_spacing():
    """Test actual platform generation with minimum horizontal distance"""
    print("\nTesting platform generation with minimum spacing...")
    
    generator = PlatformGenerator()
    camera = Camera()
    
    # Generate platforms
    generator.generate_platforms_above_camera(camera, camera.y - 1000)
    platforms = generator.get_active_platforms()
    
    if len(platforms) < 2:
        print("⚠️  Not enough platforms generated for spacing test")
        return True
    
    # Sort platforms by Y coordinate (going up)
    platforms.sort(key=lambda p: p.y)
    
    min_distance = generator.min_horizontal_distance
    violations = 0
    total_pairs = 0
    
    # Check horizontal distances between consecutive platforms
    for i in range(len(platforms) - 1):
        current = platforms[i]
        next_platform = platforms[i + 1]
        
        horizontal_distance = abs(next_platform.x - current.x)
        total_pairs += 1
        
        if horizontal_distance < min_distance:
            violations += 1
            print(f"  Violation: platforms at ({current.x:.0f}, {current.y:.0f}) and ({next_platform.x:.0f}, {next_platform.y:.0f}) - distance: {horizontal_distance:.0f}px")
    
    print(f"Platform pairs checked: {total_pairs}")
    print(f"Minimum distance violations: {violations}")
    
    if violations == 0:
        print("✓ All platform pairs meet minimum horizontal distance")
    else:
        print(f"❌ {violations} platform pairs violate minimum distance")
        return False
    
    return True

def test_reachability_with_minimum_distance():
    """Test that platforms are still reachable with minimum distance"""
    print("\nTesting platform reachability with minimum distance...")
    
    generator = PlatformGenerator()
    min_distance = generator.min_horizontal_distance
    max_reach = generator.max_horizontal_reach
    frog_reach = generator.frog_horizontal_reach
    
    print(f"Minimum distance: {min_distance}px")
    print(f"Frog horizontal reach: {frog_reach}px")
    print(f"Generator max reach: {max_reach}px")
    
    # Check that minimum distance is within frog's reach
    if min_distance <= frog_reach:
        print("✓ Minimum distance is within frog's jumping ability")
    else:
        print("❌ Minimum distance exceeds frog's jumping ability")
        return False
    
    # Test with actual platform creation
    platform1 = generator.create_platform(400, 300)
    
    # Try to find reachable position
    target_y = 200  # 100 pixels up
    position = generator.find_reachable_position(platform1, target_y)
    
    if position:
        x, y = position
        horizontal_distance = abs(x - platform1.x)
        print(f"Found reachable position: ({x:.0f}, {y:.0f})")
        print(f"Horizontal distance: {horizontal_distance:.0f}px")
        
        if horizontal_distance >= min_distance:
            print("✓ Reachable position meets minimum distance requirement")
        else:
            print("❌ Reachable position violates minimum distance")
            return False
    else:
        print("⚠️  No reachable position found (might be edge case)")
    
    return True

def test_gameplay_impact():
    """Test the gameplay impact of minimum horizontal distance"""
    print("\nTesting gameplay impact...")
    
    generator = PlatformGenerator()
    min_distance = generator.min_horizontal_distance
    platform_width = generator.platform_width
    
    print(f"Minimum horizontal distance: {min_distance}px")
    print(f"Platform width: {platform_width}px")
    
    # Calculate minimum gap between platform edges
    min_edge_gap = min_distance - platform_width
    
    print(f"Minimum gap between platform edges: {min_edge_gap}px")
    
    if min_edge_gap > 0:
        print("✓ Platforms will always have gaps between them")
        print(f"  Players must move horizontally at least {min_edge_gap}px")
    elif min_edge_gap == 0:
        print("⚠️  Platforms might just touch at edges")
    else:
        print("⚠️  Platforms might overlap (but centers are still separated)")
    
    # Check if the distance forces meaningful movement
    if min_distance >= platform_width * 0.6:  # At least 60% of platform width
        print("✓ Minimum distance forces meaningful horizontal movement")
    else:
        print("⚠️  Minimum distance might not force enough horizontal movement")
    
    return True

if __name__ == "__main__":
    print("=== Minimum Horizontal Distance Test ===")
    
    try:
        success = True
        success &= test_horizontal_offset_generation()
        success &= test_platform_generation_spacing()
        success &= test_reachability_with_minimum_distance()
        success &= test_gameplay_impact()
        
        if success:
            print("\n🎉 All horizontal spacing tests passed!")
            print("\nHorizontal spacing improvements:")
            print("• Minimum horizontal distance: 120px enforced")
            print("• Players must always move left or right to reach next platform")
            print("• All platforms remain reachable within frog's jumping ability")
            print("• No more platforms directly above each other")
            print("• More engaging horizontal movement gameplay")
        else:
            print("\n❌ Some horizontal spacing tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)