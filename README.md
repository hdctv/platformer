# 🐸 Frog Platformer

A vertical scrolling platformer game where you control a frog character climbing ever upward through randomly generated platforms. Built with Python and Pygame Zero.

![Game Screenshot](screenshot.png)

## 🎮 How to Play

### Controls
- **SPACE** or **UP ARROW** - Jump
- **LEFT/RIGHT ARROWS** or **A/D** - Move horizontally
- **ESC** - Quit game
- **M** - Show memory statistics (debug)

### Objective
Climb as high as possible by jumping between platforms! The higher you go, the more challenging it becomes with new platform types and mechanics.

## 🏗️ Platform Types

The game features **6 different platform types** that are progressively introduced as you climb higher:

### 🟤 Normal Platforms
- **Introduced**: From the start
- **Behavior**: Solid, reliable platforms you can stand on
- **Strategy**: Your safe havens - use them to plan your next moves

### 🔄 Conveyor Platforms (Height 1000+)
- **Introduced**: Height 1000
- **Color**: Gray
- **Behavior**: Push you sideways while you're on them
- **Direction**: Alternates left/right based on position
- **Speed**: 1.2 pixels/frame (balanced for gameplay)
- **Strategy**: Use the push to reach distant platforms, but be careful not to get pushed off edges!

### 🧡 Breakable Platforms (Height 2000+)
- **Introduced**: Height 2000
- **Color**: Orange (flashes when about to break)
- **Behavior**: Break after 1 second when stepped on
- **Strategy**: Quick thinking required - don't linger!

### 🟣 Moving Platforms (Height 3000+)
- **Introduced**: Height 3000
- **Color**: Purple
- **Behavior**: Move horizontally back and forth
- **Strategy**: Time your jumps and ride them to new areas

### 🔵 Vertical Platforms (Height 3500+)
- **Introduced**: Height 3500
- **Color**: Cyan
- **Behavior**: Move up and down, carrying you with them
- **Strategy**: Use them as elevators to reach higher areas quickly

### 🩷 Bouncy Platforms (Height 3750+)
- **Introduced**: Height 3750
- **Color**: Pink
- **Behavior**: Launch you upward with **double jump height**
- **Risk/Reward**: Can't stand still - immediately become airborne
- **Strategy**: High-risk, high-reward - can skip sections but less control

### 🔴 Harmful Platforms (Height 4000+)
- **Introduced**: Height 4000
- **Color**: Red
- **Behavior**: **Game over** on contact!
- **Frequency**: Becomes more common at very high heights
- **Strategy**: Avoid at all costs - plan your route carefully

## 🏆 Achievement System

Unlock achievements as you reach new heights! Each milestone unlocks new platform types and provides bonus points:

- **🎯 Height 1000**: "First Conveyor Platforms" - Conveyor platforms introduced
- **🎯 Height 2000**: "Breakable Platforms Introduced" - Breakable platforms appear
- **🎯 Height 3000**: "Moving Platforms Appear" - Moving platforms added
- **🎯 Height 3500**: "Vertical Platforms Added" - Vertical platforms introduced
- **🎯 Height 3750**: "Bouncy Platforms Available" - Bouncy platforms unlocked
- **🎯 Height 4000**: "Harmful Platforms - Danger Zone!" - Harmful platforms appear
- **🎯 Height 5000**: "Master Climber" - You're getting good!
- **🎯 Height 7500**: "Platform Expert" - Mastery level reached
- **🎯 Height 10000**: "Sky Walker" - Ultimate achievement!

**Achievement notifications** appear on screen with gold borders and trophy emojis when unlocked!

## 📊 Progressive Difficulty

The game features a sophisticated **progressive difficulty system**:

### Platform Introduction
- New platform types are introduced at specific heights
- **Gradual progression** - normal platforms remain dominant even at high heights
- **Balanced distribution** - special platforms cap at ~50% frequency

### Dynamic Frequency
- **Base chance**: 20% for special platforms
- **Progressive scaling**: Increases slowly with height
- **Milestone bonuses**: +2% per achievement unlocked
- **Maximum frequency**: Capped at 60% to maintain balance

