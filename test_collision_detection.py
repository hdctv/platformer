"""
Unit tests for collision detection in Frog Platformer
Tests frog-platform collision detection accuracy and edge cases
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Frog, Platform, PlatformType
from pygame import Rect


class TestCollisionDetection(unittest.TestCase):
    """Test cases for frog-platform collision detection"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a standard frog for testing
        self.frog = Frog(400, 300)
        
        # Create a standard platform for testing
        self.platform = Platform(400, 350, 100, 20)
    
    def test_frog_landing_on_platform_center(self):
        """Test frog landing on the center of a platform"""
        # Position frog above platform center, falling downward
        self.frog.x = 400
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return True
        self.assertTrue(self.platform.check_collision(self.frog))
    
    def test_frog_landing_on_platform_left_edge(self):
        """Test frog landing on the left edge of a platform"""
        # Position frog at left edge of platform
        self.frog.x = 350  # Left edge (platform center 400 - width/2 50 = 350)
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return True
        self.assertTrue(self.platform.check_collision(self.frog))
    
    def test_frog_landing_on_platform_right_edge(self):
        """Test frog landing on the right edge of a platform"""
        # Position frog at right edge of platform
        self.frog.x = 450  # Right edge (platform center 400 + width/2 50 = 450)
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return True
        self.assertTrue(self.platform.check_collision(self.frog))
    
    def test_frog_just_outside_platform_left(self):
        """Test frog just outside the left edge of platform (no collision)"""
        # Position frog just outside left edge
        # Platform left edge is at 350, frog width is 32, so frog center needs to be at 350 - 16 - 1 = 333
        self.frog.x = 333  # Just outside left edge (accounting for frog width)
        self.frog.y = 340  # At platform level
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return False
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_frog_just_outside_platform_right(self):
        """Test frog just outside the right edge of platform (no collision)"""
        # Position frog just outside right edge
        # Platform right edge is at 450, frog width is 32, so frog center needs to be at 450 + 16 + 1 = 467
        self.frog.x = 467  # Just outside right edge (accounting for frog width)
        self.frog.y = 340  # At platform level
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return False
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_frog_jumping_up_through_platform(self):
        """Test frog jumping up through platform (should not collide)"""
        # Position frog below platform, jumping upward
        self.frog.x = 400
        self.frog.y = 380  # Below platform
        self.frog.vy = -10  # Jumping upward (negative velocity)
        
        # Check collision should return False (can't land when jumping up)
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_frog_above_platform_not_falling(self):
        """Test frog above platform but not falling (zero velocity)"""
        # Position frog above platform with no vertical velocity
        self.frog.x = 400
        self.frog.y = 340
        self.frog.vy = 0   # No vertical movement
        
        # Check collision should return False
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_frog_far_above_platform(self):
        """Test frog far above platform (no collision)"""
        # Position frog well above platform
        self.frog.x = 400
        self.frog.y = 200  # Far above platform
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return False
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_frog_far_below_platform(self):
        """Test frog far below platform (no collision)"""
        # Position frog well below platform
        self.frog.x = 400
        self.frog.y = 500  # Far below platform
        self.frog.vy = 5   # Falling downward
        
        # Check collision should return False
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_inactive_platform_no_collision(self):
        """Test that inactive platforms don't cause collisions"""
        # Set platform to inactive (for breakable platforms)
        self.platform.active = False
        
        # Position frog to land on platform
        self.frog.x = 400
        self.frog.y = 340
        self.frog.vy = 5
        
        # Check collision should return False for inactive platform
        self.assertFalse(self.platform.check_collision(self.frog))
    
    def test_platform_on_collision_behavior(self):
        """Test platform's on_collision method behavior"""
        # Position frog falling onto platform
        self.frog.x = 400
        self.frog.y = 340
        self.frog.vy = 8   # Fast downward velocity
        self.frog.on_ground = False
        
        # Call on_collision
        self.platform.on_collision(self.frog)
        
        # Verify frog is positioned correctly on top of platform
        expected_y = self.platform.y - self.frog.height // 2
        self.assertEqual(self.frog.y, expected_y)
        
        # Verify frog's vertical velocity is stopped
        self.assertEqual(self.frog.vy, 0)
        
        # Verify frog is marked as on ground
        self.assertTrue(self.frog.on_ground)
    
    def test_frog_collision_with_multiple_platforms(self):
        """Test frog collision detection with multiple platforms"""
        # Create multiple platforms
        platform1 = Platform(300, 350, 100, 20)
        platform2 = Platform(500, 350, 100, 20)
        platforms = [platform1, platform2]
        
        # Position frog to land on first platform
        self.frog.x = 300
        self.frog.y = 340
        self.frog.vy = 5
        
        # Test collision with platform list
        self.frog.check_platform_collision(platforms)
        
        # Verify frog landed on the platform
        self.assertTrue(self.frog.on_ground)
        self.assertEqual(self.frog.vy, 0)
    
    def test_platform_rect_calculation(self):
        """Test platform rectangle calculation for collision detection"""
        platform = Platform(400, 300, 100, 20)
        rect = platform.get_rect()
        
        # Verify rectangle position and size
        self.assertEqual(rect.x, 350)  # center_x - width/2 = 400 - 50
        self.assertEqual(rect.y, 300)  # top of platform
        self.assertEqual(rect.width, 100)
        self.assertEqual(rect.height, 20)
    
    def test_frog_collision_precision_edge_case(self):
        """Test collision detection precision at exact boundaries"""
        # Test frog exactly at platform boundary
        self.frog.x = 350  # Exactly at left edge
        self.frog.y = 350  # Exactly at platform top
        self.frog.vy = 1   # Minimal downward velocity
        
        # Should still detect collision
        self.assertTrue(self.platform.check_collision(self.frog))
    
    def test_different_platform_sizes(self):
        """Test collision detection with different platform sizes"""
        # Test with narrow platform
        narrow_platform = Platform(400, 350, 50, 20)
        
        # Frog at edge of narrow platform
        self.frog.x = 425  # Right edge of narrow platform
        self.frog.y = 340
        self.frog.vy = 5
        
        self.assertTrue(narrow_platform.check_collision(self.frog))
        
        # Frog just outside narrow platform
        # Narrow platform right edge is at 425, frog width is 32, so frog center needs to be at 425 + 16 + 1 = 442
        self.frog.x = 442  # Just outside (accounting for frog width)
        self.assertFalse(narrow_platform.check_collision(self.frog))
        
        # Test with wide platform
        wide_platform = Platform(400, 350, 200, 20)
        
        # Frog at edge of wide platform
        self.frog.x = 500  # Right edge of wide platform
        self.frog.y = 340
        self.frog.vy = 5
        
        self.assertTrue(wide_platform.check_collision(self.frog))
    
    def test_frog_size_impact_on_collision(self):
        """Test how frog size affects collision detection"""
        # Create frog with different size
        large_frog = Frog(400, 340)
        large_frog.width = 64  # Larger than default
        large_frog.height = 64
        large_frog.vy = 5
        
        # Test collision with larger frog
        self.assertTrue(self.platform.check_collision(large_frog))
        
        # Position large frog where smaller frog wouldn't collide
        large_frog.x = 460  # Further from platform center
        # Large frog should still collide due to its size
        self.assertTrue(self.platform.check_collision(large_frog))


class TestCollisionEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions for collision detection"""
    
    def test_zero_size_platform(self):
        """Test collision with zero-size platform"""
        platform = Platform(400, 350, 0, 0)
        frog = Frog(400, 340)
        frog.vy = 5
        
        # Should not collide with zero-size platform
        self.assertFalse(platform.check_collision(frog))
    
    def test_negative_velocity_edge_case(self):
        """Test collision with very small negative velocity"""
        frog = Frog(400, 340)
        platform = Platform(400, 350, 100, 20)
        
        # Very small upward velocity (should not collide)
        frog.vy = -0.1
        self.assertFalse(platform.check_collision(frog))
        
        # Very small downward velocity (should collide)
        frog.vy = 0.1
        self.assertTrue(platform.check_collision(frog))
    
    def test_platform_at_screen_boundaries(self):
        """Test collision with platforms at screen boundaries"""
        # Platform at left edge of screen
        left_platform = Platform(50, 350, 100, 20)
        frog = Frog(50, 340)
        frog.vy = 5
        
        self.assertTrue(left_platform.check_collision(frog))
        
        # Platform at right edge of screen (assuming 800px width)
        right_platform = Platform(750, 350, 100, 20)
        frog.x = 750
        
        self.assertTrue(right_platform.check_collision(frog))
    
    def test_overlapping_platforms(self):
        """Test collision behavior with overlapping platforms"""
        platform1 = Platform(400, 350, 100, 20)
        platform2 = Platform(420, 350, 100, 20)  # Overlapping platform
        
        frog = Frog(410, 340)  # In overlap area
        frog.vy = 5
        
        # Both platforms should detect collision
        self.assertTrue(platform1.check_collision(frog))
        self.assertTrue(platform2.check_collision(frog))


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)