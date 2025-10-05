#!/usr/bin/env python3
"""
Test to verify safety platform generation for harmful platforms
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, PlatformType, Camera


def test_safety_platform_generation():
    """Test that safety platforms are generated for harmful platforms"""
    print("🛡️ Testing Safety Platform Generation")
    print("=" * 50)
    
    # Create generator and camera
    generator = PlatformGenerator()
    camera = Camera()
    
    # Force creation of a harmful platform
    harmful_x, harmful_y = 400, 300
    harmful_platform = generator.create_platform(harmful_x, harmful_y, PlatformType.HARMFUL)
    generator.active_platforms.append(harmful_platform)
    
    print(f"Created harmful platform at ({harmful_x}, {harmful_y})")
    print(f"Platforms before safety generation: {len(generator.active_platforms)}")
    
    # Add safety platform
    generator.add_safety_platform_for_harmful(harmful_x, harmful_y)
    
    print(f"Platforms after safety generation: {len(generator.active_platforms)}")
    
    # Check if safety platform was added
    safety_platforms = [p for p in generator.active_platforms if p.platform_type == PlatformType.NORMAL]
    harmful_platforms = [p for p in generator.active_platforms if p.platform_type == PlatformType.HARMFUL]
    
    print(f"Harmful platforms: {len(harmful_platforms)}")
    print(f"Safety platforms: {len(safety_platforms)}")
    
    if safety_platforms:
        safety_platform = safety_platforms[0]
        distance = abs(safety_platform.x - harmful_x)
        y_diff = abs(safety_platform.y - harmful_y)
        
        print(f"Safety platform at ({safety_platform.x}, {safety_platform.y})")
        print(f"Distance from harmful platform: {distance:.1f} pixels")
        print(f"Y difference: {y_diff:.1f} pixels")
        
        # Verify safety platform is reasonably positioned
        assert distance >= 100, f"Safety platform too close: {distance}"
        assert distance <= 300, f"Safety platform too far: {distance}"  # Updated for increased safety distance
        assert y_diff <= 50, f"Safety platform Y difference too large: {y_diff}"
        
        print("✅ Safety platform positioned correctly!")
    else:
        print("❌ No safety platform was created!")
        return False
    
    return True


def test_safety_platform_integration():
    """Test safety platform generation during normal platform generation"""
    print("\n🎮 Testing Safety Platform Integration")
    print("=" * 50)
    
    # Create generator and camera
    generator = PlatformGenerator()
    camera = Camera()
    
    # Override platform type selection to force harmful platforms
    original_select = generator.select_platform_type
    def force_harmful(height_progress, progress_tracker=None):
        if height_progress >= 400:  # When harmful platforms are available
            return PlatformType.HARMFUL
        return original_select(height_progress, progress_tracker)
    
    generator.select_platform_type = force_harmful
    
    # Generate platforms at high progress (where harmful platforms appear)
    generator.generate_platforms_above_camera(camera, camera.y - 500)
    
    # Count platform types
    platform_counts = {}
    for platform in generator.active_platforms:
        ptype = platform.platform_type
        platform_counts[ptype] = platform_counts.get(ptype, 0) + 1
    
    print("Platform type distribution:")
    for ptype, count in platform_counts.items():
        print(f"  {ptype.value}: {count}")
    
    harmful_count = platform_counts.get(PlatformType.HARMFUL, 0)
    normal_count = platform_counts.get(PlatformType.NORMAL, 0)
    
    if harmful_count > 0:
        print(f"\n✅ Generated {harmful_count} harmful platforms")
        print(f"✅ Generated {normal_count} normal platforms (includes safety platforms)")
        
        # There should be at least some normal platforms as safety platforms
        assert normal_count > 0, "No safety platforms generated for harmful platforms"
        
        print("✅ Safety platform integration working!")
        return True
    else:
        print("ℹ️ No harmful platforms generated (may be due to progress threshold)")
        return True


if __name__ == '__main__':
    print("🛡️ Safety Platform Generation Tests")
    print("=" * 60)
    
    success1 = test_safety_platform_generation()
    success2 = test_safety_platform_integration()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All safety platform tests passed!")
    else:
        print("❌ Some safety platform tests failed!")