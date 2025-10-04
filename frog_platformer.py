"""
Frog Platformer - A vertical scrolling platformer game built with Pygame Zero
"""

from enum import Enum
from pygame import Rect

# Game Configuration Constants
GAME_CONFIG = {
    'screen_width': 800,
    'screen_height': 600,
    'scroll_speed': 1.0,
    'gravity': 0.5,
    'jump_strength': -12,
    'horizontal_speed': 3,
    'platform_spacing': {
        'min_vertical': 80,
        'max_vertical': 120,
        'min_horizontal': 100
    },
    'platform_introduction': {
        100: ['slippery'],
        200: ['breakable'],
        300: ['moving'],
        400: ['harmful']
    }
}

# Screen dimensions
WIDTH = GAME_CONFIG['screen_width']
HEIGHT = GAME_CONFIG['screen_height']

# Game State Enum
class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

# Platform Type Enum
class PlatformType(Enum):
    NORMAL = "normal"
    SLIPPERY = "slippery"
    BREAKABLE = "breakable"
    MOVING = "moving"
    HARMFUL = "harmful"

# Platform Class
class Platform:
    """
    Platform class with position, size, and collision detection
    """
    def __init__(self, x, y, width=100, height=20, platform_type=PlatformType.NORMAL):
        """
        Initialize a platform
        
        Args:
            x (float): X position (center of platform)
            y (float): Y position (top of platform)
            width (int): Platform width
            height (int): Platform height
            platform_type (PlatformType): Type of platform
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type
        self.active = True  # For breakable platforms
        
        # Sprite will be added later when we have actual image assets
        self.sprite = None
    
    def get_rect(self):
        """
        Get the collision rectangle for this platform in world coordinates
        
        Returns:
            Rect: Pygame rectangle for collision detection
        """
        return Rect(self.x - self.width//2, self.y, self.width, self.height)
    
    def get_screen_rect(self, camera):
        """
        Get the collision rectangle for this platform in screen coordinates
        
        Args:
            camera (Camera): Camera object for coordinate conversion
            
        Returns:
            Rect: Pygame rectangle for rendering
        """
        screen_y = camera.world_to_screen_y(self.y)
        return Rect(self.x - self.width//2, screen_y, self.width, self.height)
    
    def check_collision(self, frog):
        """
        Check if frog is colliding with this platform from above
        
        Args:
            frog (Frog): The frog object to check collision with
            
        Returns:
            bool: True if frog is landing on platform, False otherwise
        """
        if not self.active:
            return False
            
        # Get rectangles for collision detection
        platform_rect = self.get_rect()
        frog_rect = Rect(frog.x - frog.width//2, frog.y - frog.height//2, 
                        frog.width, frog.height)
        
        # Check if rectangles overlap
        if not platform_rect.colliderect(frog_rect):
            return False
        
        # Check if frog is falling (positive vertical velocity) and landing from above
        # This prevents frog from landing when jumping up through platform
        if frog.vy > 0 and frog.y - frog.height//2 <= self.y + self.height:
            return True
            
        return False
    
    def on_collision(self, frog):
        """
        Handle frog landing on this platform
        
        Args:
            frog (Frog): The frog that landed on the platform
        """
        # Stop frog's downward movement and place on top of platform
        frog.y = self.y - frog.height//2
        frog.vy = 0
        frog.on_ground = True
    
    def update(self):
        """
        Update platform behavior (for moving/breakable platforms)
        """
        # Base platform doesn't need updates
        # This will be extended for special platform types
        pass

# Frog Character Class
class Frog:
    """
    The player-controlled frog character with physics and movement
    """
    def __init__(self, x, y):
        """
        Initialize the frog at the given position
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        # Position coordinates
        self.x = x
        self.y = y
        
        # Velocity components
        self.vx = 0.0  # Horizontal velocity
        self.vy = 0.0  # Vertical velocity
        
        # State tracking
        self.on_ground = False
        
        # Load frog sprite
        import pygame
        try:
            # Load the sprite and convert for better performance
            self.sprite_image = pygame.image.load('frg.png').convert()
            # Set black (0, 0, 0) as the transparent color
            self.sprite_image.set_colorkey((0, 0, 0))
            self.has_sprite = True
        except:
            self.has_sprite = False
        
        # Set size for collision detection (matches sprite size)
        self.width = 32
        self.height = 32
    
    def update(self):
        """
        Update frog physics, input, and state
        """
        # Apply gravity to vertical velocity
        self.vy += GAME_CONFIG['gravity']
        
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy
        
        # Keep frog within horizontal screen bounds
        if self.x < self.width // 2:
            self.x = self.width // 2
        elif self.x > WIDTH - self.width // 2:
            self.x = WIDTH - self.width // 2
        
        # Reset on_ground state - will be set by platform collision if applicable
        self.on_ground = False
    
    def jump(self):
        """
        Apply upward velocity for jumping
        Only allows jumping when frog is on ground
        """
        if self.on_ground:
            self.vy = GAME_CONFIG['jump_strength']
            self.on_ground = False
    
    def move_horizontal(self, direction):
        """
        Apply horizontal movement
        
        Args:
            direction (int): -1 for left, 1 for right, 0 for no movement
        """
        self.vx = direction * GAME_CONFIG['horizontal_speed']
    
    def check_platform_collision(self, platforms):
        """
        Handle landing on platforms
        
        Args:
            platforms (list): List of platform objects to check collision against
        """
        for platform in platforms:
            if platform.check_collision(self):
                platform.on_collision(self)
                break  # Only land on one platform at a time

