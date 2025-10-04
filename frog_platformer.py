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
        Get the collision rectangle for this platform
        
        Returns:
            Rect: Pygame rectangle for collision detection
        """
        return Rect(self.x - self.width//2, self.y, self.width, self.height)
    
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

# Global game state
game_state = GameState.PLAYING

# Global game objects
frog = None
platforms = []

def init_game():
    """
    Initialize the game objects
    """
    global frog, platforms
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
    global game_state, frog
    
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
    
    if game_state == GameState.PLAYING:
        # Draw platforms
        for platform in platforms:
            if platform.active:
                # Draw platform as brown rectangle
                screen.draw.filled_rect(platform.get_rect(), 'brown')
                # Draw platform border
                screen.draw.rect(platform.get_rect(), 'black')
        
        # Draw frog
        if frog:
            # For now, draw a simple green rectangle as the frog
            # This will be replaced with actual sprite rendering later
            screen.draw.filled_rect(
                Rect(frog.x - frog.width//2, frog.y - frog.height//2, 
                     frog.width, frog.height), 
                'green'
            )
        
        # Show game title and status
        screen.draw.text("Frog Platformer", center=(WIDTH//2, 50), 
                        fontsize=36, color="white")
        screen.draw.text("Use SPACE/UP to jump, ARROW KEYS/WASD to move", 
                        center=(WIDTH//2, HEIGHT - 50), 
                        fontsize=16, color="white")
        screen.draw.text("Press ESC to quit", 
                        center=(WIDTH//2, HEIGHT - 30), 
                        fontsize=16, color="white")
        
        # Debug info
        if frog:
            screen.draw.text(f"Frog: ({int(frog.x)}, {int(frog.y)}) vel: ({frog.vx:.1f}, {frog.vy:.1f}) ground: {frog.on_ground}", 
                            topleft=(10, 10), fontsize=16, color="white")
    elif game_state == GameState.GAME_OVER:
        # Game over screen will be implemented later
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), 
                        fontsize=48, color="red")

# Run the game - Pygame Zero will handle this automatically