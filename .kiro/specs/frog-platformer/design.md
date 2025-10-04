# Design Document

## Overview

The Frog Platformer is a vertical scrolling platformer built with Pygame Zero that challenges players to continuously climb upward by jumping between randomly generated platforms. The game features a physics-based frog character, automatic upward scrolling, and progressively introduced platform types that add complexity and challenge.

## Architecture

### Core Game Loop
- **Main Game State**: Handles the primary gameplay loop including player input, physics updates, collision detection, and rendering
- **Platform Generation**: Continuously generates new platforms above the visible area as the screen scrolls
- **Scroll Management**: Manages upward screen scrolling and removes off-screen elements
- **Progress Tracking**: Monitors player height and determines when to introduce new platform types

### Pygame Zero Integration
- Utilizes Pygame Zero's built-in game loop with `update()` and `draw()` functions
- Leverages Pygame Zero's Actor system for game objects (frog, platforms)
- Uses Pygame Zero's input handling for responsive controls
- Implements custom collision detection suitable for platformer mechanics

## Components and Interfaces

### Frog Character (Player)
```python
class Frog:
    - position (x, y)
    - velocity (vx, vy)
    - on_ground: boolean
    - sprite: Actor
    
    Methods:
    - update(): Handle physics, input, and state
    - jump(): Apply upward velocity
    - move_horizontal(direction): Apply horizontal movement
    - check_platform_collision(platforms): Handle landing on platforms
```

### Platform System
```python
class Platform:
    - position (x, y)
    - width, height
    - platform_type: PlatformType enum
    - sprite: Actor
    - active: boolean (for breakable platforms)
    
    Methods:
    - update(): Handle platform-specific behavior
    - on_collision(frog): Handle frog landing events

class PlatformGenerator:
    - current_height: float
    - platform_spacing: dict
    - type_probabilities: dict
    
    Methods:
    - generate_platforms(target_height): Create new platforms
    - get_platform_type(height): Determine type based on progress
    - ensure_playability(): Verify platforms are reachable
```

### Platform Types
- **Normal**: Standard solid platforms
- **Slippery**: Reduced friction, frog slides more
- **Breakable**: Disappears after being stepped on (with delay)
- **Moving**: Moves horizontally back and forth
- **Harmful**: Causes damage/game over on contact

### Game Manager
```python
class GameManager:
    - camera_y: float (current scroll position)
    - scroll_speed: float
    - score: int (based on height reached)
    - game_state: GameState enum
    
    Methods:
    - update_scroll(): Move camera upward
    - cleanup_platforms(): Remove off-screen platforms
    - check_game_over(): Detect if frog fell off screen
    - update_progress_milestones(): Introduce new platform types
```

## Data Models

### Game State
```python
class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

class PlatformType(Enum):
    NORMAL = "normal"
    SLIPPERY = "slippery"
    BREAKABLE = "breakable"
    MOVING = "moving"
    HARMFUL = "harmful"
```

### Configuration
```python
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
```

## Physics System

### Frog Physics
- **Gravity**: Constant downward acceleration (0.5 pixels/frame²)
- **Jump Mechanics**: Initial upward velocity of -12 pixels/frame
- **Horizontal Movement**: 3 pixels/frame base speed
- **Friction**: Different values for normal vs slippery platforms
- **Collision Detection**: AABB (Axis-Aligned Bounding Box) for platform landings

### Platform Behaviors
- **Moving Platforms**: Sinusoidal or linear horizontal movement
- **Breakable Platforms**: Timer-based destruction after contact
- **Slippery Platforms**: Modified friction coefficient (0.1 vs 0.8)

## Rendering System

### Camera System
- **World Coordinates**: Absolute positions for all game objects
- **Screen Coordinates**: Relative to current camera position
- **Coordinate Conversion**: `screen_y = world_y - camera_y`

### Visual Elements
- **Frog Sprite**: Animated character with jump/land states
- **Platform Sprites**: Distinct visuals for each platform type
  - Normal: Green/brown solid appearance
  - Slippery: Blue/icy appearance
  - Breakable: Cracked/fragile appearance
  - Moving: Mechanical/gear appearance
  - Harmful: Red/spiky appearance
- **Background**: Scrolling or static background elements
- **UI Elements**: Score display, progress indicators

## Error Handling

### Platform Generation Safety
- **Gap Validation**: Ensure no impossible jumps are created
- **Minimum Platform Density**: Guarantee sufficient platforms in each screen section
- **Boundary Checks**: Keep platforms within reasonable horizontal bounds

### Physics Edge Cases
- **High Velocity Handling**: Prevent tunneling through platforms
- **Stuck Detection**: Handle cases where frog gets stuck in geometry
- **Floating Point Precision**: Round positions to prevent accumulation errors

### Game State Management
- **Graceful Degradation**: Handle missing sprites or assets
- **Input Validation**: Sanitize all player inputs
- **Memory Management**: Clean up off-screen objects to prevent memory leaks

## Testing Strategy

### Unit Testing
- **Physics Calculations**: Verify gravity, jump, and collision math
- **Platform Generation**: Test random generation produces valid layouts
- **Game State Transitions**: Ensure proper state management

### Integration Testing
- **Frog-Platform Interactions**: Test all platform type behaviors
- **Scroll System**: Verify camera movement and object cleanup
- **Progress System**: Test platform type introduction timing

### Gameplay Testing
- **Difficulty Progression**: Ensure game remains challenging but fair
- **Control Responsiveness**: Verify input handling feels smooth
- **Performance**: Test with large numbers of platforms

### Visual Testing
- **Sprite Rendering**: Ensure all visual elements display correctly
- **Animation Timing**: Verify smooth character and platform animations
- **UI Layout**: Test score and game state displays