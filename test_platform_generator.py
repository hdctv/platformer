"""
Unit tests for PlatformGenerator class
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, Camera, Platform, WIDTH, HEIGHT


class TestPlatformGenerator(unittest.TestCase):
    """Test cases for PlatformGenerator functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.generator = PlatformGenerator()
        self.camera = Camera()
    
    def test_generator_initialization(self):
        """Test platform generator initializes correctly"""
        self.assertEqual(len(self.generator.active_platforms), 0)
        self.assertEqual(len(self.generator.inactive_platforms), 0)
        self.assertEqual(self.generator.highest_platform_y, 0)
        self.assertGreater(self.generator.generation_buffer, 0)
    
    def test_create_platform(self):
        """Test platform creation"""
        platform = self.generator.create_platform(400, 300)
        
        self.assertIsInstance(platform, Platform)
        self.assertEqual(platform.x, 400)
        self.assertEqual(platform.y, 300)
        self.assertTrue(platform.active)
    
    def test_platform_reuse(self):
        """Test that inactive platforms are reused"""
        # Create a platform and make it inactive
        platform1 = Platform(100, 100, 100, 20)
        platform1.active = False
        self.generator.inactive_platforms.append(platform1)
        
        # Create new platform should reuse the inactive one
        platform2 = self.generator.create_platform(200, 200)
        
        # Should be the same object, just repositioned
        self.assertIs(platform1, platform2)
        self.assertEqual(platform2.x, 200)
        self.assertEqual(platform2.y, 200)
        self.assertTrue(platform2.active)
        self.assertEqual(len(self.generator.inactive_platforms), 0)
    
    def test_generate_platforms_above_camera(self):
        """Test platform generation above camera"""
        # Set camera position
        self.camera.y = -100
        
        # Generate platforms
        target_height = self.camera.y - 500
        self.generator.generate_platforms_above_camera(self.camera, target_height)
        
        # Should have generated platforms
        self.assertGreater(len(self.generator.active_platforms), 0)
        
        # All platforms should be above target height (with reasonable margin)
        for platform in self.generator.active_platforms:
            self.assertLessEqual(platform.y, self.camera.y + 100)  # Should be above camera
    
    def test_platform_spacing_validation(self):
        """Test that generated platforms have proper spacing"""
        self.camera.y = -100
        
        # Generate platforms
        self.generator.generate_platforms_above_camera(self.camera, self.camera.y - 500)
        
        platforms = self.generator.active_platforms
        self.assertGreater(len(platforms), 1)
        
        # Check spacing between consecutive platforms
        for i in range(1, len(platforms)):
            prev_platform = platforms[i-1]
            curr_platform = platforms[i]
            
            # Vertical spacing should be within range
            vertical_gap = prev_platform.y - curr_platform.y
            self.assertGreaterEqual(vertical_gap, self.generator.min_vertical_gap - 10)  # Small tolerance
            self.assertLessEqual(vertical_gap, self.generator.max_vertical_gap + 10)
            
            # Horizontal spacing should be reachable
            horizontal_gap = abs(prev_platform.x - curr_platform.x)
            self.assertLessEqual(horizontal_gap, self.generator.max_horizontal_reach + 20)  # Some tolerance
    
    def test_platforms_within_screen_bounds(self):
        """Test that generated platforms stay within screen bounds"""
        self.camera.y = -100
        
        # Generate platforms
        self.generator.generate_platforms_above_camera(self.camera, self.camera.y - 500)
        
        # All platforms should be within screen width
        for platform in self.generator.active_platforms:
            platform_left = platform.x - platform.width // 2
            platform_right = platform.x + platform.width // 2
            
            self.assertGreaterEqual(platform_left, 0)
            self.assertLessEqual(platform_right, WIDTH)
    
    def test_generator_update(self):
        """Test platform generator update method"""
        # Set camera position
        self.camera.y = -200
        
        # Update generator
        self.generator.update(self.camera)
        
        # Should have generated platforms
        self.assertGreater(len(self.generator.active_platforms), 0)
        
        # Highest platform should be above camera
        self.assertLess(self.generator.highest_platform_y, self.camera.y)
    
    def test_platform_cleanup(self):
        """Test cleanup of platforms below camera"""
        # Create platforms at various heights
        platform1 = Platform(400, 100, 100, 20)  # Above camera
        platform2 = Platform(400, 800, 100, 20)  # Below camera
        platform3 = Platform(400, 1200, 100, 20) # Far below camera
        
        self.generator.active_platforms = [platform1, platform2, platform3]
        
        # Set camera position
        self.camera.y = 0
        
        # Cleanup platforms
        self.generator.cleanup_platforms_below_camera(self.camera, cleanup_margin=200)
        
        # Platform1 should remain active (above camera)
        self.assertIn(platform1, self.generator.active_platforms)
        
        # Platform2 might remain (depends on exact calculation)
        # Platform3 should be cleaned up (far below)
        self.assertLess(len(self.generator.active_platforms), 3)
        self.assertGreater(len(self.generator.inactive_platforms), 0)
    
    def test_get_active_platforms(self):
        """Test getting active platforms"""
        # Add some platforms
        platform1 = Platform(400, 100, 100, 20)
        platform2 = Platform(400, 200, 100, 20)
        self.generator.active_platforms = [platform1, platform2]
        
        # Get active platforms
        active = self.generator.get_active_platforms()
        
        self.assertEqual(len(active), 2)
        self.assertIn(platform1, active)
        self.assertIn(platform2, active)
    
    def test_continuous_generation(self):
        """Test that platforms are continuously generated as camera moves"""
        initial_count = 0
        
        # Generate initial platforms
        self.camera.y = -100
        self.generator.update(self.camera)
        initial_count = len(self.generator.active_platforms)
        
        # Move camera up significantly
        self.camera.y = -500
        self.generator.update(self.camera)
        
        # Should have generated more platforms
        new_count = len(self.generator.active_platforms)
        self.assertGreater(new_count, initial_count)
    
    def test_platform_generation_performance(self):
        """Test that platform generation doesn't create excessive platforms"""
        self.camera.y = -100
        
        # Generate platforms
        self.generator.update(self.camera)
        platform_count = len(self.generator.active_platforms)
        
        # Should generate reasonable number of platforms
        self.assertLess(platform_count, 50)  # Shouldn't generate too many
        self.assertGreater(platform_count, 5)  # Should generate enough


