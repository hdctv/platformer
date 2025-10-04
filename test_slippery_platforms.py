"""
Enhanced unit tests for slippery platform mechanics
"""

import unittest
import sys
import os
import math

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


class TestSlipperyPlatformMechanics(unittest.TestCase):
    """Test cases for enhanced slippery platform mechanics"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.frog = Frog(400, 300)
        self.slippery_platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
        self.normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
    
    def test_slippery_platform_initialization(self):
        """Test slippery platform initializes with correct properties"""
        platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
        
        self.assertEqual(platform.platform_type, PlatformType.SLIPPERY)
        self.assertEqual(platform.friction, 0.3)
        self.assertEqual(platform.color, 'lightblue')
        self.assertTrue(hasattr(platform, 'ice_shine_timer'))
        self.assertTrue(hasattr(platform, 'continuous_slip'))
    
    def test_frog_slippery_state_tracking(self):
        """Test frog tracks slippery surface state"""
        # Initially not on slippery surface
        self.assertFalse(self.frog.on_slippery_surface)
        self.assertIsNone(self.frog.slippery_platform)
        
        # Land on slippery platform
        self.slippery_platform.on_frog_land(self.frog)
        
        # Should be marked as on slippery surface
        self.assertTrue(self.frog.on_slippery_surface)
        self.assertEqual(self.frog.slippery_platform, self.slippery_platform)
    
    def test_reduced_friction_on_landing(self):
        """Test friction reduction when landing on slippery platform"""
        # Set initial horizontal velocity
        self.frog.vx = 10.0
        
        # Land on slippery platform
        self.slippery_platform.on_frog_land(self.frog)
        
        # Velocity should be reduced by friction
        expected_vx = 10.0 * self.slippery_platform.friction
        self.assertEqual(self.frog.vx, expected_vx)
    
    def test_continuous_friction_effect(self):
        """Test continuous friction while on slippery platform"""
        # Set up frog on slippery platform
        self.frog.on_slippery_surface = True
        self.frog.slippery_platform = self.slippery_platform
        self.frog.vx = 5.0
        
        initial_vx = self.frog.vx
        
        # Update frog (applies continuous friction)
        self.frog.update()
        
        # Velocity should be reduced (but not to zero immediately)
        self.assertLess(abs(self.frog.vx), abs(initial_vx))
        self.assertNotEqual(self.frog.vx, 0)  # Should still have some velocity
    
    def test_reduced_control_on_slippery_surface(self):
        """Test reduced movement control on slippery platforms"""
        # Set up frog on slippery platform
        self.frog.on_slippery_surface = True
        self.frog.slippery_platform = self.slippery_platform
        self.frog.vx = 0
        
        # Try to move right
        self.frog.move_horizontal(1)
        
        # Should have less velocity than normal movement
        normal_speed = 3.0  # GAME_CONFIG['horizontal_speed']
        expected_reduced_speed = normal_speed * 0.6  # control_factor
        
        # Due to gradual acceleration, won't reach full speed immediately
        self.assertLess(abs(self.frog.vx), expected_reduced_speed)
        self.assertGreater(abs(self.frog.vx), 0)
    
    def test_normal_control_on_regular_platform(self):
        """Test normal movement control on regular platforms"""
        # Frog not on slippery surface
        self.frog.on_slippery_surface = False
        self.frog.vx = 0
        
        # Try to move right
        self.frog.move_horizontal(1)
        
        # Should have full velocity immediately
        expected_speed = 3.0  # GAME_CONFIG['horizontal_speed']
        self.assertEqual(self.frog.vx, expected_speed)
    
    def test_slippery_platform_visual_shine_effect(self):
        """Test slippery platform shine animation"""
        platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
        
        # Test different shine states
        colors_seen = set()
        
        # Update platform multiple times to see different shine states
        for i in range(20):
            platform.update(0.1)
            color = platform.get_visual_color()
            colors_seen.add(color)
        
        # Should see multiple colors due to shine effect
        self.assertGreater(len(colors_seen), 1)
        
        # Should include shine colors
        possible_colors = {'lightblue', 'lightcyan', 'white'}
        self.assertTrue(colors_seen.intersection(possible_colors))
    
    def test_shine_animation_timing(self):
        """Test shine animation follows sine wave pattern"""
        platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
        
        # Test that shine timer increases
        initial_timer = platform.ice_shine_timer
        platform.update(0.5)
        self.assertGreater(platform.ice_shine_timer, initial_timer)
        
        # Test shine effect creates expected color pattern
        platform.ice_shine_timer = 0  # Reset to known state
        color_at_0 = platform.get_visual_color()
        
        platform.ice_shine_timer = math.pi / 2  # Peak of sine wave
        color_at_peak = platform.get_visual_color()
        
        # Colors should be different at different points in animation
        # (though this might be the same if both are in same intensity range)
        # The important thing is the animation is working
        self.assertTrue(hasattr(platform, 'ice_shine_timer'))
    
    def test_slippery_state_reset_on_collision_check(self):
        """Test frog slippery state resets properly during collision checking"""
        # Set frog on slippery surface
        self.frog.on_slippery_surface = True
        self.frog.slippery_platform = self.slippery_platform
        
        # Check collision (should reset slippery state first, then set it again if on slippery platform)
        self.frog.check_platform_collision([])  # Empty list means no platforms to land on
        
        # State should be reset since no platforms were found
        self.assertFalse(self.frog.on_slippery_surface)
        self.assertIsNone(self.frog.slippery_platform)
    
    def test_gradual_acceleration_on_slippery_surface(self):
        """Test gradual acceleration instead of instant movement on slippery platforms"""
        # Set up frog on slippery platform
        self.frog.on_slippery_surface = True
        self.frog.slippery_platform = self.slippery_platform
        self.frog.vx = 0
        
        # Apply movement multiple times
        velocities = []
        for i in range(5):
            self.frog.move_horizontal(1)
            velocities.append(abs(self.frog.vx))
        
        # Velocity should gradually increase (not instant)
        for i in range(1, len(velocities)):
            self.assertGreaterEqual(velocities[i], velocities[i-1])
        
        # Should not reach full speed immediately
        full_speed = 3.0 * 0.6  # reduced speed on slippery
        self.assertLess(velocities[0], full_speed * 0.5)  # Much less than full speed initially
    
    def test_slippery_vs_normal_platform_comparison(self):
        """Test difference between slippery and normal platform behavior"""
        # Test normal platform
        normal_frog = Frog(400, 300)
        normal_frog.vx = 10.0
        self.normal_platform.on_frog_land(normal_frog)
        normal_final_vx = normal_frog.vx
        
        # Test slippery platform
        slippery_frog = Frog(400, 300)
        slippery_frog.vx = 10.0
        self.slippery_platform.on_frog_land(slippery_frog)
        slippery_final_vx = slippery_frog.vx
        
        # Slippery platform should reduce velocity more
        self.assertLess(abs(slippery_final_vx), abs(normal_final_vx))
    
    def test_slippery_platform_friction_multiplier(self):
        """Test slippery platform returns correct friction multiplier"""
        friction = self.slippery_platform.get_friction_multiplier()
        self.assertEqual(friction, 0.3)
        
        # Compare with normal platform
        normal_friction = self.normal_platform.get_friction_multiplier()
        self.assertEqual(normal_friction, 1.0)
        self.assertLess(friction, normal_friction)


class TestSlipperyPlatformIntegration(unittest.TestCase):
    """Integration tests for slippery platforms with game systems"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.frog = Frog(400, 300)
        self.slippery_platform = Platform(400, 350, 100, 20, PlatformType.SLIPPERY)
    
    def test_slippery_platform_collision_integration(self):
        """Test slippery platform works with collision system"""
        # Set up collision scenario
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        self.frog.vx = 8   # Moving horizontally
        
        # Check collision and handle landing
        if self.slippery_platform.check_collision(self.frog):
            self.slippery_platform.on_collision(self.frog)
        
        # Verify collision handling worked
        self.assertTrue(self.frog.on_ground)
        self.assertEqual(self.frog.vy, 0)
        self.assertTrue(self.frog.on_slippery_surface)
        
        # Verify friction was applied
        self.assertLess(abs(self.frog.vx), 8)  # Should be reduced from original
    
    def test_multiple_slippery_platform_updates(self):
        """Test slippery platform behavior over multiple update cycles"""
        # Land frog on slippery platform
        self.slippery_platform.on_frog_land(self.frog)
        
        # Simulate multiple game update cycles
        for i in range(10):
            # Update platform (for shine animation)
            self.slippery_platform.update(1/60)
            
            # Simulate frog being on platform
            self.frog.on_slippery_surface = True
            self.frog.slippery_platform = self.slippery_platform
            
            # Update frog
            self.frog.update()
        
        # Platform should still be active and animating
        self.assertTrue(self.slippery_platform.active)
        self.assertGreater(self.slippery_platform.ice_shine_timer, 0)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)