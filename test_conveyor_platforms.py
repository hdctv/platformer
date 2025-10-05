"""
Unit tests for conveyor platform mechanics
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


class TestConveyorPlatformMechanics(unittest.TestCase):
    """Test cases for conveyor platform mechanics"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.frog = Frog(400, 300)
        self.conveyor_platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
        self.normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
    
    def test_conveyor_platform_initialization(self):
        """Test conveyor platform initializes with correct properties"""
        platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
        
        self.assertEqual(platform.platform_type, PlatformType.CONVEYOR)
        self.assertEqual(platform.friction, 1.0)  # Normal friction
        self.assertEqual(platform.color, 'gray')
        self.assertTrue(hasattr(platform, 'conveyor_speed'))
        self.assertTrue(hasattr(platform, 'conveyor_direction'))
        self.assertEqual(platform.conveyor_speed, 3.5)
        self.assertIn(platform.conveyor_direction, [-1, 1])  # Should be either left or right
    
    def test_frog_conveyor_state_tracking(self):
        """Test frog tracks conveyor state"""
        # Initially not on conveyor
        self.assertFalse(self.frog.on_conveyor)
        self.assertIsNone(self.frog.conveyor_platform)
        
        # Land on conveyor platform
        self.conveyor_platform.on_frog_land(self.frog)
        
        # Should be marked as on conveyor
        self.assertTrue(self.frog.on_conveyor)
        self.assertEqual(self.frog.conveyor_platform, self.conveyor_platform)
    
    def test_conveyor_movement_on_landing(self):
        """Test conveyor applies sideways movement when landing"""
        # Set initial horizontal velocity
        self.frog.vx = 0.0
        
        # Land on conveyor platform
        self.conveyor_platform.on_frog_land(self.frog)
        
        # Velocity should be changed by conveyor
        expected_vx = self.conveyor_platform.conveyor_speed * self.conveyor_platform.conveyor_direction
        self.assertEqual(self.frog.vx, expected_vx)
    
    def test_continuous_conveyor_effect(self):
        """Test continuous conveyor movement while on platform"""
        # Set up frog on conveyor platform
        self.frog.on_conveyor = True
        self.frog.conveyor_platform = self.conveyor_platform
        self.frog.vx = 0.0
        
        initial_vx = self.frog.vx
        
        # Update frog (applies continuous conveyor movement)
        self.frog.update()
        
        # Velocity should be increased by conveyor effect
        expected_increase = self.conveyor_platform.conveyor_speed * self.conveyor_platform.conveyor_direction * 0.5
        self.assertEqual(self.frog.vx, initial_vx + expected_increase)
    
    def test_normal_control_on_conveyor(self):
        """Test normal movement control on conveyor platforms"""
        # Frog on conveyor (but controls should work normally)
        self.frog.on_conveyor = True
        self.frog.conveyor_platform = self.conveyor_platform
        self.frog.vx = 0
        
        # Try to move right
        self.frog.move_horizontal(1)
        
        # Should have full velocity immediately (no reduced control)
        expected_speed = 3.0  # GAME_CONFIG['horizontal_speed']
        self.assertEqual(self.frog.vx, expected_speed)
    
    def test_conveyor_platform_visual_appearance(self):
        """Test conveyor platform has gray appearance"""
        platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
        
        # Should be gray
        self.assertEqual(platform.get_visual_color(), 'gray')
        self.assertEqual(platform.color, 'gray')
    
    def test_conveyor_vs_normal_platform_comparison(self):
        """Test difference between conveyor and normal platform behavior"""
        # Test normal platform
        normal_frog = Frog(400, 300)
        normal_frog.vx = 0.0
        self.normal_platform.on_frog_land(normal_frog)
        normal_final_vx = normal_frog.vx
        
        # Test conveyor platform
        conveyor_frog = Frog(400, 300)
        conveyor_frog.vx = 0.0
        self.conveyor_platform.on_frog_land(conveyor_frog)
        conveyor_final_vx = conveyor_frog.vx
        
        # Conveyor platform should add velocity
        self.assertEqual(normal_final_vx, 0.0)
        self.assertNotEqual(conveyor_final_vx, 0.0)
    
    def test_conveyor_direction_alternation(self):
        """Test that conveyor platforms alternate direction based on position"""
        # Create platforms at different positions
        platform1 = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)  # x=400, even
        platform2 = Platform(401, 350, 100, 20, PlatformType.CONVEYOR)  # x=401, odd
        
        # Should have different directions
        self.assertNotEqual(platform1.conveyor_direction, platform2.conveyor_direction)


class TestConveyorPlatformIntegration(unittest.TestCase):
    """Integration tests for conveyor platforms with game systems"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.frog = Frog(400, 300)
        self.conveyor_platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    
    def test_conveyor_platform_collision_integration(self):
        """Test conveyor platform works with collision system"""
        # Set up collision scenario
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        self.frog.vx = 0   # No horizontal movement initially
        
        # Check collision and handle landing
        if self.conveyor_platform.check_collision(self.frog):
            self.conveyor_platform.on_collision(self.frog)
        
        # Verify collision handling worked
        self.assertTrue(self.frog.on_ground)
        self.assertEqual(self.frog.vy, 0)
        self.assertTrue(self.frog.on_conveyor)
        
        # Verify conveyor movement was applied
        expected_vx = self.conveyor_platform.conveyor_speed * self.conveyor_platform.conveyor_direction
        self.assertEqual(self.frog.vx, expected_vx)
    
    def test_conveyor_state_reset_on_collision_check(self):
        """Test conveyor state resets properly during collision checking"""
        # Set frog on conveyor
        self.frog.on_conveyor = True
        self.frog.conveyor_platform = self.conveyor_platform
        
        # Check collision (should reset conveyor state first, then set it again if on conveyor platform)
        self.frog.check_platform_collision([])  # Empty list means no platforms to land on
        
        # State should be reset since no platforms were found
        self.assertFalse(self.frog.on_conveyor)
        self.assertIsNone(self.frog.conveyor_platform)
    
    def test_multiple_conveyor_platform_updates(self):
        """Test conveyor platform behavior over multiple update cycles"""
        # Land frog on conveyor platform
        self.conveyor_platform.on_frog_land(self.frog)
        
        # Simulate multiple game update cycles
        for i in range(10):
            # Update platform
            self.conveyor_platform.update(1/60)
            
            # Simulate frog being on platform
            self.frog.on_conveyor = True
            self.frog.conveyor_platform = self.conveyor_platform
            
            # Update frog
            self.frog.update()
        
        # Platform should still be active
        self.assertTrue(self.conveyor_platform.active)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)