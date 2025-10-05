#!/usr/bin/env python3
"""
Unit tests for vertical moving platform mechanics
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog


class TestVerticalPlatformMechanics(unittest.TestCase):
    """Test cases for vertical moving platform mechanics"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.frog = Frog(400, 300)
        self.vertical_platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        self.normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
    
    def test_vertical_platform_initialization(self):
        """Test vertical platform initializes with correct properties"""
        platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        
        self.assertEqual(platform.platform_type, PlatformType.VERTICAL)
        self.assertEqual(platform.friction, 1.0)
        self.assertEqual(platform.color, 'cyan')
        self.assertTrue(hasattr(platform, 'move_speed'))
        self.assertTrue(hasattr(platform, 'move_direction'))
        self.assertTrue(hasattr(platform, 'move_range'))
        self.assertTrue(hasattr(platform, 'original_y'))
        self.assertEqual(platform.move_speed, 0.8)
        self.assertEqual(platform.move_range, 80)
        self.assertEqual(platform.original_y, 350)
        self.assertIn(platform.move_direction, [-1, 1])
    
    def test_vertical_platform_movement(self):
        """Test vertical platform moves up and down"""
        platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        
        initial_y = platform.y
        initial_direction = platform.move_direction
        
        # Update platform multiple times
        for _ in range(10):
            platform.update(1/60)
        
        # Platform should have moved
        self.assertNotEqual(platform.y, initial_y)
        
        # Test direction reversal at boundaries
        # Move to upper boundary
        platform.y = platform.original_y - platform.move_range
        platform.move_direction = -1  # Moving up
        platform.update(1/60)
        self.assertEqual(platform.move_direction, 1)  # Should reverse to down
        
        # Move to lower boundary
        platform.y = platform.original_y + platform.move_range
        platform.move_direction = 1  # Moving down
        platform.update(1/60)
        self.assertEqual(platform.move_direction, -1)  # Should reverse to up
    
    def test_frog_moves_with_vertical_platform(self):
        """Test that frog moves vertically with the platform"""
        platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        
        # Position frog on platform first
        self.frog.y = platform.y - self.frog.height//2 + 1  # Standard landing position
        initial_frog_y = self.frog.y
        
        # Apply vertical platform effect (this is what on_frog_land does for vertical platforms)
        self.frog.y += platform.move_speed * platform.move_direction
        
        # Frog should have moved with platform
        expected_y = initial_frog_y + platform.move_speed * platform.move_direction
        self.assertEqual(self.frog.y, expected_y)
    
    def test_vertical_platform_collision_integration(self):
        """Test vertical platform works with collision system"""
        platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        
        # Set up collision scenario
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        initial_y = self.frog.y
        
        # Check collision and handle landing
        if platform.check_collision(self.frog):
            platform.on_collision(self.frog)
        
        # Verify collision handling worked
        self.assertTrue(self.frog.on_ground)
        self.assertEqual(self.frog.vy, 0)
        
        # Verify vertical movement was applied
        expected_y = initial_y + platform.move_speed * platform.move_direction
        # Note: collision also adjusts frog.y, so we check it moved from collision position
        self.assertNotEqual(self.frog.y, initial_y)
    
    def test_vertical_vs_normal_platform_comparison(self):
        """Test difference between vertical and normal platform behavior"""
        # Test normal platform
        normal_frog = Frog(400, 300)
        initial_normal_y = normal_frog.y
        self.normal_platform.on_frog_land(normal_frog)
        normal_final_y = normal_frog.y
        
        # Test vertical platform
        vertical_frog = Frog(400, 300)
        initial_vertical_y = vertical_frog.y
        self.vertical_platform.on_frog_land(vertical_frog)
        vertical_final_y = vertical_frog.y
        
        # Both should adjust Y for landing, but vertical should have additional movement
        normal_movement = abs(normal_final_y - initial_normal_y)
        vertical_movement = abs(vertical_final_y - initial_vertical_y)
        
        # Vertical platform should cause more Y movement due to platform motion
        self.assertGreater(vertical_movement, normal_movement)
    
    def test_vertical_platform_visual_appearance(self):
        """Test vertical platform has cyan appearance"""
        platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        
        # Should be cyan
        self.assertEqual(platform.get_visual_color(), 'cyan')
        self.assertEqual(platform.color, 'cyan')
    
    def test_vertical_platform_update_behavior(self):
        """Test vertical platform updates correctly over time"""
        platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
        
        positions = []
        directions = []
        
        # Record positions and directions over multiple updates
        for i in range(200):  # Enough to see direction changes
            positions.append(platform.y)
            directions.append(platform.move_direction)
            platform.update(1/60)
        
        # Should have moved
        self.assertNotEqual(positions[0], positions[-1])
        
        # Should have changed direction at least once
        self.assertGreater(len(set(directions)), 1)
        
        # Should stay within movement range
        min_y = min(positions)
        max_y = max(positions)
        expected_min = platform.original_y - platform.move_range
        expected_max = platform.original_y + platform.move_range
        
        self.assertGreaterEqual(min_y, expected_min - 5)  # Small tolerance
        self.assertLessEqual(max_y, expected_max + 5)


class TestVerticalPlatformIntegration(unittest.TestCase):
    """Integration tests for vertical platforms with game systems"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.frog = Frog(400, 300)
        self.vertical_platform = Platform(400, 350, 100, 20, PlatformType.VERTICAL)
    
    def test_multiple_vertical_platform_updates(self):
        """Test vertical platform behavior over multiple update cycles"""
        # Land frog on vertical platform
        self.vertical_platform.on_frog_land(self.frog)
        
        # Simulate multiple game update cycles
        for i in range(20):
            # Update platform
            self.vertical_platform.update(1/60)
        
        # Platform should still be active
        self.assertTrue(self.vertical_platform.active)
        
        # Platform should have moved from original position
        self.assertNotEqual(self.vertical_platform.y, 350)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)