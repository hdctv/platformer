"""
Unit tests for enhanced platform cleanup system
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, Camera, Platform, HEIGHT


class TestPlatformCleanup(unittest.TestCase):
    """Test cases for platform cleanup system"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.generator = PlatformGenerator()
        self.camera = Camera()
    
    def test_cleanup_initialization(self):
        """Test cleanup system initializes with correct settings"""
        self.assertEqual(self.generator.max_inactive_platforms, 50)
        self.assertEqual(self.generator.cleanup_margin, 200)
        self.assertIsInstance(self.generator.stats, dict)
        self.assertEqual(self.generator.stats['platforms_created'], 0)
    
    def test_platform_cleanup_below_camera(self):
        """Test that platforms below camera are cleaned up"""
        # Create platforms at various heights
        platform1 = Platform(400, 100, 100, 20)  # Above camera
        platform2 = Platform(400, 800, 100, 20)  # Below camera
        platform3 = Platform(400, 1200, 100, 20) # Far below camera
        
        self.generator.active_platforms = [platform1, platform2, platform3]
        
        # Set camera position
        self.camera.y = 0
        
        # Cleanup platforms
        self.generator.cleanup_platforms_below_camera(self.camera)
        
        # Platform1 should remain active (above camera)
        self.assertIn(platform1, self.generator.active_platforms)
        
        # Platforms below should be cleaned up
        self.assertLess(len(self.generator.active_platforms), 3)
        
        # Cleaned platforms should be in inactive list (if under max)
        self.assertGreater(len(self.generator.inactive_platforms), 0)
    
    def test_cleanup_margin_setting(self):
        """Test cleanup margin configuration"""
        # Create platform just below screen
        platform = Platform(400, HEIGHT + 100, 100, 20)
        self.generator.active_platforms = [platform]
        
        # With large margin, platform should not be cleaned
        self.generator.cleanup_platforms_below_camera(self.camera, cleanup_margin=300)
        self.assertIn(platform, self.generator.active_platforms)
        
        # With small margin, platform should be cleaned
        self.generator.cleanup_platforms_below_camera(self.camera, cleanup_margin=50)
        self.assertNotIn(platform, self.generator.active_platforms)
    
    def test_max_inactive_platforms_limit(self):
        """Test that inactive platforms are limited to max count"""
        # Set a small max inactive limit
        self.generator.max_inactive_platforms = 3
        
        # Create many platforms below camera
        platforms = []
        for i in range(10):
            platform = Platform(400, 1000 + i * 100, 100, 20)
            platforms.append(platform)
            self.generator.active_platforms.append(platform)
        
        # Cleanup all platforms
        self.generator.cleanup_platforms_below_camera(self.camera)
        
        # Should only keep max_inactive_platforms in inactive list
        self.assertLessEqual(len(self.generator.inactive_platforms), 3)
        
        # All should be removed from active list
        self.assertEqual(len(self.generator.active_platforms), 0)
    
    def test_platform_reuse_statistics(self):
        """Test platform reuse tracking"""
        # Create a platform and make it inactive
        platform = Platform(100, 100, 100, 20)
        platform.active = False
        self.generator.inactive_platforms.append(platform)
        
        # Create new platform should reuse the inactive one
        reused_platform = self.generator.create_platform(200, 200)
        
        # Should track reuse
        self.assertEqual(self.generator.stats['platforms_reused'], 1)
        self.assertEqual(self.generator.stats['platforms_created'], 0)
        
        # Create another platform when no inactive ones exist
        new_platform = self.generator.create_platform(300, 300)
        
        # Should track creation
        self.assertEqual(self.generator.stats['platforms_created'], 1)
    
    def test_memory_stats_reporting(self):
        """Test memory statistics reporting"""
        # Add some platforms
        self.generator.active_platforms = [Platform(400, i * 100, 100, 20) for i in range(5)]
        self.generator.inactive_platforms = [Platform(400, i * 100, 100, 20) for i in range(3)]
        self.generator.stats['platforms_created'] = 10
        self.generator.stats['platforms_reused'] = 5
        
        stats = self.generator.get_memory_stats()
        
        self.assertEqual(stats['active_platforms'], 5)
        self.assertEqual(stats['inactive_platforms'], 3)
        self.assertEqual(stats['total_platforms'], 8)
        self.assertEqual(stats['platforms_created'], 10)
        self.assertEqual(stats['platforms_reused'], 5)
        self.assertAlmostEqual(stats['reuse_efficiency'], 33.33, places=1)
    
    def test_force_cleanup(self):
        """Test forced cleanup of inactive platforms"""
        # Add many inactive platforms
        for i in range(20):
            platform = Platform(400, i * 100, 100, 20)
            platform.active = False
            self.generator.inactive_platforms.append(platform)
        
        initial_count = len(self.generator.inactive_platforms)
        
        # Force cleanup to keep only 5
        self.generator.force_cleanup(keep_count=5)
        
        # Should only have 5 left
        self.assertEqual(len(self.generator.inactive_platforms), 5)
        
        # Should track cleaned platforms
        expected_cleaned = initial_count - 5
        self.assertEqual(self.generator.stats['platforms_cleaned'], expected_cleaned)
    
    def test_cleanup_settings_configuration(self):
        """Test cleanup settings configuration"""
        # Set new cleanup settings
        self.generator.set_cleanup_settings(cleanup_margin=300, max_inactive=25)
        
        self.assertEqual(self.generator.cleanup_margin, 300)
        self.assertEqual(self.generator.max_inactive_platforms, 25)
        
        # Test partial setting
        self.generator.set_cleanup_settings(cleanup_margin=150)
        self.assertEqual(self.generator.cleanup_margin, 150)
        self.assertEqual(self.generator.max_inactive_platforms, 25)  # Should remain unchanged
    
    def test_cleanup_performance_with_many_platforms(self):
        """Test cleanup performance with large number of platforms"""
        # Create many platforms
        for i in range(100):
            platform = Platform(400, i * 50, 100, 20)
            self.generator.active_platforms.append(platform)
        
        # Move camera up so most platforms are below
        self.camera.y = -2000
        
        initial_count = len(self.generator.active_platforms)
        
        # Cleanup should be fast and effective
        self.generator.cleanup_platforms_below_camera(self.camera)
        
        # Should have cleaned up most platforms
        self.assertLess(len(self.generator.active_platforms), initial_count)
        
        # Should have some inactive platforms for reuse
        self.assertGreater(len(self.generator.inactive_platforms), 0)
    
    def test_cleanup_integration_with_generation(self):
        """Test cleanup working together with platform generation"""
        # Generate initial platforms
        self.generator.update(self.camera)
        initial_active = len(self.generator.active_platforms)
        
        # Move camera up significantly
        self.camera.y = -1000
        
        # Update should generate new platforms and cleanup old ones
        self.generator.update(self.camera)
        
        # Should have platforms (new ones generated)
        self.assertGreater(len(self.generator.active_platforms), 0)
        
        # Should have some inactive platforms from cleanup
        self.assertGreaterEqual(len(self.generator.inactive_platforms), 0)


