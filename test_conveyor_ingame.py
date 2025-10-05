#!/usr/bin/env python3
"""
Test conveyor platforms in a game-like scenario
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


def test_conveyor_game_simulation():
    """Simulate the game loop with conveyor platforms"""
    print("🎮 Simulating Game Loop with Conveyor Platforms")
    print("=" * 60)
    
    # Create frog and conveyor platform
    frog = Frog(400, 300)
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    platforms = [conveyor]
    
    print(f"Conveyor direction: {conveyor.conveyor_direction}")
    print(f"Conveyor speed: {conveyor.conveyor_speed}")
    print(f"Initial frog position: ({frog.x:.1f}, {frog.y:.1f})")
    print(f"Initial frog velocity: ({frog.vx:.1f}, {frog.vy:.1f})")
    print()
    
    # Simulate frog falling onto conveyor
    frog.y = 340  # Just above platform
    frog.vy = 5   # Falling downward
    frog.vx = 0   # No horizontal movement
    
    print("🎯 Simulating game frames:")
    print("Frame | Frog X  | Frog Y  | Frog VX | Frog VY | On Ground | On Conveyor")
    print("-" * 70)
    
    for frame in range(15):
        # Simulate game loop order:
        # 1. Update frog physics
        frog.update()
        
        # 2. Check platform collisions
        frog.check_platform_collision(platforms)
        
        # 3. Update platforms
        for platform in platforms:
            platform.update(1/60)
        
        # Print frame info
        print(f"{frame:5d} | {frog.x:7.1f} | {frog.y:7.1f} | {frog.vx:7.1f} | {frog.vy:7.1f} | {str(frog.on_ground):9s} | {str(frog.on_conveyor):10s}")
        
        # Stop if frog falls too far
        if frog.y > 500:
            print("Frog fell off screen!")
            break
    
    print()
    print("🔍 Analysis:")
    if abs(frog.vx) > 0.1:
        print(f"✅ Conveyor effect working! Final horizontal velocity: {frog.vx:.1f}")
        if frog.x != 400:
            print(f"✅ Frog moved horizontally from {400} to {frog.x:.1f}")
        else:
            print("⚠️ Frog didn't move horizontally despite having velocity")
    else:
        print("❌ No conveyor effect detected!")
        print("Possible issues:")
        print("- Frog not landing on conveyor")
        print("- Conveyor state not being set")
        print("- Continuous effect not working")
    
    return abs(frog.vx) > 0.1


def test_conveyor_step_by_step():
    """Test conveyor mechanics step by step"""
    print("\n🔬 Step-by-Step Conveyor Analysis")
    print("=" * 60)
    
    frog = Frog(400, 300)
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    
    print("Step 1: Initial state")
    print(f"  Frog: x={frog.x}, y={frog.y}, vx={frog.vx}, vy={frog.vy}")
    print(f"  On conveyor: {frog.on_conveyor}")
    print()
    
    print("Step 2: Position frog above conveyor")
    frog.y = 340  # Just above platform
    frog.vy = 5   # Falling
    print(f"  Frog: x={frog.x}, y={frog.y}, vx={frog.vx}, vy={frog.vy}")
    print()
    
    print("Step 3: Check collision")
    collision = conveyor.check_collision(frog)
    print(f"  Collision detected: {collision}")
    
    if collision:
        print("Step 4: Handle collision")
        conveyor.on_collision(frog)
        print(f"  After collision: x={frog.x}, y={frog.y}, vx={frog.vx}, vy={frog.vy}")
        print(f"  On ground: {frog.on_ground}")
        print(f"  On conveyor: {frog.on_conveyor}")
        print()
        
        print("Step 5: Update frog (continuous effect)")
        old_vx = frog.vx
        frog.update()
        print(f"  VX change: {old_vx} → {frog.vx} (change: {frog.vx - old_vx:+.1f})")
        print(f"  On conveyor after update: {frog.on_conveyor}")
        print()
        
        print("Step 6: Reset conveyor state and check collision again")
        frog.check_platform_collision([conveyor])
        print(f"  On conveyor after collision check: {frog.on_conveyor}")
        
        return True
    else:
        print("❌ No collision detected - frog not positioned correctly")
        return False


if __name__ == '__main__':
    print("🎢 Conveyor Platform In-Game Testing")
    print("=" * 70)
    
    success1 = test_conveyor_step_by_step()
    success2 = test_conveyor_game_simulation() if success1 else False
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 Conveyor platforms working correctly in game simulation!")
    else:
        print("❌ Issues found with conveyor platform mechanics")