# Platform Generator Class
class PlatformGenerator:
    """
    Manages dynamic platform generation above the camera view
    """
    def __init__(self):
        """
        Initialize the platform generator
        """
        # Generation parameters
        self.min_vertical_gap = 60
        self.max_vertical_gap = 100
        self.max_horizontal_reach = 120
        self.platform_width = 100
        self.platform_height = 20
        
        # Track generation state
        self.highest_platform_y = 0  # Y coordinate of highest generated platform
        self.generation_buffer = 800  # Generate platforms this far above camera
        
        # Platform pool for reuse
        self.active_platforms = []
        self.inactive_platforms = []
        
        # Memory management settings
        self.max_inactive_platforms = 50  # Maximum platforms to keep in inactive pool
        self.cleanup_margin = 200  # Margin below screen before cleanup
        
        # Statistics tracking
        self.stats = {
            'platforms_created': 0,
            'platforms_cleaned': 0,
            'platforms_reused': 0,
            'max_active_platforms': 0
        }
    
    def generate_platforms_above_camera(self, camera, target_height):
        """
        Generate platforms above the camera up to target height
        
        Args:
            camera (Camera): Camera object to determine generation area
            target_height (float): Generate platforms up to this Y coordinate
        """
        import random
        
        # Start generating from the highest existing platform (smallest Y value)
        if self.active_platforms:
            # Find the platform with the smallest Y value (highest up)
            highest_platform = min(self.active_platforms, key=lambda p: p.y)
            start_y = highest_platform.y
            current_x = highest_platform.x
        else:
            # If no platforms exist, start from camera view
            start_y = camera.y + HEIGHT - 200  # Start near bottom of screen
            current_x = WIDTH // 2
        
        current_y = start_y
        
        # Generate platforms until we reach target height
        while current_y > target_height:
            # Calculate next platform position
            vertical_gap = random.randint(self.min_vertical_gap, self.max_vertical_gap)
            next_y = current_y - vertical_gap
            
            # Calculate horizontal position within reach
            max_offset = min(self.max_horizontal_reach, 100)
            horizontal_offset = random.randint(-max_offset, max_offset)
            next_x = current_x + horizontal_offset
            
            # Keep platform within screen bounds
            margin = self.platform_width // 2 + 20
            next_x = max(margin, min(WIDTH - margin, next_x))
            
            # Create or reuse platform
            platform = self.create_platform(next_x, next_y)
            self.active_platforms.append(platform)
            
            # Update tracking
            current_x = next_x
            current_y = next_y
            # Update highest platform Y (smallest Y value = highest up)
            self.highest_platform_y = min(self.highest_platform_y, next_y)
    
    def create_platform(self, x, y):
        """
        Create a new platform or reuse an inactive one
        
        Args:
            x (float): X position
            y (float): Y position
            
        Returns:
            Platform: New or reused platform object
        """
        if self.inactive_platforms:
            # Reuse inactive platform
            platform = self.inactive_platforms.pop()
            platform.x = x
            platform.y = y
            platform.active = True
            self.stats['platforms_reused'] += 1
        else:
            # Create new platform
            platform = Platform(x, y, self.platform_width, self.platform_height)
            self.stats['platforms_created'] += 1
        
        return platform
    
    def update(self, camera):
        """
        Update platform generation based on camera position
        
        Args:
            camera (Camera): Camera object to track position
        """
        # Generate platforms ahead of camera
        target_height = camera.y - self.generation_buffer
        
        # Only generate if we need more platforms above
        if self.highest_platform_y > target_height:
            self.generate_platforms_above_camera(camera, target_height)
    
    def get_active_platforms(self):
        """
        Get list of currently active platforms
        
        Returns:
            list: List of active Platform objects
        """
        return self.active_platforms
    
    def cleanup_platforms_below_camera(self, camera, cleanup_margin=None):
        """
        Remove platforms that are far below the camera view
        
        Args:
            camera (Camera): Camera object to determine cleanup area
            cleanup_margin (float): Extra margin below screen before cleanup (optional)
        """
        if cleanup_margin is None:
            cleanup_margin = self.cleanup_margin
            
        screen_bottom = camera.screen_to_world_y(HEIGHT)
        cleanup_threshold = screen_bottom + cleanup_margin
        
        # Move platforms below threshold to inactive list
        platforms_to_remove = []
        for platform in self.active_platforms:
            if platform.y > cleanup_threshold:
                platform.active = False
                
                # Only keep platform in inactive pool if we haven't exceeded max
                if len(self.inactive_platforms) < self.max_inactive_platforms:
                    self.inactive_platforms.append(platform)
                # Otherwise, let it be garbage collected (true cleanup)
                
                platforms_to_remove.append(platform)
                self.stats['platforms_cleaned'] += 1
        
        # Remove from active list
        for platform in platforms_to_remove:
            self.active_platforms.remove(platform)
        
        # Update max active platforms stat
        self.stats['max_active_platforms'] = max(
            self.stats['max_active_platforms'], 
            len(self.active_platforms)
        )
    
    def get_memory_stats(self):
        """
        Get memory usage and performance statistics
        
        Returns:
            dict: Dictionary containing memory and performance stats
        """
        return {
            'active_platforms': len(self.active_platforms),
            'inactive_platforms': len(self.inactive_platforms),
            'total_platforms': len(self.active_platforms) + len(self.inactive_platforms),
            'platforms_created': self.stats['platforms_created'],
            'platforms_cleaned': self.stats['platforms_cleaned'],
            'platforms_reused': self.stats['platforms_reused'],
            'max_active_platforms': self.stats['max_active_platforms'],
            'reuse_efficiency': (
                self.stats['platforms_reused'] / max(1, self.stats['platforms_created'] + self.stats['platforms_reused'])
            ) * 100
        }
    
    def force_cleanup(self, keep_count=10):
        """
        Force cleanup of inactive platforms to free memory
        
        Args:
            keep_count (int): Number of inactive platforms to keep
        """
        if len(self.inactive_platforms) > keep_count:
            # Remove excess inactive platforms
            excess_count = len(self.inactive_platforms) - keep_count
            for _ in range(excess_count):
                self.inactive_platforms.pop()
            self.stats['platforms_cleaned'] += excess_count
    
    def set_cleanup_settings(self, cleanup_margin=None, max_inactive=None):
        """
        Configure cleanup system settings
        
        Args:
            cleanup_margin (float): Margin below screen before cleanup
            max_inactive (int): Maximum inactive platforms to keep
        """
        if cleanup_margin is not None:
            self.cleanup_margin = cleanup_margin
        if max_inactive is not None:
            self.max_inactive_platforms = max_inactive

