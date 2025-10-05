"""
Unit tests for platform types and behaviors
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, PlatformGenerator, Frog


class TestPlatformTypes(unittest.TestCase):
    """Test cases for different platform types and their behaviors"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.frog = Frog(400, 300)
    
    def test_normal_platform(self):
        """Test normal platform behavior"""
        platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
        
        self.assertEqual(platform.platform_type, PlatformType.NORMAL)
        self.assertEqual(platform.get_friction_multiplier(), 1.0)
        self.assertFalse(platform.is_harmful())
        self.assertFalse(platform.should_break())
        self.assertEqual(platform.get_visual_color(), 'brown')
    
    def test_conveyor_platform(self):
        """Test conveyor platform behavior"""
        platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
        
        self.assertEqual(platform.platform_type, PlatformType.CONVEYOR)
        self.assertEqual(platform.get_friction_multiplier(), 1.0)
        self.assertFalse(platform.is_harmful())
        self.assertEqual(platform.get_visual_color(), 'gray')
        
        # Test conveyor effect on frog
        self.frog.vx = 10.0
        platform.on_frog_land(self.frog)
        expected_vx = 10.0 + (platform.conveyor_speed * platform.conveyor_direction)
        self.assertEqual(self.frog.vx, expected_vx)
    
    def test_breakable_platform(self):
        """Test breakable platform behavior"""
        platform = Platform(400, 350, 100, 20, PlatformType.BREAKABLE)
        
        self.assertEqual(platform.platform_type, PlatformType.BREAKABLE)
        self.assertFalse(platform.stepped_on)
        self.assertFalse(platform.should_break())
        self.assertEqual(platform.get_visual_color(), 'orange')
        
        # Test stepping on breakable platform
        platform.on_frog_land(self.frog)
        self.assertTrue(platform.stepped_on)
        self.assertEqual(platform.break_timer, 0.0)
        
        # Test breaking after delay
        platform.update(1.5)  # More than break_delay (1.0)
        self.assertTrue(platform.should_break())
        self.assertFalse(platform.active)
    
    def test_moving_platform(self):
        """Test moving platform behavior"""
        platform = Platform(400, 350, 100, 20, PlatformType.MOVING)
        
        self.assertEqual(platform.platform_type, PlatformType.MOVING)
        self.assertEqual(platform.original_x, 400)
        self.assertEqual(platform.move_direction, 1)
        self.assertEqual(platform.get_visual_color(), 'purple')
        
        # Test movement
        initial_x = platform.x
        platform.update(1.0)
        self.assertNotEqual(platform.x, initial_x)
        
        # Test frog moving with platform
        initial_frog_x = self.frog.x
        platform.on_frog_land(self.frog)
        self.assertNotEqual(self.frog.x, initial_frog_x)
    
    def test_harmful_platform(self):
        """Test harmful platform behavior"""
        platform = Platform(400, 350, 100, 20, PlatformType.HARMFUL)
        
        self.assertEqual(platform.platform_type, PlatformType.HARMFUL)
        self.assertTrue(platform.is_harmful())
        self.assertEqual(platform.get_visual_color(), 'red')
    
    def test_platform_type_initialization(self):
        """Test that platform types initialize correctly"""
        # Test all platform types
        for platform_type in PlatformType:
            platform = Platform(400, 350, 100, 20, platform_type)
            self.assertEqual(platform.platform_type, platform_type)
            self.assertTrue(hasattr(platform, 'friction'))
            self.assertTrue(hasattr(platform, 'color'))
    
    def test_breakable_platform_visual_flash(self):
        """Test breakable platform visual flashing when about to break"""
        platform = Platform(400, 350, 100, 20, PlatformType.BREAKABLE)
        
        # Step on platform
        platform.on_frog_land(self.frog)
        
        # Test normal color initially
        self.assertEqual(platform.get_visual_color(), 'orange')
        
        # Test flashing when close to breaking
        platform.break_timer = 0.8  # Close to break_delay (1.0)
        color = platform.get_visual_color()
        # Should be either red or orange (flashing)
        self.assertIn(color, ['red', 'orange'])
    
    def test_moving_platform_direction_change(self):
        """Test moving platform changes direction at boundaries"""
        platform = Platform(400, 350, 100, 20, PlatformType.MOVING)
        
        # Move platform to right boundary
        platform.x = platform.original_x + platform.move_range
        platform.update(0.1)
        self.assertEqual(platform.move_direction, -1)  # Should reverse
        
        # Move platform to left boundary
        platform.x = platform.original_x - platform.move_range
        platform.update(0.1)
        self.assertEqual(platform.move_direction, 1)  # Should reverse again
    
    def test_platform_update_behavior(self):
        """Test that different platform types update correctly"""
        platforms = [
            Platform(400, 350, 100, 20, PlatformType.NORMAL),
            Platform(400, 350, 100, 20, PlatformType.CONVEYOR),
            Platform(400, 350, 100, 20, PlatformType.BREAKABLE),
            Platform(400, 350, 100, 20, PlatformType.MOVING),
            Platform(400, 350, 100, 20, PlatformType.HARMFUL),
        ]
        
        # All platforms should update without errors
        for platform in platforms:
            initial_active = platform.active
            platform.update(0.1)
            # Normal, conveyor, and harmful platforms should remain active
            if platform.platform_type in [PlatformType.NORMAL, PlatformType.CONVEYOR, PlatformType.HARMFUL]:
                self.assertEqual(platform.active, initial_active)


