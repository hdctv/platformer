#!/usr/bin/env python3
"""
Test conveyor platforms with input handling simulation
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


def simulate_input_handling(frog, direction=0):
    """Simulate the input handling that happens in the actual game"""
    # This simulates what handle_input() does
    frog.move_horizontal(direction)


def test_conveyor_with_input_simulation():
    """Test conveyor with realistic input handling"""
    print("🎮 Testing Conveyor with Input Handling Simulation")
    print("=" * 60)
    
    frog = Frog(400, 300)
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    platforms = [conveyor]
    
    # Position frog above conveyor
    frog.y = 340
    frog.vy = 5
    frog.vx = 0
    
    print("Simulating realistic game loop with input handling:")
    print("Frame | Input Dir | Before Input | After Input | After Update | After Collision")
    print("-" * 80)
    
    for frame in range(8):
        # Simulate no input (this was the problem!)
        input_direction = 0
        
        old_vx_before_input = frog.vx
        
        # Step 1: Handle input (this was overriding conveyor effect!)
        simulate_input_handling(frog, input_direction)
        vx_after_input = frog.vx
        
        # Step 2: Update frog physics
        frog.update()
        vx_after_update = frog.vx
        
        # Step 3: Check platform collisions
        frog.check_platform_collision(platforms)
        vx_after_collision = frog.vx
        
        print(f"{frame:5d} | {input_direction:9d} | {old_vx_before_input:12.1f} | {vx_after_input:11.1f} | {vx_after_update:12.1f} | {vx_after_collision:15.1f}")
        
        # Stop if frog moves too far
        if abs(frog.x - 400) > 200:
            print("Frog moved too far, stopping simulation")
            break
    
    print()
    final_distance = abs(frog.x - 400)
    print(f"Final frog position: ({frog.x:.1f}, {frog.y:.1f})")
    print(f"Distance moved: {final_distance:.1f} pixels")
    
    if final_distance > 50:
        print("✅ Conveyor effect working! Frog moved significantly.")
        return True
    else:
        print("❌ Conveyor effect not working. Frog barely moved.")
        return False


def test_conveyor_with_player_input():
    """Test conveyor with player trying to counteract it"""
    print("\n🕹️ Testing Conveyor with Player Input")
    print("=" * 60)
    
    frog = Frog(400, 300)
    conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)  # Pushes right
    platforms = [conveyor]
    
    # Position frog on conveyor
    frog.y = 335
    frog.vy = 0
    frog.vx = 0
    frog.on_ground = True
    frog.on_conveyor = True
    frog.conveyor_platform = conveyor
    
    print("Player tries to move left while conveyor pushes right:")
    print("Frame | Player Input | Conveyor Push | Final VX | Net Effect")
    print("-" * 60)
    
    for frame in range(5):
        # Player tries to move left (-1)
        player_input = -1
        
        # Apply player input
        simulate_input_handling(frog, player_input)
        vx_after_input = frog.vx
        
        # Apply conveyor effect (simulated)
        conveyor_push = conveyor.conveyor_speed * conveyor.conveyor_direction
        frog.vx += conveyor_push
        
        net_effect = "Left" if frog.vx < 0 else "Right" if frog.vx > 0 else "None"
        
        print(f"{frame:5d} | {player_input:12d} | {conveyor_push:13.1f} | {frog.vx:8.1f} | {net_effect}")
    
    print()
    if frog.vx > 0:
        print("✅ Conveyor overpowers player input (as expected)")
        return True
    else:
        print("❌ Player input overpowers conveyor (unexpected)")
        return False


if __name__ == '__main__':
    print("🎢 CONVEYOR + INPUT HANDLING TESTS")
    print("=" * 70)
    
    success1 = test_conveyor_with_input_simulation()
    success2 = test_conveyor_with_player_input()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 Conveyor platforms work correctly with input handling!")
    else:
        print("❌ Issues found with conveyor + input interaction")