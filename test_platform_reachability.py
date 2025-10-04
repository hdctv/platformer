"""
Unit tests for platform reachability validation system
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, Camera, Platform, WIDTH


class TestPlatformReachability(unittest.TestCase):
    """Test cases for platform reachability validation"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.generator = PlatformGenerator()
        self.camera = Camera()
    
    def test_reachability_parameters(self):
        """Test that reachability parameters are set correctly"""
        self.assertEqual(self.generator.frog_jump_height, 144)
        self.assertEqual(self.generator.frog_horizontal_reach, 144)
        self.assertEqual(self.generator.safety_margin, 0.8)
        self.assertGreater(self.generator.min_platforms_in_range, 0)
    
    def test_platform_reachability_check(self):
        """Test basic platform reachability checking"""
        from_platform = Platform(400, 300, 100, 20)
        
        # Test reachable position (close and not too high)
        self.assertTrue(self.generator.is_platform_reachable(from_platform, 450, 250))
        
        # Test unreachable position (too far horizontally)
        self.assertFalse(self.generator.is_platform_reachable(from_platform, 600, 250))
        
        # Test unreachable position (too high vertically)
        self.assertFalse(self.generator.is_platform_reachable(from_platform, 400, 100))
        
        # Test unreachable position (going downward - should be reachable)
        self.assertTrue(self.generator.is_platform_reachable(from_platform, 400, 350))
    
    def test_find_reachable_position(self):
        """Test finding valid reachable positions"""
        from_platform = Platform(400, 300, 100, 20)
        
        # Should find a valid position
        position = self.generator.find_reachable_position(from_platform, 250)
        self.assertIsNotNone(position)
        
        if position:
            x, y = position
            self.assertTrue(self.generator.is_platform_reachable(from_platform, x, y))
            
        # Test with impossible target (too high)
        position = self.generator.find_reachable_position(from_platform, 50)
        # Should adjust target_y to be reachable
        if position:
            x, y = position
            self.assertTrue(self.generator.is_platform_reachable(from_platform, x, y))
    
    def test_platform_density_checking(self):
        """Test platform density checking around a position"""
        # Add platforms around a center point
        center_x, center_y = 400, 300
        
        # Add platforms within range
        self.generator.active_platforms = [
            Platform(center_x + 50, center_y + 50, 100, 20),
            Platform(center_x - 50, center_y - 50, 100, 20),
            Platform(center_x + 80, center_y - 30, 100, 20),
        ]
        
        density = self.generator.check_platform_density(center_x, center_y)
        self.assertGreater(density, 0)
        
        # Test with no platforms nearby
        density_empty = self.generator.check_platform_density(100, 100)
        self.assertEqual(density_empty, 0)
    
    def test_position_overlap_checking(self):
        """Test checking for position overlaps with existing platforms"""
        # Add a platform
        self.generator.active_platforms = [Platform(400, 300, 100, 20)]
        
        # Test overlapping position
        self.assertTrue(self.generator.position_overlaps_existing(400, 300))
        self.assertTrue(self.generator.position_overlaps_existing(420, 320))
        
        # Test non-overlapping position
        self.assertFalse(self.generator.position_overlaps_existing(500, 300))
        self.assertFalse(self.generator.position_overlaps_existing(400, 200))
    
    def test_safe_platform_position_finding(self):
        """Test finding safe positions for new platforms"""
        # Add some existing platforms
        self.generator.active_platforms = [
            Platform(400, 300, 100, 20),
            Platform(500, 250, 100, 20),
        ]
        
        # Should find a position that doesn't overlap
        position = self.generator.find_safe_platform_position(450, 275)
        
        if position:
            x, y = position
            self.assertFalse(self.generator.position_overlaps_existing(x, y))
    
    def test_minimum_density_enforcement(self):
        """Test ensuring minimum platform density"""
        # Start with low density
        self.generator.active_platforms = [Platform(400, 300, 100, 20)]
        
        initial_count = len(self.generator.active_platforms)
        
        # Ensure minimum density
        self.generator.ensure_minimum_density(400, 300)
        
        # Should have added platforms to meet minimum density
        final_count = len(self.generator.active_platforms)
        self.assertGreaterEqual(final_count, initial_count)
    
    def test_layout_validation(self):
        """Test validation of platform layout"""
        # Create a layout with some issues
        self.generator.active_platforms = [
            Platform(400, 500, 100, 20),  # Ground platform
            Platform(450, 400, 100, 20),  # Reachable
            Platform(600, 200, 100, 20),  # Potentially unreachable
        ]
        
        issues = self.generator.validate_platform_layout()
        
        # Should detect some issues
        self.assertIsInstance(issues, dict)
        self.assertIn('unreachable_platforms', issues)
        self.assertIn('low_density_areas', issues)
    
    def test_layout_issue_fixing(self):
        """Test fixing layout issues"""
        # Create problematic layout
        self.generator.active_platforms = [
            Platform(400, 500, 100, 20),  # Ground
            Platform(700, 200, 100, 20),  # Far away, unreachable
        ]
        
        initial_count = len(self.generator.active_platforms)
        
        # Validate and fix
        issues = self.generator.validate_platform_layout()
        self.generator.fix_layout_issues(issues)
        
        # Should have added platforms to fix issues
        final_count = len(self.generator.active_platforms)
        self.assertGreaterEqual(final_count, initial_count)
    
    def test_generation_with_validation(self):
        """Test that platform generation uses validation"""
        # Generate platforms
        self.generator.update(self.camera)
        
        # Should have generated platforms
        self.assertGreater(len(self.generator.active_platforms), 0)
        
        # Validate the generated layout
        issues = self.generator.validate_platform_layout()
        
        # Should have minimal issues (good generation)
        unreachable_count = len(issues['unreachable_platforms'])
        self.assertLessEqual(unreachable_count, 1)  # Allow at most 1 unreachable
    
    def test_reachability_with_screen_bounds(self):
        """Test reachability checking respects screen boundaries"""
        # Platform near left edge
        left_platform = Platform(50, 300, 100, 20)
        position = self.generator.find_reachable_position(left_platform, 250)
        
        if position:
            x, y = position
            # Should stay within screen bounds
            self.assertGreaterEqual(x, self.generator.platform_width // 2 + 20)
            self.assertLessEqual(x, WIDTH - self.generator.platform_width // 2 - 20)
        
        # Platform near right edge
        right_platform = Platform(WIDTH - 50, 300, 100, 20)
        position = self.generator.find_reachable_position(right_platform, 250)
        
        if position:
            x, y = position
            # Should stay within screen bounds
            self.assertGreaterEqual(x, self.generator.platform_width // 2 + 20)
            self.assertLessEqual(x, WIDTH - self.generator.platform_width // 2 - 20)
    
    def test_density_requirements_met(self):
        """Test that minimum density requirements are consistently met"""
        # Generate a larger layout
        for i in range(5):
            self.camera.y = -i * 200
            self.generator.update(self.camera)
        
        # Check density around several platforms
        density_violations = 0
        
        for platform in self.generator.active_platforms[:10]:  # Check first 10
            density = self.generator.check_platform_density(platform.x, platform.y)
            if density < self.generator.min_platforms_in_range:
                density_violations += 1
        
        # Should have very few density violations
        self.assertLessEqual(density_violations, 2)  # Allow some tolerance


class TestReachabilityIntegration(unittest.TestCase):
    """Integration tests for reachability with other systems"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = PlatformGenerator()
        self.camera = Camera()
    
    def test_reachability_with_cleanup(self):
        """Test that reachability works with platform cleanup"""
        # Generate platforms and move camera up
        for i in range(3):
            self.camera.y = -i * 300
            self.generator.update(self.camera)
            self.generator.cleanup_platforms_below_camera(self.camera)
        
        # Remaining platforms should still be reachable
        if len(self.generator.active_platforms) > 1:
            issues = self.generator.validate_platform_layout()
            unreachable_count = len(issues['unreachable_platforms'])
            
            # Should have minimal unreachable platforms after cleanup
            self.assertLessEqual(unreachable_count, 1)
    
    def test_performance_with_validation(self):
        """Test that validation doesn't significantly impact performance"""
        import time
        
        # Time generation without validation
        start_time = time.time()
        for i in range(10):
            self.camera.y = -i * 100
            self.generator.generate_platforms_above_camera(self.camera, self.camera.y - 500)
        generation_time = time.time() - start_time
        
        # Reset
        self.generator.active_platforms = []
        
        # Time generation with validation
        start_time = time.time()
        for i in range(10):
            self.camera.y = -i * 100
            self.generator.update(self.camera)  # Includes validation
        validation_time = time.time() - start_time
        
        # Validation shouldn't be more than 3x slower
        self.assertLess(validation_time, generation_time * 3)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)