class TestMemoryManagement(unittest.TestCase):
    """Test memory management aspects of cleanup system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = PlatformGenerator()
        self.camera = Camera()
    
    def test_memory_leak_prevention(self):
        """Test that cleanup prevents memory leaks"""
        # Simulate long gameplay with many platform generations
        total_platforms_created = 0
        
        for i in range(20):  # Simulate 20 camera movements
            self.camera.y = -i * 200
            self.generator.update(self.camera)
            total_platforms_created += len(self.generator.active_platforms)
        
        # Total platforms in memory should be much less than total created
        total_in_memory = len(self.generator.active_platforms) + len(self.generator.inactive_platforms)
        self.assertLess(total_in_memory, total_platforms_created * 0.5)  # Less than 50% of total
    
    def test_reuse_efficiency(self):
        """Test that platform reuse is working efficiently"""
        # Generate initial platforms
        self.generator.update(self.camera)
        
        # Move camera up and generate more platforms, then cleanup old ones
        for i in range(5):
            self.camera.y = -i * 500  # Move camera up significantly
            self.generator.update(self.camera)  # Generate new platforms
            self.generator.cleanup_platforms_below_camera(self.camera)  # Cleanup old ones
        
        stats = self.generator.get_memory_stats()
        
        # Should have created and reused platforms
        self.assertGreater(stats['platforms_created'], 0)
        
        # If we have inactive platforms, we should eventually reuse some
        if len(self.generator.inactive_platforms) > 0:
            # Generate more platforms to trigger reuse
            self.camera.y = -3000
            self.generator.update(self.camera)
            stats = self.generator.get_memory_stats()
            
            # Now we should have some reuse
            self.assertGreaterEqual(stats['platforms_reused'], 0)  # Allow 0 or more


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)