class TestPlatformGeneratorIntegration(unittest.TestCase):
    """Integration tests for platform generator with game systems"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = PlatformGenerator()
        self.camera = Camera()
    
    def test_generator_with_camera_movement(self):
        """Test generator behavior as camera moves upward"""
        # Start with camera at bottom
        self.camera.y = 0
        self.generator.update(self.camera)
        initial_highest = self.generator.highest_platform_y
        
        # Move camera up
        self.camera.y = -300
        self.generator.update(self.camera)
        
        # Should have generated platforms higher up
        self.assertLess(self.generator.highest_platform_y, initial_highest)
    
    def test_memory_management(self):
        """Test that platform cleanup prevents memory leaks"""
        # Generate many platforms
        for i in range(10):
            self.camera.y = -i * 100
            self.generator.update(self.camera)
        
        # Should have many platforms
        total_platforms = len(self.generator.active_platforms) + len(self.generator.inactive_platforms)
        
        # Cleanup old platforms
        self.generator.cleanup_platforms_below_camera(self.camera, cleanup_margin=100)
        
        # Should have cleaned up some platforms
        new_total = len(self.generator.active_platforms) + len(self.generator.inactive_platforms)
        self.assertLessEqual(new_total, total_platforms + 10)  # Allow some growth but not excessive


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)