# Camera Class for scroll management
class Camera:
    """
    Camera system for managing vertical scrolling and coordinate conversion
    """
    def __init__(self):
        """
        Initialize the camera at the starting position
        """
        # Camera position - represents the Y coordinate of the top of the camera view
        # In Pygame coordinates: Y=0 is top of screen, Y increases downward
        self.y = 0.0  # Start with camera at the very top
        
        # Camera bounds and settings
        self.follow_offset = HEIGHT * 0.3  # Keep frog in lower 30% of screen
        self.max_y = 0.0  # Maximum camera Y position (never go below starting position)
        
        # Automatic scrolling settings (disabled by default - camera follows frog instead)
        self.scroll_speed = GAME_CONFIG['scroll_speed']  # Units per frame to scroll upward
        self.auto_scroll_enabled = False  # Enable/disable automatic scrolling
    
    def update(self, frog):
        """
        Update camera position to follow the frog (upward only, never down)
        
        Args:
            frog (Frog): The frog object to follow
        """
        # Apply automatic upward scrolling if enabled
        # Upward scrolling means camera.y decreases (moving toward negative values)
        if self.auto_scroll_enabled:
            self.y -= self.scroll_speed
        
        if frog:
            # Calculate target camera position to keep frog in lower portion of screen
            # We want the frog to be at about 70% down the screen (HEIGHT - follow_offset)
            target_y = frog.y - (HEIGHT - self.follow_offset)
            
            # Only move camera upward (never downward) - this creates the "scrolling" effect
            # When frog jumps UP (frog.y decreases), camera should move UP (camera.y decreases)
            # When frog falls DOWN, camera stays where it is (never moves down)
            if target_y < self.y:  # Frog is getting too high, move camera up
                self.y = target_y
            
            # Ensure camera doesn't go below starting position (never scroll down)
            if self.y > self.max_y:
                self.y = self.max_y
    
    def world_to_screen_y(self, world_y):
        """
        Convert world Y coordinate to screen Y coordinate
        
        Args:
            world_y (float): Y coordinate in world space
            
        Returns:
            float: Y coordinate in screen space
        """
        return world_y - self.y
    
    def screen_to_world_y(self, screen_y):
        """
        Convert screen Y coordinate to world Y coordinate
        
        Args:
            screen_y (float): Y coordinate in screen space
            
        Returns:
            float: Y coordinate in world space
        """
        return screen_y + self.y
    
    def is_visible(self, world_y, object_height=0):
        """
        Check if an object at the given world Y coordinate is visible on screen
        
        Args:
            world_y (float): Y coordinate in world space
            object_height (float): Height of the object (optional)
            
        Returns:
            bool: True if object is visible, False otherwise
        """
        screen_y = self.world_to_screen_y(world_y)
        return -object_height <= screen_y <= HEIGHT + object_height
    
    def get_visible_bounds(self):
        """
        Get the world coordinate bounds of what's currently visible
        
        Returns:
            tuple: (top_world_y, bottom_world_y) of visible area
        """
        top_world_y = self.screen_to_world_y(0)
        bottom_world_y = self.screen_to_world_y(HEIGHT)
        return (top_world_y, bottom_world_y)
    
    def set_scroll_speed(self, speed):
        """
        Set the automatic scroll speed
        
        Args:
            speed (float): New scroll speed in units per frame
        """
        self.scroll_speed = speed
    
    def enable_auto_scroll(self, enabled=True):
        """
        Enable or disable automatic scrolling
        
        Args:
            enabled (bool): True to enable, False to disable
        """
        self.auto_scroll_enabled = enabled
    
    def get_scroll_distance(self):
        """
        Get the total distance the camera has scrolled upward
        
        Returns:
            float: Total scroll distance from starting position (positive = scrolled up)
        """
        return self.max_y - self.y  # Positive when camera has moved up (y decreased)
    
    def is_frog_below_screen(self, frog, margin=50):
        """
        Check if the frog has fallen below the visible screen area
        
        Args:
            frog (Frog): The frog object to check
            margin (float): Extra margin below screen before triggering game over
            
        Returns:
            bool: True if frog is below screen (game over), False otherwise
        """
        if not frog:
            return False
            
        # Calculate the bottom of the screen in world coordinates
        screen_bottom = self.screen_to_world_y(HEIGHT)
        
        # Check if frog is below screen bottom plus margin
        frog_bottom = frog.y + frog.height // 2
        return frog_bottom > screen_bottom + margin