### Intelligent Generation
- **Weighted selection**: Helpful platforms (conveyors) more common than dangerous ones
- **Anti-clustering**: Prevents too many similar platforms in a row
- **Difficulty scaling**: Challenging platforms become more frequent at extreme heights

## 🎯 Scoring System

- **Height-based scoring**: 1 point per unit climbed
- **Milestone bonuses**: 100 points per achievement
- **Danger bonuses**: Extra points for avoiding harmful platforms
- **Statistics tracking**: Platforms landed on, bounces performed, etc.

## 🎨 Visual Features

- **Distinct platform colors** for easy identification
- **Achievement notifications** with fade effects
- **Real-time height display** showing your progress
- **Debug information** (press M for memory stats)
- **Smooth camera following** that tracks your upward progress

## 🛠️ Technical Features

### Advanced Physics
- **Realistic gravity** and jump mechanics
- **Platform-specific behaviors** (conveyor push, bouncy launch, etc.)
- **Collision detection** with proper edge cases
- **Momentum preservation** for smooth gameplay

### Smart Generation
- **Infinite vertical generation** - platforms created as you climb
- **Reachability validation** - ensures no impossible jumps
- **Memory management** - old platforms cleaned up automatically
- **Performance optimization** - efficient platform reuse system

### Progress Tracking
- **Comprehensive statistics** tracking all player actions
- **Milestone system** with visual feedback
- **Score calculation** with multiple bonus types
- **Achievement persistence** throughout game session

## 🚀 Installation & Running

### Prerequisites
- Python 3.7+
- Pygame Zero

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd frog-platformer

# Install dependencies
pip install pgzero

# Run the game
pgzrun frog_platformer.py
```

### Optional: Virtual Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pgzero

# Run the game
pgzrun frog_platformer.py
```

## 🧪 Testing

The game includes comprehensive test suites:

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python test_platform_types.py      # Platform mechanics
python test_progress_tracking.py   # Progress system
python test_achievement_notifications.py  # Achievement system
python test_progressive_platforms.py      # Difficulty progression
```

## 🎮 Gameplay Tips

### Beginner Tips
1. **Master the basics** - Practice jumping and movement on normal platforms first
2. **Plan ahead** - Look for your next landing spot before jumping
3. **Use conveyors wisely** - They can help you reach distant platforms
4. **Don't panic on breakable platforms** - You have a full second to jump

### Advanced Strategies
1. **Bouncy platform chains** - Use multiple bouncy platforms for rapid ascent
2. **Conveyor momentum** - Combine conveyor push with your movement for longer jumps
3. **Vertical platform timing** - Wait for the right moment to maximize height gain
4. **Risk assessment** - Sometimes it's worth taking a dangerous route for better positioning

### Expert Techniques
1. **Speed running** - Use bouncy platforms and conveyors for maximum efficiency
2. **Harmful platform navigation** - Learn to identify and avoid red platforms quickly
3. **Platform type prediction** - Understand the progression system to anticipate what's coming
4. **Score optimization** - Balance height gain with achievement collection

## 🏗️ Development

### Architecture
- **Modular design** with separate classes for each game component
- **Event-driven system** for platform interactions
- **Configurable parameters** for easy gameplay tuning
- **Comprehensive testing** with 100+ test cases

### Key Components
- **Frog**: Player character with physics and state management
- **Platform**: Base class with type-specific behaviors
- **PlatformGenerator**: Intelligent platform creation and management
- **Camera**: Smooth scrolling and coordinate conversion
- **ProgressTracker**: Achievement and statistics system

## 📈 Game Statistics

Current implementation includes:
- **6 platform types** with unique mechanics
- **9 achievement milestones** with visual feedback
- **Progressive difficulty** with intelligent scaling
- **100+ unit tests** ensuring quality
- **Comprehensive documentation** for maintainability

## 🤝 Contributing

This game was built as a learning project demonstrating:
- Game development with Python/Pygame Zero
- Object-oriented design patterns
- Test-driven development
- Progressive difficulty systems
- Achievement and progression mechanics

## 📝 License

This project is open source and available under the MIT License.

---

**Have fun climbing! 🐸⬆️**

*Can you reach the ultimate height of 10,000 and become a Sky Walker?*