"""
Unit tests for game over detection system
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import Camera, Frog, GameState, restart_game
import frog_platformer


class TestGameOverDetection(unittest.TestCase):
    """Test cases for game over detection functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.camera = Camera()
        self.frog = Frog(400, 300)
    
    def test_frog_below_screen_detection(self):
        """Test detection when frog falls below screen"""
        # Position camera at a certain height
        self.camera.y = -100  # Camera scrolled up
        
        # Position frog well below screen
        screen_bottom = self.camera.screen_to_world_y(600)  # Bottom of screen in world coords
        self.frog.y = screen_bottom + 100  # Frog below screen
        
        # Should detect frog is below screen
        self.assertTrue(self.camera.is_frog_below_screen(self.frog))
    
    def test_frog_on_screen_no_game_over(self):
        """Test that frog on screen doesn't trigger game over"""
        # Position camera at a certain height
        self.camera.y = -100
        
        # Position frog on screen
        self.frog.y = self.camera.screen_to_world_y(300)  # Middle of screen
        
        # Should not detect game over
        self.assertFalse(self.camera.is_frog_below_screen(self.frog))
    
    def test_frog_just_below_screen_with_margin(self):
        """Test margin before triggering game over"""
        # Position camera
        self.camera.y = -100
        
        # Position frog just below screen but within margin
        screen_bottom = self.camera.screen_to_world_y(600)
        self.frog.y = screen_bottom + 25  # Within default margin of 50
        
        # Should not trigger game over yet (within margin)
        self.assertFalse(self.camera.is_frog_below_screen(self.frog))
        
        # Position frog beyond margin
        self.frog.y = screen_bottom + 75  # Beyond margin
        
        # Should trigger game over
        self.assertTrue(self.camera.is_frog_below_screen(self.frog))
    
    def test_custom_margin(self):
        """Test game over detection with custom margin"""
        self.camera.y = -100
        screen_bottom = self.camera.screen_to_world_y(600)
        
        # Test with custom margin of 100
        self.frog.y = screen_bottom + 75
        
        # Should not trigger with larger margin
        self.assertFalse(self.camera.is_frog_below_screen(self.frog, margin=100))
        
        # Should trigger with smaller margin
        self.assertTrue(self.camera.is_frog_below_screen(self.frog, margin=50))
    
    def test_frog_size_consideration(self):
        """Test that frog's bottom edge is used for detection"""
        self.camera.y = -100
        screen_bottom = self.camera.screen_to_world_y(600)
        
        # Position frog so its center is at screen bottom
        self.frog.y = screen_bottom
        
        # Frog's bottom should be below screen (center + height/2)
        # With default frog height of 32, bottom is at screen_bottom + 16
        # This should trigger game over with default margin of 50
        self.assertFalse(self.camera.is_frog_below_screen(self.frog))
        
        # Move frog further down
        self.frog.y = screen_bottom + 40
        # Now frog bottom is at screen_bottom + 56, beyond margin
        self.assertTrue(self.camera.is_frog_below_screen(self.frog))
    
    def test_no_frog_no_game_over(self):
        """Test that None frog doesn't trigger game over"""
        self.assertFalse(self.camera.is_frog_below_screen(None))
    
    def test_restart_game_functionality(self):
        """Test that restart_game resets the game state"""
        # Set game state to game over
        frog_platformer.game_state = GameState.GAME_OVER
        
        # Restart game
        restart_game()
        
        # Should be back to playing state
        self.assertEqual(frog_platformer.game_state, GameState.PLAYING)
        
        # Should have new game objects
        self.assertIsNotNone(frog_platformer.frog)
        self.assertIsNotNone(frog_platformer.camera)
        self.assertGreater(len(frog_platformer.platforms), 0)


class TestGameOverIntegration(unittest.TestCase):
    """Integration tests for game over system"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Initialize a fresh game
        frog_platformer.init_game()
        frog_platformer.game_state = GameState.PLAYING
    
    def test_game_over_triggers_correctly(self):
        """Test that game over is triggered when frog falls off screen"""
        # Get game objects
        frog = frog_platformer.frog
        camera = frog_platformer.camera
        
        # Move camera up significantly
        camera.y = -500
        
        # Position frog way below screen
        screen_bottom = camera.screen_to_world_y(600)
        frog.y = screen_bottom + 100
        
        # Simulate one update cycle
        if camera and frog:
            camera.update(frog)
            if camera.is_frog_below_screen(frog):
                frog_platformer.game_state = GameState.GAME_OVER
        
        # Should trigger game over
        self.assertEqual(frog_platformer.game_state, GameState.GAME_OVER)
    
    def test_game_continues_when_frog_on_screen(self):
        """Test that game continues when frog is visible"""
        # Get game objects
        frog = frog_platformer.frog
        camera = frog_platformer.camera
        
        # Keep frog on screen
        frog.y = camera.screen_to_world_y(300)  # Middle of screen
        
        # Simulate update
        if camera and frog:
            camera.update(frog)
            if camera.is_frog_below_screen(frog):
                frog_platformer.game_state = GameState.GAME_OVER
        
        # Should still be playing
        self.assertEqual(frog_platformer.game_state, GameState.PLAYING)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)