# Global game state
game_state = GameState.PLAYING

# Global game objects
frog = None
platforms = []
camera = None
platform_generator = None

def generate_reachable_platforms(start_x, start_y, count=20):
    """
    Generate a series of platforms that are always reachable from each other
    
    Args:
        start_x (float): Starting X position
        start_y (float): Starting Y position  
        count (int): Number of platforms to generate
        
    Returns:
        list: List of Platform objects
    """
    import random
    
    platforms = []
    current_x = start_x
    current_y = start_y
    
    # Calculate safe jump parameters based on frog physics
    max_jump_height = 120  # Slightly less than theoretical max (144) for safety
    max_horizontal_reach = 120  # Safe horizontal distance
    min_vertical_gap = 60   # Minimum vertical spacing
    max_vertical_gap = max_jump_height - 20  # Leave some margin
    
    platform_width = 100
    
    for i in range(count):
        # For the first platform (ground), use the starting position
        if i == 0:
            platforms.append(Platform(current_x, current_y, 200, 20))  # Wider ground platform
            continue
        
        # Calculate next platform position within reachable range
        # Vertical spacing: always upward, within jump range
        vertical_gap = random.randint(min_vertical_gap, max_vertical_gap)
        next_y = current_y - vertical_gap  # Negative because Y decreases going up
        
        # Horizontal spacing: within horizontal reach, but varied
        max_horizontal_offset = min(max_horizontal_reach, 100)  # Cap for better gameplay
        horizontal_offset = random.randint(-max_horizontal_offset, max_horizontal_offset)
        next_x = current_x + horizontal_offset
        
        # Keep platforms within screen bounds with some margin
        platform_margin = platform_width // 2 + 20
        next_x = max(platform_margin, min(WIDTH - platform_margin, next_x))
        
        # Create the platform
        platforms.append(Platform(next_x, next_y, platform_width, 20))
        
        # Update current position for next iteration
        current_x = next_x
        current_y = next_y
    
    return platforms

