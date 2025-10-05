#!/usr/bin/env python3
"""
Comprehensive debug test for conveyor platform issues
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog, PlatformGenerator, Camera
import frog_platformer


def debug_conveyor_creation():
    """Debug conveyor platform creation"""
    print("🔍 DEBUG: Conveyor Platform Creation")
    print("=" * 50)
    
    # Test 1: Direct creation
    print("Test 1: Direct conveyor creation")
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    print(f"  Platform type: {conveyor.platform_type}")
    print(f"  Platform type value: {conveyor.platform_type.value}")
    print(f"  Has conveyor_speed: {hasattr(conveyor, 'conveyor_speed')}")
    print(f"  Has conveyor_direction: {hasattr(conveyor, 'conveyor_direction')}")
    if hasattr(conveyor, 'conveyor_speed'):
        print(f"  Conveyor speed: {conveyor.conveyor_speed}")
        print(f"  Conveyor direction: {conveyor.conveyor_direction}")
    print()
    
    # Test 2: Generator creation
    print("Test 2: Generator conveyor creation")
    generator = PlatformGenerator()
    gen_conveyor = generator.create_platform(500, 300, PlatformType.CONVEYOR)
    print(f"  Platform type: {gen_conveyor.platform_type}")
    print(f"  Has conveyor_speed: {hasattr(gen_conveyor, 'conveyor_speed')}")
    if hasattr(gen_conveyor, 'conveyor_speed'):
        print(f"  Conveyor speed: {gen_conveyor.conveyor_speed}")
        print(f"  Conveyor direction: {gen_conveyor.conveyor_direction}")
    print()
    
    return conveyor


def debug_conveyor_collision(conveyor):
    """Debug conveyor collision detection"""
    print("🔍 DEBUG: Conveyor Collision Detection")
    print("=" * 50)
    
    frog = Frog(400, 300)
    print(f"Initial frog state:")
    print(f"  Position: ({frog.x}, {frog.y})")
    print(f"  Velocity: ({frog.vx}, {frog.vy})")
    print(f"  On conveyor: {frog.on_conveyor}")
    print()
    
    # Position frog above conveyor
    frog.y = 340  # Just above platform
    frog.vy = 5   # Falling
    print(f"Positioned frog above conveyor:")
    print(f"  Frog Y: {frog.y}")
    print(f"  Conveyor Y: {conveyor.y}")
    print(f"  Frog falling: {frog.vy > 0}")
    print()
    
    # Test collision detection
    collision = conveyor.check_collision(frog)
    print(f"Collision detection result: {collision}")
    
    if collision:
        print("Collision detected! Testing collision handling...")
        old_vx = frog.vx
        old_vy = frog.vy
        old_y = frog.y
        
        conveyor.on_collision(frog)
        
        print(f"After collision handling:")
        print(f"  Position change: Y {old_y} → {frog.y}")
        print(f"  Velocity change: VX {old_vx} → {frog.vx}")
        print(f"  Velocity change: VY {old_vy} → {frog.vy}")
        print(f"  On ground: {frog.on_ground}")
        print(f"  On conveyor: {frog.on_conveyor}")
        print(f"  Conveyor platform set: {frog.conveyor_platform is not None}")
        
        return frog
    else:
        print("❌ No collision detected!")
        return None


def debug_conveyor_continuous_effect(frog, conveyor):
    """Debug continuous conveyor effect"""
    print("\n🔍 DEBUG: Continuous Conveyor Effect")
    print("=" * 50)
    
    if not frog:
        print("❌ No frog to test continuous effect")
        return
    
    print("Testing continuous conveyor effect over multiple frames:")
    print("Frame | Frog VX | On Conveyor | Conveyor Platform")
    print("-" * 45)
    
    for frame in range(5):
        old_vx = frog.vx
        
        # Simulate the frog update (this should apply continuous conveyor effect)
        frog.update()
        
        print(f"{frame:5d} | {frog.vx:7.1f} | {str(frog.on_conveyor):11s} | {frog.conveyor_platform is not None}")
        
        # Reset conveyor state (normally done by collision detection)
        if frog.on_conveyor:
            frog.on_conveyor = True
            frog.conveyor_platform = conveyor
    
    print()


def debug_game_loop_integration():
    """Debug conveyor in actual game loop context"""
    print("🔍 DEBUG: Game Loop Integration")
    print("=" * 50)
    
    # Initialize game components
    frog = Frog(400, 300)
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    platforms = [conveyor]
    
    print("Simulating actual game loop order:")
    print("1. Handle input (skipped)")
    print("2. Update frog")
    print("3. Check platform collisions")
    print("4. Update platforms")
    print()
    
    # Position frog above conveyor
    frog.y = 340
    frog.vy = 5
    frog.vx = 0
    
    print("Initial state:")
    print(f"  Frog: ({frog.x:.1f}, {frog.y:.1f}) vel=({frog.vx:.1f}, {frog.vy:.1f})")
    print()
    
    for frame in range(3):
        print(f"Frame {frame}:")
        
        # Step 2: Update frog
        print("  Before frog.update():")
        print(f"    VX: {frog.vx:.1f}, On conveyor: {frog.on_conveyor}")
        
        frog.update()
        
        print("  After frog.update():")
        print(f"    VX: {frog.vx:.1f}, Position: ({frog.x:.1f}, {frog.y:.1f})")
        
        # Step 3: Check platform collisions
        print("  Before collision check:")
        print(f"    On conveyor: {frog.on_conveyor}")
        
        frog.check_platform_collision(platforms)
        
        print("  After collision check:")
        print(f"    VX: {frog.vx:.1f}, On ground: {frog.on_ground}, On conveyor: {frog.on_conveyor}")
        
        # Step 4: Update platforms
        for platform in platforms:
            platform.update(1/60)
        
        print()


def debug_platform_generation():
    """Debug if conveyors are being generated in the game"""
    print("🔍 DEBUG: Platform Generation")
    print("=" * 50)
    
    generator = PlatformGenerator()
    camera = Camera()
    
    # Force generation at height where conveyors should appear
    print("Generating platforms at height 200 (conveyors available at 100+):")
    generator.generate_platforms_above_camera(camera, camera.y - 1000)
    
    # Count platform types
    type_counts = {}
    conveyor_platforms = []
    
    for platform in generator.active_platforms:
        ptype = platform.platform_type
        type_counts[ptype] = type_counts.get(ptype, 0) + 1
        
        if ptype == PlatformType.CONVEYOR:
            conveyor_platforms.append(platform)
    
    print("Platform distribution:")
    for ptype, count in type_counts.items():
        print(f"  {ptype.value}: {count}")
    
    print(f"\nConveyor platforms found: {len(conveyor_platforms)}")
    
    if conveyor_platforms:
        print("Sample conveyor details:")
        conv = conveyor_platforms[0]
        print(f"  Position: ({conv.x}, {conv.y})")
        print(f"  Type: {conv.platform_type}")
        print(f"  Speed: {getattr(conv, 'conveyor_speed', 'MISSING!')}")
        print(f"  Direction: {getattr(conv, 'conveyor_direction', 'MISSING!')}")
        
        # Test this conveyor
        print("\nTesting generated conveyor:")
        test_frog = Frog(conv.x, conv.y - 20)
        test_frog.vy = 5
        
        if conv.check_collision(test_frog):
            conv.on_collision(test_frog)
            print(f"  Collision test: VX changed to {test_frog.vx}")
        else:
            print("  Collision test: No collision")


if __name__ == '__main__':
    print("🐛 COMPREHENSIVE CONVEYOR DEBUG")
    print("=" * 70)
    
    # Run all debug tests
    conveyor = debug_conveyor_creation()
    frog = debug_conveyor_collision(conveyor)
    debug_conveyor_continuous_effect(frog, conveyor)
    debug_game_loop_integration()
    debug_platform_generation()
    
    print("\n" + "=" * 70)
    print("🔍 Debug complete! Check output above for issues.")