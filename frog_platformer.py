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
        
        # Sprite will be added later when we have actual image assets
        # For now, we'll use rectangle rendering in the draw function
        self.sprite = None
        
        # Set a default size for collision detection
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

# Camera Class for scroll management
class Camera:
    """
    Camera system for managing vertical scrolling and coordinate conversion
    """
    def __init__(self):
        """
        Initialize the camera at the bottom of the screen
        """
        # Camera position in world coordinates (y increases upward)
        self.y = 0.0
        
        # Camera bounds and settings
        self.follow_offset = HEIGHT * 0.3  # Keep frog in lower 30% of screen
        self.min_y = 0.0  # Minimum camera position
    
    def update(self, frog):
        """
        Update camera position to follow the frog
        
        Args:
            frog (Frog): The frog object to follow
        """
        if frog:
            # Calculate target camera position to keep frog in lower portion of screen
            target_y = frog.y - (HEIGHT - self.follow_offset)
            
            # Only move camera upward (never downward)
            if target_y > self.y:
                self.y = target_y
            
            # Ensure camera doesn't go below minimum position
            if self.y < self.min_y:
                self.y = self.min_y
    
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

# Global game state
game_state = GameState.PLAYING

# Global game objects
frog = None
platforms = []
camera = None

def init_game():
    """
    Initialize the game objects
    """
    global frog, platforms, camera
    # Initialize camera system
    camera = Camera()
    
    # Start the frog in the center-bottom of the screen
    frog = Frog(WIDTH // 2, HEIGHT - 100)
    
    # Create initial static platforms for testing
    platforms = []
    
    # Ground platform at the bottom
    platforms.append(Platform(WIDTH // 2, HEIGHT - 50, 200, 20))
    
    # Create a series of platforms going upward for testing
    # Platform 1: Left side, medium height
    platforms.append(Platform(200, HEIGHT - 150, 120, 20))
    
    # Platform 2: Right side, higher
    platforms.append(Platform(600, HEIGHT - 250, 120, 20))
    
    # Platform 3: Center, even higher
    platforms.append(Platform(400, HEIGHT - 350, 120, 20))
    
    # Platform 4: Left side, highest
    platforms.append(Platform(150, HEIGHT - 450, 120, 20))
    
    # Platform 5: Right side, very high
    platforms.append(Platform(650, HEIGHT - 550, 120, 20))

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
        
        # Update platforms
        for platform in platforms:
            platform.update()
    elif game_state == GameState.GAME_OVER:
        # Game over logic will be implemented later
        pass

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
            frog_screen_rect = Rect(frog.x - frog.width//2, frog_screen_y - frog.height//2, 
                                   frog.width, frog.height)
            
            # For now, draw a simple green rectangle as the frog
            # This will be replaced with actual sprite rendering later
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
            screen.draw.text(f"Frog World: ({int(frog.x)}, {int(frog.y)}) Screen: ({int(frog.x)}, {int(camera.world_to_screen_y(frog.y))})", 
                            topleft=(10, 10), fontsize=14, color="white")
            screen.draw.text(f"Velocity: ({frog.vx:.1f}, {frog.vy:.1f}) Ground: {frog.on_ground}", 
                            topleft=(10, 30), fontsize=14, color="white")
            screen.draw.text(f"Camera Y: {camera.y:.1f}", 
                            topleft=(10, 50), fontsize=14, color="white")
    elif game_state == GameState.GAME_OVER:
        # Game over screen will be implemented later
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), 
                        fontsize=48, color="red")

# Run the game - Pygame Zero will handle this automatically