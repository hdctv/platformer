"""
Unit tests for camera system coordinate conversion
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Camera, Frog, Platform


class TestCameraSystem(unittest.TestCase):
    """Test cases for camera system functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.camera = Camera()
        self.frog = Frog(400, 300)
    
    def test_camera_initialization(self):
        """Test camera initializes with correct default values"""
        camera = Camera()
        self.assertEqual(camera.y, 0.0)
        self.assertEqual(camera.min_y, 0.0)
        self.assertGreater(camera.follow_offset, 0)
    
    def test_world_to_screen_coordinate_conversion(self):
        """Test conversion from world coordinates to screen coordinates"""
        # Camera at position 0
        self.camera.y = 0
        self.assertEqual(self.camera.world_to_screen_y(100), 100)
        self.assertEqual(self.camera.world_to_screen_y(0), 0)
        
        # Camera moved up by 50 units
        self.camera.y = 50
        self.assertEqual(self.camera.world_to_screen_y(100), 50)  # 100 - 50
        self.assertEqual(self.camera.world_to_screen_y(50), 0)    # 50 - 50
    
    def test_screen_to_world_coordinate_conversion(self):
        """Test conversion from screen coordinates to world coordinates"""
        # Camera at position 0
        self.camera.y = 0
        self.assertEqual(self.camera.screen_to_world_y(100), 100)
        self.assertEqual(self.camera.screen_to_world_y(0), 0)
        
        # Camera moved up by 50 units
        self.camera.y = 50
        self.assertEqual(self.camera.screen_to_world_y(100), 150)  # 100 + 50
        self.assertEqual(self.camera.screen_to_world_y(0), 50)     # 0 + 50
    
    def test_coordinate_conversion_roundtrip(self):
        """Test that coordinate conversions are reversible"""
        self.camera.y = 123.45
        world_y = 456.78
        
        # Convert world to screen and back
        screen_y = self.camera.world_to_screen_y(world_y)
        converted_back = self.camera.screen_to_world_y(screen_y)
        
        self.assertAlmostEqual(world_y, converted_back, places=5)
    
    def test_camera_follows_frog_upward(self):
        """Test camera follows frog when frog moves upward"""
        # Position frog high enough to trigger camera movement
        # Camera follow_offset is HEIGHT * 0.3 = 600 * 0.3 = 180
        # So frog needs to be at y > (HEIGHT - 180) = 420 to trigger camera movement
        self.frog.y = 500  # High enough position to trigger camera movement
        
        initial_camera_y = self.camera.y
        self.camera.update(self.frog)
        
        # Camera should move up to follow frog
        self.assertGreater(self.camera.y, initial_camera_y)
    
    def test_camera_does_not_move_downward(self):
        """Test camera doesn't move down when frog falls"""
        # Move camera up first
        self.frog.y = 100
        self.camera.update(self.frog)
        camera_y_after_up = self.camera.y
        
        # Move frog down
        self.frog.y = 50
        self.camera.update(self.frog)
        
        # Camera should not move down
        self.assertEqual(self.camera.y, camera_y_after_up)
    
    def test_camera_respects_minimum_position(self):
        """Test camera doesn't go below minimum position"""
        # Try to move camera below minimum
        self.camera.y = -10
        self.frog.y = 0
        self.camera.update(self.frog)
        
        # Camera should be at minimum position
        self.assertGreaterEqual(self.camera.y, self.camera.min_y)
    
    def test_visibility_check(self):
        """Test camera visibility checking"""
        # Camera at position 0, screen height is 600
        self.camera.y = 0
        
        # Object at screen position 300 should be visible
        self.assertTrue(self.camera.is_visible(300))
        
        # Object at screen position -100 should not be visible
        self.assertFalse(self.camera.is_visible(-100))
        
        # Object at screen position 700 should not be visible (beyond screen height)
        self.assertFalse(self.camera.is_visible(700))
    
    def test_visibility_with_object_height(self):
        """Test visibility checking with object height consideration"""
        self.camera.y = 0
        
        # Object just outside screen but with height should be visible
        self.assertTrue(self.camera.is_visible(-10, object_height=20))
        self.assertTrue(self.camera.is_visible(610, object_height=20))
    
    def test_get_visible_bounds(self):
        """Test getting visible world coordinate bounds"""
        self.camera.y = 100
        
        top_y, bottom_y = self.camera.get_visible_bounds()
        
        # Top should be camera position
        self.assertEqual(top_y, 100)
        # Bottom should be camera position + screen height (600)
        self.assertEqual(bottom_y, 700)
    
    def test_platform_screen_rect_conversion(self):
        """Test platform screen rectangle conversion"""
        platform = Platform(400, 300, 100, 20)
        self.camera.y = 50
        
        screen_rect = platform.get_screen_rect(self.camera)
        
        # X coordinates should remain the same
        self.assertEqual(screen_rect.x, 350)  # 400 - 100/2
        self.assertEqual(screen_rect.width, 100)
        self.assertEqual(screen_rect.height, 20)
        
        # Y coordinate should be converted to screen space
        expected_screen_y = self.camera.world_to_screen_y(300)
        self.assertEqual(screen_rect.y, expected_screen_y)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)