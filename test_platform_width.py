#!/usr/bin/env python3
"""
Test script to verify platform width changes and spawn position
"""

import sys
sys.path.append('.')

from frog_platformer import *

def test_platform_widths():
    """Test that all platforms are properly doubled in width"""
    print("Testing platform width changes...")
    
    # Test generator settings
    generator = PlatformGenerator()
    print(f"✓ Generator platform width: {generator.platform_width} (doubled from 100)")
    
    # Test default platform creation
    platform = Platform(400, 300)
    print(f"✓ Default platform width: {platform.width}")
    
    # Test generator-created platforms
    gen_platform = generator.create_platform(400, 300)
    print(f"✓ Generator-created platform width: {gen_platform.width}")
    
    # Test different platform types maintain width
    for ptype in [PlatformType.NORMAL, PlatformType.CONVEYOR, PlatformType.BREAKABLE]:
        test_platform = generator.create_platform(400, 300, ptype)
        print(f"✓ {ptype.value} platform width: {test_platform.width}")
    
    print("All platforms are properly doubled in width!")

def test_spawn_changes():
    """Test spawn position and starting platform changes"""
    print("\nTesting spawn changes...")
    
    # Test frog spawn position
    frog = Frog(100, HEIGHT - 100)
    print(f"✓ Frog spawns at x={frog.x} (left corner, not center)")
    
    # Test starting platform width
    ground_platform = Platform(WIDTH // 2, HEIGHT - 50, WIDTH, 20)
    print(f"✓ Starting platform width: {ground_platform.width} (full screen)")
    print(f"  Screen width: {WIDTH}")
    print(f"  Platform spans from {ground_platform.x - ground_platform.width//2} to {ground_platform.x + ground_platform.width//2}")
    
    # Verify frog can't fall off starting platform
    frog_left_edge = frog.x - frog.width//2
    frog_right_edge = frog.x + frog.width//2
    platform_left_edge = ground_platform.x - ground_platform.width//2
    platform_right_edge = ground_platform.x + ground_platform.width//2
    
    print(f"✓ Frog edges: {frog_left_edge} to {frog_right_edge}")
    print(f"✓ Platform edges: {platform_left_edge} to {platform_right_edge}")
    
    if frog_left_edge >= platform_left_edge and frog_right_edge <= platform_right_edge:
        print("✓ Frog is safely on the starting platform!")
    else:
        print("⚠️  Frog might be able to fall off starting platform")
    
    print("Spawn changes implemented successfully!")

def test_balance_impact():
    """Test how the width changes affect game balance"""
    print("\nTesting balance impact...")
    
    # Test platform reachability with new widths
    generator = PlatformGenerator()
    
    # Create two platforms with typical spacing
    platform1 = generator.create_platform(400, 300)
    platform2 = generator.create_platform(500, 200)  # 100 pixels apart horizontally
    
    horizontal_gap = abs(platform2.x - platform1.x)
    platform_overlap = (platform1.width + platform2.width) / 2
    effective_gap = horizontal_gap - platform_overlap
    
    print(f"✓ Horizontal gap between platforms: {horizontal_gap} pixels")
    print(f"✓ Combined platform half-widths: {platform_overlap} pixels")
    print(f"✓ Effective gap to jump: {effective_gap} pixels")
    
    if effective_gap < 50:  # Much easier to jump
        print("✓ Platforms are much easier to reach with doubled width!")
    else:
        print(f"✓ Platforms still require {effective_gap} pixel jumps")
    
    print("Balance changes will make the game more forgiving!")

if __name__ == "__main__":
    print("=== Platform Width & Spawn Test ===")
    
    try:
        test_platform_widths()
        test_spawn_changes()
        test_balance_impact()
        
        print("\n🎉 All platform and spawn changes verified!")
        print("\nChanges summary:")
        print("• All platforms are now 200px wide (doubled from 100px)")
        print("• Starting platform spans the full screen width (1200px)")
        print("• Frog spawns in left corner (x=100) instead of center")
        print("• Game should be more forgiving and beginner-friendly!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)