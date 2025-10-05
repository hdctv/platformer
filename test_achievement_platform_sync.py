#!/usr/bin/env python3
"""
Test that achievements sync with platform introductions
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, ProgressTracker, PlatformType, Camera, Frog

def test_platform_unlock_sync():
    """Test that platform types unlock when achievements are earned"""
    generator = PlatformGenerator()
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("Testing platform unlock synchronization...")
    
    # Test early game - only normal platforms
    camera.y = -8000  # Before any achievements
    tracker.update(frog, camera)
    
    platform_types = []
    for _ in range(50):
        platform_type = generator.select_platform_type(8000, tracker)
        platform_types.append(platform_type)
    
    # Should only have normal platforms
    unique_types = set(platform_types)
    assert unique_types == {PlatformType.NORMAL}, f"Expected only normal, got {unique_types}"
    print("✅ Before achievements: Only normal platforms")
    
    # Test after conveyor achievement (10000)
    camera.y = -12000
    tracker.update(frog, camera)
    
    platform_types = []
    for _ in range(100):
        platform_type = generator.select_platform_type(12000, tracker)
        platform_types.append(platform_type)
    
    unique_types = set(platform_types)
    assert PlatformType.NORMAL in unique_types
    assert PlatformType.CONVEYOR in unique_types
    assert PlatformType.BREAKABLE not in unique_types  # Not unlocked yet
    print("✅ After Conveyor Master: Normal + Conveyor platforms")
    
    # Test after multiple achievements (25000)
    camera.y = -28000
    tracker.update(frog, camera)
    
    platform_types = []
    for _ in range(200):
        platform_type = generator.select_platform_type(28000, tracker)
        platform_types.append(platform_type)
    
    unique_types = set(platform_types)
    expected_types = {PlatformType.NORMAL, PlatformType.CONVEYOR, PlatformType.BREAKABLE, 
                     PlatformType.MOVING, PlatformType.VERTICAL}
    
    for expected_type in expected_types:
        assert expected_type in unique_types, f"Missing {expected_type} at height 28000"
    
    # Should not have bouncy or harmful yet
    assert PlatformType.BOUNCY not in unique_types
    assert PlatformType.HARMFUL not in unique_types
    print("✅ After multiple achievements: All unlocked types present")
    
    print("✅ Platform unlock synchronization test passed!")

def test_achievement_descriptions_match_unlocks():
    """Test that achievement descriptions mention platform unlocks"""
    tracker = ProgressTracker()
    
    print("\nTesting achievement descriptions...")
    
    # Check that platform-unlocking achievements mention unlocks
    unlock_achievements = [10000, 15000, 20000, 25000, 30000, 40000]
    
    for height in unlock_achievements:
        description = tracker.milestone_heights[height]
        assert "Unlocked" in description, f"Achievement at {height} should mention unlock: {description}"
    
    print("✅ All platform-unlocking achievements mention unlocks")

def demo_achievement_platform_progression():
    """Demo the synchronized achievement-platform system"""
    print("\n" + "="*60)
    print("🎮 ACHIEVEMENT-PLATFORM SYNCHRONIZATION DEMO")
    print("="*60)
    
    generator = PlatformGenerator()
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    # Test progression at key heights
    test_heights = [8000, 12000, 18000, 28000, 35000, 45000]
    
    for height in test_heights:
        print(f"\n📍 Height: {height}")
        
        # Update progress
        camera.y = -height
        old_milestones = len(tracker.milestones_reached)
        tracker.update(frog, camera)
        new_milestones = len(tracker.milestones_reached)
        
        # Show achievements
        if new_milestones > old_milestones:
            latest_achievement = max(m for m in tracker.milestones_reached if m <= height)
            description = tracker.milestone_heights[latest_achievement]
            print(f"🏆 NEW ACHIEVEMENT: {description}")
        
        # Show available platform types
        platform_counts = {}
        for _ in range(100):
            platform_type = generator.select_platform_type(height, tracker)
            platform_counts[platform_type] = platform_counts.get(platform_type, 0) + 1
        
        print("Available platform types:")
        for platform_type, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percentage = count / 100 * 100
                print(f"  {platform_type.value:10}: {percentage:4.0f}%")
    
    print("\n🎉 Achievement-platform synchronization working perfectly!")
    print("Platform types unlock exactly when achievements are earned!")

if __name__ == '__main__':
    print("Testing Achievement-Platform Synchronization...")
    test_platform_unlock_sync()
    test_achievement_descriptions_match_unlocks()
    
    demo_achievement_platform_progression()
    
    print("\n🎉 All achievement-platform sync tests passed!")