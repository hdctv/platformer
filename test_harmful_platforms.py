"""
Unit tests for harmful platform mechanics
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Platform, PlatformType, Frog, GameState
import frog_platformer


class TestHarmfulPlatformMechanics(unittest.TestCase):
    """Test cases for harmful platform mechanics"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.frog = Frog(400, 300)
        self.harmful_platform = Platform(400, 350, 100, 20, PlatformType.HARMFUL)
        self.normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
    
    def test_harmful_platform_initialization(self):
        """Test harmful platform initializes with correct properties"""
        platform = Platform(400, 350, 100, 20, PlatformType.HARMFUL)
        
        self.assertEqual(platform.platform_type, PlatformType.HARMFUL)
        self.assertTrue(platform.is_harmful())
        self.assertEqual(platform.color, 'red')
        self.assertEqual(platform.get_visual_color(), 'red')
        self.assertTrue(hasattr(platform, 'damage'))
    
    def test_frog_harmful_flag_initialization(self):
        """Test frog initializes with harmful platform flag set to False"""
        frog = Frog(400, 300)
        self.assertFalse(frog.touched_harmful_platform)
    
    def test_harmful_platform_triggers_flag(self):
        """Test that landing on harmful platform sets the harmful flag"""
        # Initially flag should be False
        self.assertFalse(self.frog.touched_harmful_platform)
        
        # Land on harmful platform
        self.harmful_platform.on_frog_land(self.frog)
        
        # Flag should now be True
        self.assertTrue(self.frog.touched_harmful_platform)
    
    def test_normal_platform_does_not_trigger_flag(self):
        """Test that landing on normal platform does not set harmful flag"""
        # Initially flag should be False
        self.assertFalse(self.frog.touched_harmful_platform)
        
        # Land on normal platform
        self.normal_platform.on_frog_land(self.frog)
        
        # Flag should remain False
        self.assertFalse(self.frog.touched_harmful_platform)
    
    def test_harmful_platform_collision_integration(self):
        """Test harmful platform works with collision system"""
        # Set up collision scenario
        self.frog.y = 340  # Just above platform
        self.frog.vy = 5   # Falling downward
        
        # Check collision and handle landing
        if self.harmful_platform.check_collision(self.frog):
            self.harmful_platform.on_collision(self.frog)
        
        # Verify collision handling worked and harmful flag is set
        self.assertTrue(self.frog.on_ground)
        self.assertEqual(self.frog.vy, 0)
        self.assertTrue(self.frog.touched_harmful_platform)
    
    def test_harmful_platform_visual_appearance(self):
        """Test harmful platform has distinct red appearance"""
        platform = Platform(400, 350, 100, 20, PlatformType.HARMFUL)
        
        # Should be red for warning
        self.assertEqual(platform.get_visual_color(), 'red')
        self.assertEqual(platform.color, 'red')
    
    def test_harmful_vs_normal_platform_comparison(self):
        """Test difference between harmful and normal platform behavior"""
        # Test normal platform
        normal_frog = Frog(400, 300)
        self.normal_platform.on_frog_land(normal_frog)
        self.assertFalse(normal_frog.touched_harmful_platform)
        
        # Test harmful platform
        harmful_frog = Frog(400, 300)
        self.harmful_platform.on_frog_land(harmful_frog)
        self.assertTrue(harmful_frog.touched_harmful_platform)
    
    def test_harmful_platform_is_harmful_method(self):
        """Test is_harmful method returns correct values"""
        # Harmful platform should return True
        self.assertTrue(self.harmful_platform.is_harmful())
        
        # Normal platform should return False
        self.assertFalse(self.normal_platform.is_harmful())
        
        # Test other platform types
        conveyor = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
        breakable = Platform(400, 350, 100, 20, PlatformType.BREAKABLE)
        moving = Platform(400, 350, 100, 20, PlatformType.MOVING)
        
        self.assertFalse(conveyor.is_harmful())
        self.assertFalse(breakable.is_harmful())
        self.assertFalse(moving.is_harmful())


class TestHarmfulPlatformGameIntegration(unittest.TestCase):
    """Integration tests for harmful platforms with game state"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Reset game state
        frog_platformer.game_state = GameState.PLAYING
        self.frog = Frog(400, 300)
        self.harmful_platform = Platform(400, 350, 100, 20, PlatformType.HARMFUL)
    
    def test_game_over_trigger_simulation(self):
        """Test that harmful platform flag would trigger game over in game loop"""
        # Simulate the game loop logic for harmful platform detection
        frog = Frog(400, 300)
        
        # Initially game should be playing
        game_state = GameState.PLAYING
        
        # Frog touches harmful platform
        self.harmful_platform.on_frog_land(frog)
        
        # Simulate the game loop check
        if frog.touched_harmful_platform:
            game_state = GameState.GAME_OVER
        
        # Game state should now be game over
        self.assertEqual(game_state, GameState.GAME_OVER)
    
    def test_game_continues_without_harmful_platform(self):
        """Test that game continues normally without harmful platform contact"""
        # Simulate the game loop logic
        frog = Frog(400, 300)
        normal_platform = Platform(400, 350, 100, 20, PlatformType.NORMAL)
        
        # Initially game should be playing
        game_state = GameState.PLAYING
        
        # Frog touches normal platform
        normal_platform.on_frog_land(frog)
        
        # Simulate the game loop check
        if frog.touched_harmful_platform:
            game_state = GameState.GAME_OVER
        
        # Game state should remain playing
        self.assertEqual(game_state, GameState.PLAYING)
    
    def test_restart_resets_harmful_flag(self):
        """Test that restarting game resets harmful platform flag"""
        # Set up frog with harmful flag set
        frog = Frog(400, 300)
        frog.touched_harmful_platform = True
        
        # Create new frog (simulating restart)
        new_frog = Frog(400, 300)
        
        # New frog should have flag reset
        self.assertFalse(new_frog.touched_harmful_platform)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)