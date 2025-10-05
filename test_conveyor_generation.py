#!/usr/bin/env python3
"""
Test to check if conveyor platforms are being generated
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, PlatformType, Camera


def test_conveyor_generation():
    """Test if conveyor platforms are generated at appropriate heights"""
    print("🎢 Testing Conveyor Platform Generation")
    print("=" * 50)
    
    # Create generator and camera
    generator = PlatformGenerator()
    camera = Camera()
    
    # Generate platforms at height where conveyors should appear (height 100+)
    generator.generate_platforms_above_camera(camera, camera.y - 1000)
    
    # Count platform types
    platform_counts = {}
    for platform in generator.active_platforms:
        ptype = platform.platform_type
        platform_counts[ptype] = platform_counts.get(ptype, 0) + 1
    
    print("Platform type distribution:")
    for ptype, count in platform_counts.items():
        print(f"  {ptype.value}: {count}")
    
    conveyor_count = platform_counts.get(PlatformType.CONVEYOR, 0)
    total_platforms = len(generator.active_platforms)
    
    print(f"\nTotal platforms: {total_platforms}")
    print(f"Conveyor platforms: {conveyor_count}")
    
    if conveyor_count > 0:
        percentage = (conveyor_count / total_platforms) * 100
        print(f"Conveyor percentage: {percentage:.1f}%")
        print("✅ Conveyors are being generated!")
        
        # Test a specific conveyor
        conveyor = next(p for p in generator.active_platforms if p.platform_type == PlatformType.CONVEYOR)
        print(f"\nSample conveyor:")
        print(f"  Position: ({conveyor.x}, {conveyor.y})")
        print(f"  Direction: {conveyor.conveyor_direction}")
        print(f"  Speed: {conveyor.conveyor_speed}")
        print(f"  Color: {conveyor.color}")
        
        return True
    else:
        print("❌ No conveyor platforms generated!")
        print("This could be due to:")
        print("- Random chance (30% probability)")
        print("- Height requirements not met")
        print("- Bug in generation logic")
        return False


def test_conveyor_at_specific_height():
    """Test conveyor generation at specific height with forced selection"""
    print("\n🎯 Testing Conveyor at Specific Height")
    print("=" * 50)
    
    generator = PlatformGenerator()
    
    # Test platform type selection at height 150 (above conveyor threshold)
    print("Testing platform type selection at height 150:")
    for i in range(10):
        ptype = generator.select_platform_type(150)
        print(f"  Attempt {i+1}: {ptype.value}")
    
    # Force conveyor creation
    print("\nForce creating conveyor platform:")
    conveyor = generator.create_platform(400, 300, PlatformType.CONVEYOR)
    print(f"  Created: {conveyor.platform_type.value}")
    print(f"  Position: ({conveyor.x}, {conveyor.y})")
    print(f"  Direction: {conveyor.conveyor_direction}")
    print(f"  Speed: {conveyor.conveyor_speed}")
    
    return True


if __name__ == '__main__':
    print("🎢 Conveyor Platform Generation Tests")
    print("=" * 60)
    
    success1 = test_conveyor_generation()
    success2 = test_conveyor_at_specific_height()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 Conveyor generation tests completed!")
    else:
        print("⚠️ Some issues found with conveyor generation")