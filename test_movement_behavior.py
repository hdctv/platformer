#!/usr/bin/env python3
"""
Test movement behavior on different platform types
"""

import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


def simulate_input_handling(frog, direction=0):
    """Simulate the input handling that happens in the actual game"""
    frog.move_horizontal(direction)


def test_normal_platform_behavior():
    """Test that frog stops on normal platforms when no input is given"""
    print("🟤 Testing Normal Platform Behavior")
    print("=" * 50)
    
    frog = Frog(400, 300)
    normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
    platforms = [normal_platform]
    
    # Position frog on platform
    frog.y = 335
    frog.vy = 0
    frog.vx = 0
    frog.on_ground = True
    
    print("Test 1: Frog should stop when no input is given")
    print("Frame | Input | Before | After Input | Expected")
    print("-" * 45)
    
    # Give some initial velocity, then stop input
    frog.vx = 5.0  # Start with some velocity
    
    for frame in range(3):
        old_vx = frog.vx
        simulate_input_handling(frog, 0)  # No input
        
        expected = "Should be 0" if frame == 0 else "Should stay 0"
        print(f"{frame:5d} | {0:5d} | {old_vx:6.1f} | {frog.vx:11.1f} | {expected}")
    
    if frog.vx == 0:
        print("✅ Normal platform: Frog stops when no input (correct)")
        return True
    else:
        print(f"❌ Normal platform: Frog still moving at {frog.vx} (incorrect)")
        return False


def test_conveyor_platform_behavior():
    """Test that frog continues moving on conveyor platforms"""
    print("\n🔄 Testing Conveyor Platform Behavior")
    print("=" * 50)
    
    frog = Frog(400, 300)
    conveyor_platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    platforms = [conveyor_platform]
    
    # Position frog on conveyor
    frog.y = 335
    frog.vy = 0
    frog.vx = 0
    frog.on_ground = True
    frog.on_conveyor = True
    frog.conveyor_platform = conveyor_platform
    
    print("Test 2: Frog should be pushed by conveyor even without input")
    print("Frame | Input | Before | After Input | Conveyor Effect")
    print("-" * 55)
    
    for frame in range(3):
        old_vx = frog.vx
        simulate_input_handling(frog, 0)  # No input
        
        # Simulate conveyor effect (normally done in collision/update)
        if frog.on_conveyor:
            frog.vx += conveyor_platform.conveyor_speed * conveyor_platform.conveyor_direction * 0.8
        
        effect = f"Pushed to {frog.vx:.1f}"
        print(f"{frame:5d} | {0:5d} | {old_vx:6.1f} | {frog.vx:11.1f} | {effect}")
    
    if frog.vx > 5:
        print("✅ Conveyor platform: Frog pushed by conveyor (correct)")
        return True
    else:
        print(f"❌ Conveyor platform: Frog not pushed enough: {frog.vx} (incorrect)")
        return False


def test_player_input_override():
    """Test that player input works on both platform types"""
    print("\n🕹️ Testing Player Input Override")
    print("=" * 50)
    
    # Test normal platform
    frog1 = Frog(400, 300)
    frog1.vx = 0
    simulate_input_handling(frog1, 1)  # Move right
    normal_result = frog1.vx
    
    # Test conveyor platform
    frog2 = Frog(400, 300)
    frog2.vx = 0
    frog2.on_conveyor = True
    frog2.conveyor_platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    simulate_input_handling(frog2, 1)  # Move right
    conveyor_result = frog2.vx
    
    print(f"Normal platform with right input: {normal_result}")
    print(f"Conveyor platform with right input: {conveyor_result}")
    
    if normal_result == 3.0 and conveyor_result == 3.0:
        print("✅ Player input works on both platform types (correct)")
        return True
    else:
        print("❌ Player input not working correctly")
        return False


def test_realistic_game_scenario():
    """Test a realistic game scenario with platform switching"""
    print("\n🎮 Testing Realistic Game Scenario")
    print("=" * 50)
    
    frog = Frog(400, 300)
    normal_platform = Platform(300, 350, 100, 20, PlatformType.NORMAL)
    conveyor_platform = Platform(500, 350, 100, 20, PlatformType.CONVEYOR)
    
    print("Scenario: Frog jumps from normal platform to conveyor platform")
    print("Phase | Platform | Input | VX | Description")
    print("-" * 50)
    
    # Phase 1: On normal platform, no input
    frog.vx = 0
    frog.on_conveyor = False
    simulate_input_handling(frog, 0)
    print(f"  1   | Normal   |   0   | {frog.vx:.1f} | Should stay still")
    
    # Phase 2: On normal platform, move right
    simulate_input_handling(frog, 1)
    print(f"  2   | Normal   |   1   | {frog.vx:.1f} | Should move right")
    
    # Phase 3: Land on conveyor, no input
    frog.on_conveyor = True
    frog.conveyor_platform = conveyor_platform
    old_vx = frog.vx
    simulate_input_handling(frog, 0)
    # Simulate conveyor effect
    frog.vx += conveyor_platform.conveyor_speed * conveyor_platform.conveyor_direction * 0.8
    print(f"  3   | Conveyor |   0   | {frog.vx:.1f} | Should be pushed by conveyor")
    
    # Phase 4: On conveyor, try to move left
    simulate_input_handling(frog, -1)
    frog.vx += conveyor_platform.conveyor_speed * conveyor_platform.conveyor_direction * 0.8
    print(f"  4   | Conveyor |  -1   | {frog.vx:.1f} | Left input + conveyor push")
    
    print("\n✅ Realistic scenario test completed")
    return True


if __name__ == '__main__':
    print("🎮 MOVEMENT BEHAVIOR TESTS")
    print("=" * 60)
    
    success1 = test_normal_platform_behavior()
    success2 = test_conveyor_platform_behavior()
    success3 = test_player_input_override()
    success4 = test_realistic_game_scenario()
    
    print("\n" + "=" * 60)
    if success1 and success2 and success3 and success4:
        print("🎉 All movement behavior tests passed!")
    else:
        print("❌ Some movement behavior tests failed!")