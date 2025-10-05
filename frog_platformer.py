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
        100: ['conveyor'],
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
    CONVEYOR = "conveyor"
    BREAKABLE = "breakable"
    MOVING = "moving"
    VERTICAL = "vertical"
    BOUNCY = "bouncy"
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
        
        # Type-specific properties
        self.initialize_type_properties()
        
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
        
        # Special case for conveyor platforms: maintain contact only when frog is properly on platform
        # This allows continuous conveyor effect while frog is on the platform
        if (self.platform_type == PlatformType.CONVEYOR and 
            frog.vy >= 0 and  # Not jumping up
            frog.on_ground and  # Must be grounded first
            abs(frog.y - frog.height//2 - self.y) <= 2):  # Very close to platform surface
            return True
            
        return False
    
    def on_collision(self, frog):
        """
        Handle frog landing on this platform
        
        Args:
            frog (Frog): The frog that landed on the platform
        """
        # Use type-specific landing behavior
        self.on_frog_land(frog)
    
    def initialize_type_properties(self):
        """
        Initialize properties specific to platform type
        """
        if self.platform_type == PlatformType.NORMAL:
            self.friction = 1.0
            self.color = 'brown'
            
        elif self.platform_type == PlatformType.CONVEYOR:
            self.friction = 1.0  # Normal friction
            self.color = 'gray'
            self.conveyor_speed = 3.5  # Pixels per frame sideways movement
            self.conveyor_direction = 1 if self.x % 2 == 0 else -1  # Alternate directions based on position
            
        elif self.platform_type == PlatformType.BREAKABLE:
            self.friction = 1.0
            self.color = 'orange'
            self.break_timer = 0.0
            self.break_delay = 1.0  # Seconds before breaking
            self.stepped_on = False
            
        elif self.platform_type == PlatformType.MOVING:
            self.friction = 1.0
            self.color = 'purple'
            self.move_speed = 1.0
            self.move_direction = 1  # 1 for right, -1 for left
            self.move_range = 100  # Pixels to move in each direction
            self.original_x = self.x
            
        elif self.platform_type == PlatformType.VERTICAL:
            self.friction = 1.0
            self.color = 'cyan'
            self.move_speed = 0.8  # Slightly slower for vertical movement
            self.move_direction = 1  # 1 for up, -1 for down
            self.move_range = 80  # Pixels to move in each direction
            self.original_y = self.y
            
        elif self.platform_type == PlatformType.BOUNCY:
            self.friction = 1.0
            self.color = 'pink'
            self.bounce_power = 2.0  # Multiplier for jump height (double normal jump)
            
        elif self.platform_type == PlatformType.HARMFUL:
            self.friction = 1.0
            self.color = 'red'
            self.damage = True
    
    def get_friction_multiplier(self):
        """
        Get the friction multiplier for this platform type
        
        Returns:
            float: Friction multiplier (1.0 = normal, <1.0 = slippery)
        """
        return getattr(self, 'friction', 1.0)
    
    def is_harmful(self):
        """
        Check if this platform is harmful to the frog
        
        Returns:
            bool: True if platform causes damage/game over
        """
        return self.platform_type == PlatformType.HARMFUL
    
    def should_break(self):
        """
        Check if this breakable platform should break
        
        Returns:
            bool: True if platform should break and become inactive
        """
        if self.platform_type == PlatformType.BREAKABLE and self.stepped_on:
            return self.break_timer >= self.break_delay
        return False
    
    def on_frog_land(self, frog):
        """
        Handle frog landing on this platform (type-specific behavior)
        
        Args:
            frog (Frog): The frog that landed on the platform
        """
        # Base collision behavior - position frog slightly inside platform for better collision detection
        frog.y = self.y - frog.height//2 + 1
        
        # Bouncy platforms have special behavior - they don't make frog grounded
        if self.platform_type == PlatformType.BOUNCY:
            # Launch frog upward with bounce power
            normal_jump_velocity = GAME_CONFIG['jump_strength']
            bounce_velocity = normal_jump_velocity * self.bounce_power
            frog.vy = bounce_velocity
            frog.on_ground = False  # Frog should be airborne immediately
        else:
            frog.vy = 0
            frog.on_ground = True
        
        # Type-specific behavior
        if self.platform_type == PlatformType.CONVEYOR:
            # Apply conveyor belt movement to frog
            frog.vx += self.conveyor_speed * self.conveyor_direction
            # Mark frog as being on conveyor
            frog.on_conveyor = True
            frog.conveyor_platform = self
            
        elif self.platform_type == PlatformType.BREAKABLE:
            # Start break timer
            if not self.stepped_on:
                self.stepped_on = True
                self.break_timer = 0.0
                
        elif self.platform_type == PlatformType.MOVING:
            # Frog moves with the platform
            frog.x += self.move_speed * self.move_direction
            
        elif self.platform_type == PlatformType.VERTICAL:
            # Frog moves with the vertical platform
            frog.y += self.move_speed * self.move_direction
            
        elif self.platform_type == PlatformType.HARMFUL:
            # Trigger game over immediately when frog touches harmful platform
            # Set a flag that the game loop will check
            frog.touched_harmful_platform = True
    
    def update(self, dt=1/60):
        """
        Update platform behavior (for moving/breakable platforms)
        
        Args:
            dt (float): Delta time in seconds
        """
        if self.platform_type == PlatformType.CONVEYOR:
            # Conveyor platforms don't need special update behavior
            pass
            
        elif self.platform_type == PlatformType.BREAKABLE and self.stepped_on:
            # Update break timer
            self.break_timer += dt
            if self.should_break():
                self.active = False
                
        elif self.platform_type == PlatformType.MOVING:
            # Update moving platform position
            self.x += self.move_speed * self.move_direction
            
            # Reverse direction if reached movement limits
            if self.x >= self.original_x + self.move_range:
                self.move_direction = -1
            elif self.x <= self.original_x - self.move_range:
                self.move_direction = 1
                
            # Keep within screen bounds
            margin = self.width // 2 + 10
            if self.x < margin:
                self.x = margin
                self.move_direction = 1
            elif self.x > WIDTH - margin:
                self.x = WIDTH - margin
                self.move_direction = -1
                
        elif self.platform_type == PlatformType.VERTICAL:
            # Update vertical moving platform position
            self.y += self.move_speed * self.move_direction
            
            # Reverse direction if reached movement limits
            if self.y >= self.original_y + self.move_range:
                self.move_direction = -1
            elif self.y <= self.original_y - self.move_range:
                self.move_direction = 1
    
    def get_visual_color(self):
        """
        Get the color for rendering this platform
        
        Returns:
            str: Color name for rendering
        """
        if self.platform_type == PlatformType.CONVEYOR:
            # Conveyor platforms have a consistent gray appearance
            return self.color
                
        elif self.platform_type == PlatformType.BREAKABLE and self.stepped_on:
            # Flash red when about to break
            flash_intensity = self.break_timer / self.break_delay
            if flash_intensity > 0.7:
                return 'red' if int(self.break_timer * 10) % 2 else self.color
        
        return getattr(self, 'color', 'brown')

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
        self.on_conveyor = False
        self.conveyor_platform = None
        self.touched_harmful_platform = False
        self.last_platform_landed = None  # For progress tracking
        
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
        
        # Handle continuous conveyor effects while on conveyor platform
        if self.on_conveyor and self.conveyor_platform:
            # Apply continuous conveyor movement
            conveyor_push = self.conveyor_platform.conveyor_speed * self.conveyor_platform.conveyor_direction * 0.5
            self.vx += conveyor_push
            
            # Cap maximum conveyor velocity to prevent extreme speeds
            max_conveyor_speed = 8.0
            if abs(self.vx) > max_conveyor_speed:
                self.vx = max_conveyor_speed if self.vx > 0 else -max_conveyor_speed
        
        # Reset ground state - will be set by platform collision if applicable
        self.on_ground = False
        # Note: conveyor state will be reset in check_platform_collision
    
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
        base_speed = GAME_CONFIG['horizontal_speed']
        
        if direction != 0:
            # Player is giving input - set velocity directly
            self.vx = direction * base_speed
        else:
            # No input - behavior depends on platform type
            if self.on_conveyor and self.conveyor_platform:
                # On conveyor: let conveyor effect continue (don't change vx)
                pass
            else:
                # On normal platform: stop horizontal movement
                self.vx = 0
    
    def check_platform_collision(self, platforms):
        """
        Handle landing on platforms
        
        Args:
            platforms (list): List of platform objects to check collision against
        """
        # Reset conveyor state - will be set by platform collision if applicable
        self.on_conveyor = False
        self.conveyor_platform = None
        
        for platform in platforms:
            if platform.check_collision(self):
                platform.on_collision(self)
                
                # Set a flag for progress tracking (will be handled in main update loop)
                self.last_platform_landed = platform.platform_type
                
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
        
        # Physics-based reachability parameters
        self.frog_jump_height = 144  # Maximum jump height (from physics)
        self.frog_horizontal_reach = 144  # Maximum horizontal reach
        self.safety_margin = 0.8  # Use 80% of max reach for safety
        
        # Platform density requirements
        self.min_platforms_in_range = 2  # Minimum platforms within jumping range
        self.density_check_radius = 200  # Check density within this radius
        
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
        
        # Platform type generation settings
        self.type_introduction_heights = {
            1000: [PlatformType.CONVEYOR],
            2000: [PlatformType.BREAKABLE],
            3000: [PlatformType.MOVING],
            3500: [PlatformType.VERTICAL],
            3750: [PlatformType.BOUNCY],
            4000: [PlatformType.HARMFUL]
        }
        self.special_platform_chance = 0.3  # 30% chance for special platforms
    
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
            # Calculate next platform position with validation
            vertical_gap = random.randint(self.min_vertical_gap, self.max_vertical_gap)
            next_y = current_y - vertical_gap
            
            # Find last platform to ensure reachability
            last_platform = None
            if self.active_platforms:
                for platform in self.active_platforms:
                    if platform.y == current_y or abs(platform.y - current_y) < 10:
                        last_platform = platform
                        break
            
            if last_platform:
                # Use validation to find reachable position
                position = self.find_reachable_position(last_platform, next_y)
                if position:
                    next_x, next_y = position
                else:
                    # Fallback: use safer parameters
                    next_y = current_y - self.min_vertical_gap
                    next_x = current_x + random.randint(-60, 60)  # Conservative range
            else:
                # Fallback to original method if no reference platform
                max_offset = min(self.max_horizontal_reach, 100)
                horizontal_offset = random.randint(-max_offset, max_offset)
                next_x = current_x + horizontal_offset
            
            # Keep platform within screen bounds
            margin = self.platform_width // 2 + 20
            next_x = max(margin, min(WIDTH - margin, next_x))
            
            # Ensure position doesn't overlap existing platforms
            if self.position_overlaps_existing(next_x, next_y):
                # Adjust position slightly
                for offset in [40, -40, 80, -80]:
                    test_x = next_x + offset
                    if (not self.position_overlaps_existing(test_x, next_y) and 
                        margin <= test_x <= WIDTH - margin):
                        next_x = test_x
                        break
            
            # Select platform type based on progress
            height_progress = abs(next_y)  # Use absolute Y as progress measure
            platform_type = self.select_platform_type(height_progress)
            
            # Create or reuse platform
            platform = self.create_platform(next_x, next_y, platform_type)
            self.active_platforms.append(platform)
            
            # Add safety platform for harmful platforms to prevent softlocks
            if platform_type == PlatformType.HARMFUL:
                self.add_safety_platform_for_harmful(next_x, next_y)
            
            # Only ensure minimum density for normal platforms to avoid interfering with special platforms
            if platform_type == PlatformType.NORMAL:
                self.ensure_minimum_density(next_x, next_y)
            
            # Update tracking
            current_x = next_x
            current_y = next_y
            # Update highest platform Y (smallest Y value = highest up)
            self.highest_platform_y = min(self.highest_platform_y, next_y)
    
    def create_platform(self, x, y, platform_type=None):
        """
        Create a new platform or reuse an inactive one
        
        Args:
            x (float): X position
            y (float): Y position
            platform_type (PlatformType): Type of platform to create (optional)
            
        Returns:
            Platform: New or reused platform object
        """
        if platform_type is None:
            platform_type = PlatformType.NORMAL
            
        if self.inactive_platforms:
            # Reuse inactive platform
            platform = self.inactive_platforms.pop()
            platform.x = x
            platform.y = y
            platform.platform_type = platform_type
            platform.active = True
            platform.initialize_type_properties()  # Reinitialize for new type
            self.stats['platforms_reused'] += 1
        else:
            # Create new platform
            platform = Platform(x, y, self.platform_width, self.platform_height, platform_type)
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
            
            # Periodically validate and fix layout issues
            if len(self.active_platforms) % 10 == 0:  # Check every 10 platforms
                issues = self.validate_platform_layout()
                if (issues['unreachable_platforms'] or 
                    len(issues['low_density_areas']) > 2):  # Fix if significant issues
                    self.fix_layout_issues(issues)
    
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
    
    def is_platform_reachable(self, from_platform, to_x, to_y):
        """
        Check if a platform position is reachable from another platform
        
        Args:
            from_platform (Platform): Starting platform
            to_x (float): Target X position
            to_y (float): Target Y position
            
        Returns:
            bool: True if target position is reachable
        """
        # Calculate distances
        horizontal_distance = abs(to_x - from_platform.x)
        vertical_distance = from_platform.y - to_y  # Positive = jumping up
        
        # Apply safety margins
        max_safe_horizontal = self.frog_horizontal_reach * self.safety_margin
        max_safe_vertical = self.frog_jump_height * self.safety_margin
        
        # Check if within safe jumping range
        horizontal_ok = horizontal_distance <= max_safe_horizontal
        
        # For vertical: can jump up (positive vertical_distance) or fall down (negative)
        if vertical_distance >= 0:  # Jumping up
            vertical_ok = vertical_distance <= max_safe_vertical
        else:  # Falling down - always reachable if horizontal distance is OK
            vertical_ok = True
        
        return horizontal_ok and vertical_ok
    
    def find_reachable_position(self, from_platform, target_y, attempts=10):
        """
        Find a reachable position for a new platform
        
        Args:
            from_platform (Platform): Platform to jump from
            target_y (float): Desired Y coordinate
            attempts (int): Maximum attempts to find valid position
            
        Returns:
            tuple: (x, y) coordinates of valid position, or None if not found
        """
        import random
        
        # Ensure target_y is reachable
        max_jump_up = from_platform.y - (self.frog_jump_height * self.safety_margin)
        if target_y < max_jump_up:
            target_y = max_jump_up
        
        for _ in range(attempts):
            # Generate random horizontal offset within safe range
            max_offset = self.frog_horizontal_reach * self.safety_margin * 0.7  # Even more conservative
            horizontal_offset = random.randint(-int(max_offset), int(max_offset))
            candidate_x = from_platform.x + horizontal_offset
            
            # Keep within screen bounds
            margin = self.platform_width // 2 + 20
            candidate_x = max(margin, min(WIDTH - margin, candidate_x))
            
            # Verify reachability
            if self.is_platform_reachable(from_platform, candidate_x, target_y):
                return (candidate_x, target_y)
        
        return None
    
    def check_platform_density(self, center_x, center_y):
        """
        Check if there are enough platforms within jumping range of a position
        
        Args:
            center_x (float): X coordinate to check around
            center_y (float): Y coordinate to check around
            
        Returns:
            int: Number of platforms within jumping range
        """
        count = 0
        check_radius = self.density_check_radius
        
        for platform in self.active_platforms:
            distance_x = abs(platform.x - center_x)
            distance_y = abs(platform.y - center_y)
            
            # Check if within density check radius
            if distance_x <= check_radius and distance_y <= check_radius:
                # Check if actually reachable (more precise)
                if (distance_x <= self.frog_horizontal_reach * self.safety_margin and 
                    distance_y <= self.frog_jump_height * self.safety_margin):
                    count += 1
        
        return count
    
    def ensure_minimum_density(self, around_x, around_y):
        """
        Ensure minimum platform density around a position by adding platforms if needed
        
        Args:
            around_x (float): X coordinate to ensure density around
            around_y (float): Y coordinate to ensure density around
        """
        current_density = self.check_platform_density(around_x, around_y)
        
        if current_density < self.min_platforms_in_range:
            needed = self.min_platforms_in_range - current_density
            
            # Add platforms to meet minimum density
            for _ in range(needed):
                # Find a good position for additional platform
                position = self.find_safe_platform_position(around_x, around_y)
                if position:
                    x, y = position
                    platform = self.create_platform(x, y)
                    self.active_platforms.append(platform)
    
    def find_safe_platform_position(self, near_x, near_y):
        """
        Find a safe position for a platform near given coordinates
        
        Args:
            near_x (float): X coordinate to place platform near
            near_y (float): Y coordinate to place platform near
            
        Returns:
            tuple: (x, y) coordinates of safe position, or None
        """
        import random
        
        for _ in range(20):  # Try multiple positions
            # Generate position within reachable range
            offset_x = random.randint(-80, 80)  # Conservative horizontal range
            offset_y = random.randint(-80, 20)   # Mostly above, some below
            
            candidate_x = near_x + offset_x
            candidate_y = near_y + offset_y
            
            # Keep within screen bounds
            margin = self.platform_width // 2 + 20
            candidate_x = max(margin, min(WIDTH - margin, candidate_x))
            
            # Check if position doesn't overlap with existing platforms
            if not self.position_overlaps_existing(candidate_x, candidate_y):
                return (candidate_x, candidate_y)
        
        return None
    
    def position_overlaps_existing(self, x, y, min_distance=80):
        """
        Check if a position is too close to existing platforms
        
        Args:
            x (float): X coordinate to check
            y (float): Y coordinate to check
            min_distance (float): Minimum distance from existing platforms
            
        Returns:
            bool: True if position overlaps/too close to existing platforms
        """
        for platform in self.active_platforms:
            distance_x = abs(platform.x - x)
            distance_y = abs(platform.y - y)
            
            if distance_x < min_distance and distance_y < min_distance:
                return True
        
        return False
    
    def validate_platform_layout(self):
        """
        Validate that the current platform layout is fully reachable
        
        Returns:
            dict: Validation results with issues found
        """
        issues = {
            'unreachable_platforms': [],
            'low_density_areas': [],
            'isolated_platforms': []
        }
        
        # Sort platforms by Y coordinate (bottom to top)
        sorted_platforms = sorted(self.active_platforms, key=lambda p: p.y, reverse=True)
        
        # Check each platform's reachability from others
        for i, platform in enumerate(sorted_platforms):
            reachable_from = []
            
            # Check if reachable from platforms below it
            for j, other_platform in enumerate(sorted_platforms):
                if other_platform.y > platform.y:  # Other platform is below
                    if self.is_platform_reachable(other_platform, platform.x, platform.y):
                        reachable_from.append(other_platform)
            
            # If no platforms can reach this one, it's unreachable
            if not reachable_from and i > 0:  # Skip ground platform
                issues['unreachable_platforms'].append(platform)
            
            # Check density around this platform
            density = self.check_platform_density(platform.x, platform.y)
            if density < self.min_platforms_in_range:
                issues['low_density_areas'].append((platform, density))
        
        return issues
    
    def fix_layout_issues(self, issues):
        """
        Attempt to fix layout issues by adding platforms
        
        Args:
            issues (dict): Issues found by validate_platform_layout
        """
        # Fix unreachable platforms by adding intermediate platforms
        for platform in issues['unreachable_platforms']:
            # Find nearest lower platform
            nearest_lower = None
            min_distance = float('inf')
            
            for other in self.active_platforms:
                if other.y > platform.y:  # Other is below
                    distance = ((other.x - platform.x) ** 2 + (other.y - platform.y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        nearest_lower = other
            
            if nearest_lower:
                # Add intermediate platform
                mid_x = (nearest_lower.x + platform.x) / 2
                mid_y = (nearest_lower.y + platform.y) / 2
                
                if not self.position_overlaps_existing(mid_x, mid_y):
                    intermediate = self.create_platform(mid_x, mid_y)
                    self.active_platforms.append(intermediate)
        
        # Fix low density areas
        for platform, density in issues['low_density_areas']:
            needed = self.min_platforms_in_range - density
            for _ in range(needed):
                position = self.find_safe_platform_position(platform.x, platform.y)
                if position:
                    x, y = position
                    new_platform = self.create_platform(x, y)
                    self.active_platforms.append(new_platform)
    
    def select_platform_type(self, height_progress):
        """
        Select platform type based on game progress
        
        Args:
            height_progress (float): Current height/progress in the game
            
        Returns:
            PlatformType: Selected platform type
        """
        import random
        
        # Determine available platform types based on progress
        available_types = [PlatformType.NORMAL]
        
        for height_threshold, new_types in self.type_introduction_heights.items():
            if height_progress >= height_threshold:
                available_types.extend(new_types)
        
        # Decide whether to use special platform
        if len(available_types) > 1 and random.random() < self.special_platform_chance:
            # Choose a special platform type (not normal)
            special_types = [t for t in available_types if t != PlatformType.NORMAL]
            return random.choice(special_types)
        else:
            # Use normal platform
            return PlatformType.NORMAL
    
    def add_safety_platform_for_harmful(self, harmful_x, harmful_y):
        """
        Add a normal platform near a harmful platform to prevent softlocks
        
        Args:
            harmful_x (float): X position of the harmful platform
            harmful_y (float): Y position of the harmful platform
        """
        import random
        
        # Try to place safety platform at same Y level, offset horizontally
        safety_distance = 150  # Distance from harmful platform
        margin = self.platform_width // 2 + 20
        
        # Try both sides of the harmful platform
        for direction in [1, -1]:  # Right first, then left
            safety_x = harmful_x + (direction * safety_distance)
            
            # Keep within screen bounds
            if margin <= safety_x <= WIDTH - margin:
                # Check if position is clear
                if not self.position_overlaps_existing(safety_x, harmful_y):
                    # Create safety platform
                    safety_platform = self.create_platform(safety_x, harmful_y, PlatformType.NORMAL)
                    self.active_platforms.append(safety_platform)
                    return  # Successfully added safety platform
        
        # If same Y level doesn't work, try slightly above or below
        for y_offset in [-40, 40]:  # Try above first, then below
            safety_y = harmful_y + y_offset
            
            # Try both sides again
            for direction in [1, -1]:
                safety_x = harmful_x + (direction * safety_distance)
                
                # Keep within screen bounds
                if margin <= safety_x <= WIDTH - margin:
                    # Check if position is clear
                    if not self.position_overlaps_existing(safety_x, safety_y):
                        # Create safety platform
                        safety_platform = self.create_platform(safety_x, safety_y, PlatformType.NORMAL)
                        self.active_platforms.append(safety_platform)
                        return  # Successfully added safety platform

# Progress Tracking System
class ProgressTracker:
    """
    Tracks player progress and manages milestone-based features
    """
    def __init__(self):
        """
        Initialize progress tracking system
        """
        # Progress metrics
        self.current_height = 0.0  # Current height achieved (negative Y coordinate)
        self.max_height_reached = 0.0  # Maximum height ever reached
        self.score = 0  # Score based on height progression
        
        # Milestone tracking
        self.milestones_reached = set()  # Set of milestone heights reached
        self.milestone_heights = {
            1000: "First Conveyor Platforms",
            2000: "Breakable Platforms Introduced", 
            3000: "Moving Platforms Appear",
            3500: "Vertical Platforms Added",
            3750: "Bouncy Platforms Available",
            4000: "Harmful Platforms - Danger Zone!",
            5000: "Master Climber",
            7500: "Platform Expert", 
            10000: "Sky Walker"
        }
        
        # Score multipliers for different achievements
        self.height_score_multiplier = 1.0  # Points per unit height
        self.milestone_bonus = 100  # Bonus points for reaching milestones
        
        # Statistics
        self.platforms_landed_on = 0
        self.bounces_performed = 0
        self.harmful_platforms_avoided = 0
    
    def update(self, frog, camera):
        """
        Update progress tracking based on current game state
        
        Args:
            frog (Frog): Current frog object
            camera (Camera): Current camera object
        """
        # Calculate current height (negative Y means higher up)
        # Use camera position as reference since it follows the frog upward
        self.current_height = abs(camera.y)  # Convert to positive height value
        
        # Update maximum height reached
        if self.current_height > self.max_height_reached:
            self.max_height_reached = self.current_height
            
        # Update score based on height progression
        self.score = int(self.current_height * self.height_score_multiplier)
        
        # Check for new milestones
        self.check_milestones()
    
    def check_milestones(self):
        """
        Check if any new milestones have been reached
        
        Returns:
            list: List of newly reached milestone descriptions
        """
        new_milestones = []
        
        for milestone_height, description in self.milestone_heights.items():
            if (self.current_height >= milestone_height and 
                milestone_height not in self.milestones_reached):
                
                self.milestones_reached.add(milestone_height)
                self.score += self.milestone_bonus
                new_milestones.append(description)
        
        return new_milestones
    
    def get_progress_percentage(self, target_height=10000):
        """
        Get progress as percentage toward target height
        
        Args:
            target_height (float): Target height for 100% progress
            
        Returns:
            float: Progress percentage (0.0 to 100.0)
        """
        return min(100.0, (self.current_height / target_height) * 100.0)
    
    def get_next_milestone(self):
        """
        Get information about the next milestone to reach
        
        Returns:
            tuple: (height, description) of next milestone, or None if all reached
        """
        for milestone_height in sorted(self.milestone_heights.keys()):
            if milestone_height not in self.milestones_reached:
                return (milestone_height, self.milestone_heights[milestone_height])
        return None
    
    def record_platform_landing(self, platform_type):
        """
        Record that frog landed on a platform
        
        Args:
            platform_type (PlatformType): Type of platform landed on
        """
        self.platforms_landed_on += 1
        
        # Track specific platform interactions
        if platform_type == PlatformType.BOUNCY:
            self.bounces_performed += 1
        elif platform_type == PlatformType.HARMFUL:
            # This shouldn't happen (game over), but track for completeness
            pass
    
    def record_harmful_platform_avoided(self):
        """
        Record that a harmful platform was successfully avoided
        """
        self.harmful_platforms_avoided += 1
        self.score += 50  # Bonus for avoiding danger
    
    def get_statistics(self):
        """
        Get comprehensive progress statistics
        
        Returns:
            dict: Dictionary containing all progress statistics
        """
        return {
            'current_height': self.current_height,
            'max_height_reached': self.max_height_reached,
            'score': self.score,
            'milestones_reached': len(self.milestones_reached),
            'total_milestones': len(self.milestone_heights),
            'platforms_landed_on': self.platforms_landed_on,
            'bounces_performed': self.bounces_performed,
            'harmful_platforms_avoided': self.harmful_platforms_avoided,
            'progress_percentage': self.get_progress_percentage()
        }
    
    def reset(self):
        """
        Reset progress tracking for new game
        """
        self.current_height = 0.0
        self.max_height_reached = 0.0
        self.score = 0
        self.milestones_reached.clear()
        self.platforms_landed_on = 0
        self.bounces_performed = 0
        self.harmful_platforms_avoided = 0

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
progress_tracker = None

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
    global frog, platforms, camera, platform_generator, progress_tracker
    # Initialize camera system
    camera = Camera()
    
    # Initialize platform generator
    platform_generator = PlatformGenerator()
    
    # Initialize progress tracker
    progress_tracker = ProgressTracker()
    
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
    global game_state, progress_tracker
    game_state = GameState.PLAYING
    
    # Reset progress tracker if it exists
    if progress_tracker:
        progress_tracker.reset()
    
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
            
            # Record platform landing for progress tracking
            if frog.last_platform_landed and progress_tracker:
                progress_tracker.record_platform_landing(frog.last_platform_landed)
                frog.last_platform_landed = None  # Reset after recording
            
            # Check if frog touched a harmful platform
            if frog.touched_harmful_platform:
                game_state = GameState.GAME_OVER
        
        # Update camera to follow frog
        if camera and frog:
            camera.update(frog)
            
            # Update progress tracking
            if progress_tracker:
                progress_tracker.update(frog, camera)
            
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
            platform.update(1/60)  # Assume 60 FPS
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
                # Draw platform with type-specific color
                platform_color = platform.get_visual_color()
                screen.draw.filled_rect(screen_rect, platform_color)
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