class TestPlatformGenerator(unittest.TestCase):
    """Test platform generator with different types"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = PlatformGenerator()
    
    def test_platform_type_selection(self):
        """Test platform type selection based on progress"""
        # Early game - should only have normal platforms
        platform_type = self.generator.select_platform_type(50)
        self.assertEqual(platform_type, PlatformType.NORMAL)
        
        # Mid game - should have access to more types
        platform_type = self.generator.select_platform_type(250)
        self.assertIn(platform_type, [PlatformType.NORMAL, PlatformType.CONVEYOR, PlatformType.BREAKABLE])
        
        # Late game - should have access to all types
        available_types = set()
        for _ in range(50):  # Generate many to test variety
            platform_type = self.generator.select_platform_type(500)
            available_types.add(platform_type)
        
        # Should have at least normal and some special types
        self.assertIn(PlatformType.NORMAL, available_types)
        self.assertGreater(len(available_types), 1)
    
    def test_platform_creation_with_types(self):
        """Test creating platforms with specific types"""
        for platform_type in PlatformType:
            platform = self.generator.create_platform(400, 350, platform_type)
            self.assertEqual(platform.platform_type, platform_type)
            self.assertTrue(platform.active)
    
    def test_type_introduction_heights(self):
        """Test that platform types are introduced at correct heights"""
        # Test that slippery platforms are available after height 100
        available_at_150 = []
        for _ in range(20):
            platform_type = self.generator.select_platform_type(150)
            available_at_150.append(platform_type)
        
        # Should include conveyor platforms
        self.assertIn(PlatformType.CONVEYOR, available_at_150)
        
        # Test that harmful platforms are only available after height 400
        available_at_300 = []
        for _ in range(20):
            platform_type = self.generator.select_platform_type(300)
            available_at_300.append(platform_type)
        
        # Should not include harmful platforms yet
        self.assertNotIn(PlatformType.HARMFUL, available_at_300)
    
    def test_special_platform_chance(self):
        """Test that special platforms appear with correct frequency"""
        # Generate many platforms and check distribution
        platform_types = []
        for _ in range(100):
            platform_type = self.generator.select_platform_type(500)  # High progress
            platform_types.append(platform_type)
        
        normal_count = platform_types.count(PlatformType.NORMAL)
        special_count = len(platform_types) - normal_count
        
        # Should have some special platforms (not all normal)
        self.assertGreater(special_count, 0)
        
        # Should still have majority normal platforms
        self.assertGreater(normal_count, special_count)
    
    def test_platform_reuse_with_types(self):
        """Test that platform reuse works with different types"""
        # Create and deactivate a platform
        platform1 = self.generator.create_platform(400, 350, PlatformType.CONVEYOR)
        platform1.active = False
        self.generator.inactive_platforms.append(platform1)
        
        # Create new platform of different type
        platform2 = self.generator.create_platform(500, 250, PlatformType.BREAKABLE)
        
        # Should reuse the same object but with new type
        self.assertIs(platform1, platform2)
        self.assertEqual(platform2.platform_type, PlatformType.BREAKABLE)
        self.assertEqual(platform2.x, 500)
        self.assertEqual(platform2.y, 250)


class TestPlatformInteractions(unittest.TestCase):
    """Test interactions between frog and different platform types"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.frog = Frog(400, 300)
    
    def test_frog_landing_on_different_types(self):
        """Test frog landing behavior on different platform types"""
        platforms = [
            Platform(400, 350, 100, 20, PlatformType.NORMAL),
            Platform(400, 350, 100, 20, PlatformType.CONVEYOR),
            Platform(400, 350, 100, 20, PlatformType.BREAKABLE),
            Platform(400, 350, 100, 20, PlatformType.MOVING),
            Platform(400, 350, 100, 20, PlatformType.HARMFUL),
        ]
        
        for platform in platforms:
            # Reset frog state
            self.frog.y = 300
            self.frog.vy = 5
            self.frog.on_ground = False
            
            # Test landing
            platform.on_frog_land(self.frog)
            
            # All platforms should stop frog's fall
            self.assertEqual(self.frog.vy, 0)
            self.assertTrue(self.frog.on_ground)
            self.assertEqual(self.frog.y, platform.y - self.frog.height//2 + 1)
    
    def test_conveyor_platform_movement_effect(self):
        """Test that conveyor platforms add sideways movement to frog"""
        platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
        
        # Set frog horizontal velocity
        self.frog.vx = 0.0
        
        # Land on conveyor platform
        platform.on_frog_land(self.frog)
        
        # Velocity should be changed by conveyor movement
        expected_vx = platform.conveyor_speed * platform.conveyor_direction
        self.assertEqual(self.frog.vx, expected_vx)
    
    def test_moving_platform_carries_frog(self):
        """Test that moving platforms carry the frog"""
        platform = Platform(400, 350, 100, 20, PlatformType.MOVING)
        
        initial_frog_x = self.frog.x
        
        # Land on moving platform
        platform.on_frog_land(self.frog)
        
        # Frog should move with platform
        expected_x = initial_frog_x + platform.move_speed * platform.move_direction
        self.assertEqual(self.frog.x, expected_x)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)