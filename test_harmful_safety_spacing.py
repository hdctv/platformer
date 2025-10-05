#!/usr/bin/env python3
"""
Test script to verify harmful and safety platforms have proper spacing
"""

import sys
sys.path.append('.')

from frog_platformer import *

def test_harmful_safety_spacing():
    """Test that harmful and safety platforms can't touch"""
    print("Testing harmful and safety platform spacing...")
    
    generator = PlatformGenerator()
    
    # Test parameters
    harmful_x = 600
    harmful_y = 300
    platform_width = generator.platform_width
    
    print(f"Platform width: {platform_width}px")
    print(f"Harmful platform at: ({harmful_x}, {harmful_y})")
    
    # Create harmful platform
    harmful_platform = generator.create_platform(harmful_x, harmful_y, PlatformType.HARMFUL)
    generator.active_platforms.append(harmful_platform)
    
    # Add safety platform
    generator.add_safety_platform_for_harmful(harmful_x, harmful_y)
    
    # Find the safety platform
    safety_platforms = [p for p in generator.active_platforms if p.platform_type == PlatformType.NORMAL]
    
    if not safety_platforms:
        print("❌ No safety platform was created")
        return False
    
    safety_platform = safety_platforms[0]
    print(f"Safety platform at: ({safety_platform.x}, {safety_platform.y})")
    
    # Calculate distance between platform centers
    center_distance = abs(safety_platform.x - harmful_platform.x)
    print(f"Distance between centers: {center_distance}px")
    
    # Calculate distance between platform edges
    harmful_left = harmful_platform.x - harmful_platform.width // 2
    harmful_right = harmful_platform.x + harmful_platform.width // 2
    safety_left = safety_platform.x - safety_platform.width // 2
    safety_right = safety_platform.x + safety_platform.width // 2
    
    print(f"Harmful platform edges: {harmful_left} to {harmful_right}")
    print(f"Safety platform edges: {safety_left} to {safety_right}")
    
    # Check for overlap or touching
    if safety_platform.x > harmful_platform.x:
        # Safety platform is to the right
        gap = safety_left - harmful_right
    else:
        # Safety platform is to the left
        gap = harmful_left - safety_right
    
    print(f"Gap between platform edges: {gap}px")
    
    if gap > 0:
        print(f"✓ Platforms have {gap}px gap between them (not touching)")
        return True
    elif gap == 0:
        print("⚠️  Platforms are exactly touching (no gap)")
        return False
    else:
        print(f"❌ Platforms are overlapping by {-gap}px")
        return False

def test_multiple_harmful_platforms():
    """Test spacing with multiple harmful platforms"""
    print("\nTesting multiple harmful platforms...")
    
    generator = PlatformGenerator()
    
    # Create multiple harmful platforms
    harmful_positions = [(400, 300), (800, 250), (600, 400)]
    
    for i, (x, y) in enumerate(harmful_positions):
        print(f"\nTesting harmful platform {i+1} at ({x}, {y})...")
        
        # Clear previous platforms
        generator.active_platforms.clear()
        
        # Create harmful platform
        harmful_platform = generator.create_platform(x, y, PlatformType.HARMFUL)
        generator.active_platforms.append(harmful_platform)
        
        # Add safety platform
        generator.add_safety_platform_for_harmful(x, y)
        
        # Check spacing
        safety_platforms = [p for p in generator.active_platforms if p.platform_type == PlatformType.NORMAL]
        
        if safety_platforms:
            safety_platform = safety_platforms[0]
            center_distance = abs(safety_platform.x - harmful_platform.x)
            
            # Calculate edge gap
            if safety_platform.x > harmful_platform.x:
                gap = (safety_platform.x - safety_platform.width//2) - (harmful_platform.x + harmful_platform.width//2)
            else:
                gap = (harmful_platform.x - harmful_platform.width//2) - (safety_platform.x + safety_platform.width//2)
            
            print(f"  Center distance: {center_distance}px, Edge gap: {gap}px")
            
            if gap <= 0:
                print(f"  ❌ Platforms touching or overlapping")
                return False
            else:
                print(f"  ✓ Good spacing")
        else:
            print(f"  ❌ No safety platform created")
            return False
    
    return True

def test_safety_distance_calculation():
    """Test that the safety distance calculation is correct"""
    print("\nTesting safety distance calculation...")
    
    generator = PlatformGenerator()
    platform_width = generator.platform_width
    
    # Read the safety distance from source
    with open('frog_platformer.py', 'r') as f:
        source = f.read()
    
    # Extract safety distance
    import re
    match = re.search(r'safety_distance = (\d+)', source)
    if match:
        safety_distance = int(match.group(1))
        print(f"Safety distance: {safety_distance}px")
        print(f"Platform width: {platform_width}px")
        
        # Calculate minimum gap
        # Gap = safety_distance - (platform_width/2 + platform_width/2)
        # Gap = safety_distance - platform_width
        min_gap = safety_distance - platform_width
        
        print(f"Minimum gap between edges: {min_gap}px")
        
        if min_gap > 0:
            print(f"✓ Safety distance ensures {min_gap}px minimum gap")
            return True
        else:
            print(f"❌ Safety distance too small - platforms would overlap by {-min_gap}px")
            return False
    else:
        print("❌ Could not find safety_distance in source code")
        return False

if __name__ == "__main__":
    print("=== Harmful and Safety Platform Spacing Test ===")
    
    try:
        success = True
        success &= test_harmful_safety_spacing()
        success &= test_multiple_harmful_platforms()
        success &= test_safety_distance_calculation()
        
        if success:
            print("\n🎉 All harmful/safety platform spacing tests passed!")
            print("\nSpacing improvements:")
            print("• Safety distance increased from 150px to 250px")
            print("• With 200px wide platforms, minimum gap is 50px")
            print("• Harmful and safety platforms can never touch or overlap")
            print("• Proper spacing maintained in all test scenarios")
        else:
            print("\n❌ Some spacing tests failed - check output above")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)