def init_game():
    """
    Initialize the game objects
    """
    global frog, platforms, camera, platform_generator
    # Initialize camera system
    camera = Camera()
    
    # Initialize platform generator
    platform_generator = PlatformGenerator()
    
    # Start the frog in the center-bottom of the screen
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    
    # Create initial ground platform
    ground_platform = Platform(WIDTH // 2, HEIGHT - 50, 200, 20)
    platform_generator.active_platforms.append(ground_platform)
    platform_generator.highest_platform_y = HEIGHT - 50
    
    # Generate initial set of platforms
    platform_generator.generate_platforms_above_camera(camera, camera.y - 1000)
    
    # Get platforms from generator
    platforms = platform_generator.get_active_platforms()

def restart_game():
    """
    Restart the game by resetting all game objects and state
    """
    global game_state
    game_state = GameState.PLAYING
    init_game()

def handle_input():
    """
    Handle player input for frog movement
    """
    global frog
    
    # Quit game with ESC key
    if keyboard.escape:
        exit()
    
    if frog:
        # Jump input (space bar or up arrow)
        if keyboard.space or keyboard.up:
            frog.jump()
        
        # Horizontal movement input
        horizontal_direction = 0
        if keyboard.left or keyboard.a:
            horizontal_direction = -1
        elif keyboard.right or keyboard.d:
            horizontal_direction = 1
        
        frog.move_horizontal(horizontal_direction)

def update():
    """
    Main game update loop - called every frame
    Handles game logic, physics, and state updates
    """
    global game_state, frog, camera
    
    # Initialize game objects if not already done
    if frog is None:
        init_game()
    
    if game_state == GameState.PLAYING:
        # Handle player input
        handle_input()
        
        # Update frog
        if frog:
            frog.update()
            # Check platform collisions after frog physics update
            frog.check_platform_collision(platforms)
        
        # Update camera to follow frog
        if camera and frog:
            camera.update(frog)
            
            # Check if frog has fallen below screen (game over condition)
            if camera.is_frog_below_screen(frog):
                game_state = GameState.GAME_OVER
        
        # Update platform generator
        if platform_generator and camera:
            platform_generator.update(camera)
            platform_generator.cleanup_platforms_below_camera(camera)
            # Update platforms list from generator
            platforms[:] = platform_generator.get_active_platforms()
        
        # Update platforms
        for platform in platforms:
            platform.update()
    elif game_state == GameState.GAME_OVER:
        # Handle game over input
        if keyboard.space or keyboard.RETURN:
            # Restart the game
            restart_game()
        elif keyboard.escape:
            exit()

def draw():
    """
    Main drawing function - called every frame
    Handles all rendering and visual updates
    """
    # Clear screen with sky blue background
    screen.fill((135, 206, 235))
    
    if game_state == GameState.PLAYING and camera:
        # Draw platforms using camera-relative coordinates
        for platform in platforms:
            if platform.active and camera.is_visible(platform.y, platform.height):
                # Get screen coordinates for platform
                screen_rect = platform.get_screen_rect(camera)
                # Draw platform as brown rectangle
                screen.draw.filled_rect(screen_rect, 'brown')
                # Draw platform border
                screen.draw.rect(screen_rect, 'black')
        
        # Draw frog using camera-relative coordinates
        if frog:
            # Convert frog world coordinates to screen coordinates
            frog_screen_y = camera.world_to_screen_y(frog.y)
            frog_screen_x = frog.x - frog.width//2
            frog_screen_y = frog_screen_y - frog.height//2
            
            # Draw frog sprite or fallback to rectangle
            if frog.has_sprite:
                screen.blit(frog.sprite_image, (frog_screen_x, frog_screen_y))
            else:
                # Fallback to green rectangle if sprite fails to load
                frog_screen_rect = Rect(frog_screen_x, frog_screen_y, frog.width, frog.height)
                screen.draw.filled_rect(frog_screen_rect, 'green')
        
        # Show game title and status (UI elements stay in screen coordinates)
        screen.draw.text("Frog Platformer", center=(WIDTH//2, 50), 
                        fontsize=36, color="white")
        screen.draw.text("Use SPACE/UP to jump, ARROW KEYS/WASD to move", 
                        center=(WIDTH//2, HEIGHT - 50), 
                        fontsize=16, color="white")
        screen.draw.text("Press ESC to quit", 
                        center=(WIDTH//2, HEIGHT - 30), 
                        fontsize=16, color="white")
        
        # Debug info (enhanced with camera information)
        if frog and camera:
            screen.draw.text(f"Height: {int(camera.get_scroll_distance())}", 
                            topleft=(10, 10), fontsize=16, color="white")
            screen.draw.text(f"Frog: ({int(frog.x)}, {int(frog.y)}) Ground: {frog.on_ground}", 
                            topleft=(10, 30), fontsize=14, color="white")
            
            # Memory stats (show if M key is pressed)
            if platform_generator and keyboard.m:
                stats = platform_generator.get_memory_stats()
                screen.draw.text(f"Memory: Active={stats['active_platforms']} Inactive={stats['inactive_platforms']}", 
                                topleft=(10, 50), fontsize=12, color="yellow")
                screen.draw.text(f"Created={stats['platforms_created']} Reused={stats['platforms_reused']} Efficiency={stats['reuse_efficiency']:.1f}%", 
                                topleft=(10, 65), fontsize=12, color="yellow")
    elif game_state == GameState.GAME_OVER:
        # Game over screen
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 60), 
                        fontsize=48, color="red")
        
        # Show final score (scroll distance)
        if camera:
            final_score = int(camera.get_scroll_distance())
            screen.draw.text(f"Height Reached: {final_score}", center=(WIDTH//2, HEIGHT//2 - 10), 
                            fontsize=24, color="white")
        
        # Instructions
        screen.draw.text("Press SPACE or RETURN to restart", center=(WIDTH//2, HEIGHT//2 + 30), 
                        fontsize=20, color="white")
        screen.draw.text("Press ESC to quit", center=(WIDTH//2, HEIGHT//2 + 60), 
                        fontsize=16, color="white")

# Run the game - Pygame Zero will handle this automatically