#!/usr/bin/env python3
"""
Test script for the laser obstacle system
"""

import sys
sys.path.append('.')

from frog_platformer import Laser, LaserState, Frog, GAME_CONFIG
import time

def test_laser_basic_functionality():
    """Test basic laser creation and state transitions"""
    print("Testing laser basic functionality...")
    
    # Create laser
    laser = Laser(100, 'left')
    print(f"Initial state: {laser.state}")
    print(f"Initial position: y={laser.y}, side={laser.side}")
    print(f"Warning duration: {laser.warning_duration}s")
    print(f"Firing duration: {laser.firing_duration}s")
    
    # Test warning phase
    assert laser.state == LaserState.WARNING
    assert laser.get_warning_color() == 'red'
    
    # Simulate time passing
    laser.update(1.0)  # 1 second
    print(f"After 1s: state={laser.state}, color={laser.get_warning_color()}")
    
    laser.update(1.5)  # Total 2.5 seconds (past warning duration)
    print(f"After 2.5s: state={laser.state}, firing={laser.is_firing()}")
    
    # Should be firing now
    assert laser.state == LaserState.FIRING
    assert laser.is_firing()
    
    # Simulate firing duration
    laser.update(0.5)  # Total 3.0 seconds
    print(f"After 3s: state={laser.state}, active={laser.active}")
    
    # Should be inactive now
    assert laser.state == LaserState.INACTIVE
    assert not laser.active
    
    print("✓ Basic laser functionality test passed!")

def test_laser_collision():
    """Test laser collision detection with frog"""
    print("\nTesting laser collision detection...")
    
    # Create laser and frog
    laser = Laser(200, 'left')
    frog = Frog(400, 200)  # Same Y as laser
    
    # Should not collide during warning phase
    collision = laser.check_collision(frog)
    print(f"Collision during warning: {collision}")
    assert not collision
    
    # Move to firing phase
    laser.update(2.5)  # Past warning duration
    assert laser.is_firing()
    
    # Should collide now (frog is at same Y level)
    collision = laser.check_collision(frog)
    print(f"Collision during firing: {collision}")
    assert collision
    
    # Test frog collision checking
    frog.hit_by_laser = False
    frog.check_laser_collision([laser])
    print(f"Frog hit by laser: {frog.hit_by_laser}")
    assert frog.hit_by_laser
    
    print("✓ Laser collision test passed!")

def test_laser_visual_properties():
    """Test laser visual properties and oscillation"""
    print("\nTesting laser visual properties...")
    
    laser = Laser(150, 'right')
    
    # Test warning circle oscillation
    initial_radius = laser.get_warning_radius()
    print(f"Initial warning radius: {initial_radius}")
    
    # Simulate some time for oscillation
    laser.update(0.25)  # Quarter second
    new_radius = laser.get_warning_radius()
    print(f"Radius after 0.25s: {new_radius}")
    
    # Test color transition
    laser.timer = 0.5  # Early in warning
    color1 = laser.get_warning_color()
    laser.timer = 1.5  # Late in warning
    color2 = laser.get_warning_color()
    print(f"Early warning color: {color1}, Late warning color: {color2}")
    
    # Should transition from red to blue
    assert color1 == 'red'
    assert color2 == 'blue'
    
    print("✓ Laser visual properties test passed!")

def test_laser_configuration():
    """Test laser configuration values"""
    print("\nTesting laser configuration...")
    
    config = GAME_CONFIG['laser_config']
    print(f"Introduction height: {config['introduction_height']}")
    print(f"Warning duration: {config['warning_duration']}s")
    print(f"Firing duration: {config['firing_duration']}s")
    print(f"Laser height: {config['laser_height']} pixels")
    print(f"Spawn chance: {config['spawn_chance'] * 100}%")
    print(f"Oscillation speed: {config['warning_oscillation_speed']} Hz")
    
    # Verify reasonable values
    assert config['introduction_height'] == 50000
    assert 1.0 <= config['warning_duration'] <= 3.0
    assert 0.1 <= config['firing_duration'] <= 1.0
    assert config['laser_height'] >= 64  # At least 2 frog heights
    assert 0.05 <= config['spawn_chance'] <= 0.3  # Reasonable spawn rate
    
    print("✓ Laser configuration test passed!")

if __name__ == "__main__":
    print("=== Laser System Test Suite ===")
    
    try:
        test_laser_basic_functionality()
        test_laser_collision()
        test_laser_visual_properties()
        test_laser_configuration()
        
        print("\n🎉 All laser system tests passed!")
        print("\nLaser system is ready for high-altitude gameplay!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)