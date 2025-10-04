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
        self.assertEqual(camera.max_y, 0.0)
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
        # So frog needs to be at y < (HEIGHT - 180) = 420 to trigger camera movement
        # In Pygame coordinates, smaller Y = higher up
        self.frog.y = 100  # High position (small Y value)
        
        initial_camera_y = self.camera.y
        self.camera.update(self.frog)
        
        # Camera should move up to follow frog (camera.y should decrease)
        self.assertLess(self.camera.y, initial_camera_y)
    
    def test_camera_does_not_move_downward(self):
        """Test camera doesn't move down when frog falls (but still auto-scrolls)"""
        # Disable auto-scroll for this test to isolate frog-following behavior
        self.camera.enable_auto_scroll(False)
        
        # Move camera up first by positioning frog high
        self.frog.y = 100  # High position to trigger camera movement
        self.camera.update(self.frog)
        camera_y_after_up = self.camera.y
        
        # Move frog down (larger Y value)
        self.frog.y = 500
        self.camera.update(self.frog)
        
        # Camera should not move down (should stay at same position)
        self.assertEqual(self.camera.y, camera_y_after_up)
    
    def test_camera_respects_maximum_position(self):
        """Test camera doesn't go below starting position"""
        # Try to move camera below starting position
        self.camera.y = 10  # Below starting position
        self.frog.y = 600   # Frog at bottom
        self.camera.update(self.frog)
        
        # Camera should be at maximum position (starting position)
        self.assertLessEqual(self.camera.y, self.camera.max_y)
    
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
    
    def test_automatic_scrolling(self):
        """Test automatic upward scrolling functionality when enabled"""
        # Enable auto-scroll for this test
        self.camera.enable_auto_scroll(True)
        
        initial_y = self.camera.y
        
        # Update camera without frog (just automatic scrolling)
        self.camera.update(None)
        
        # Camera should have moved up by scroll_speed (y decreases)
        expected_y = initial_y - self.camera.scroll_speed
        self.assertEqual(self.camera.y, expected_y)
    
    def test_scroll_speed_control(self):
        """Test setting scroll speed"""
        new_speed = 2.5
        self.camera.set_scroll_speed(new_speed)
        self.assertEqual(self.camera.scroll_speed, new_speed)
        
        # Enable auto-scroll and test scrolling with new speed
        self.camera.enable_auto_scroll(True)
        initial_y = self.camera.y
        self.camera.update(None)
        expected_y = initial_y - new_speed  # Y decreases when scrolling up
        self.assertEqual(self.camera.y, expected_y)
    
    def test_auto_scroll_enable_disable(self):
        """Test enabling and disabling automatic scrolling"""
        initial_y = self.camera.y
        
        # Auto scroll should be disabled by default now
        self.assertFalse(self.camera.auto_scroll_enabled)
        
        # Update should not move camera when disabled
        self.camera.update(None)
        self.assertEqual(self.camera.y, initial_y)
        
        # Enable auto scroll
        self.camera.enable_auto_scroll(True)
        self.assertTrue(self.camera.auto_scroll_enabled)
        
        # Update should move camera up (y decreases)
        self.camera.update(None)
        self.assertLess(self.camera.y, initial_y)
        
        # Disable again
        self.camera.enable_auto_scroll(False)
        self.assertFalse(self.camera.auto_scroll_enabled)
    
    def test_scroll_distance_tracking(self):
        """Test tracking total scroll distance"""
        initial_distance = self.camera.get_scroll_distance()
        self.assertEqual(initial_distance, 0.0)  # Should start at 0
        
        # Scroll camera up (decrease Y)
        self.camera.y = -100
        distance = self.camera.get_scroll_distance()
        self.assertEqual(distance, 100.0)  # Positive distance = scrolled up
    
    def test_auto_scroll_with_frog_following(self):
        """Test automatic scrolling combined with frog following"""
        # Position frog high to trigger following
        self.frog.y = 100  # High position (small Y)
        initial_camera_y = self.camera.y
        
        # Update camera (should follow frog)
        self.camera.update(self.frog)
        
        # Camera should have moved up (camera.y should decrease)
        self.assertLess(self.camera.y, initial_camera_y)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)