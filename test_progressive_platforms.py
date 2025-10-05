#!/usr/bin/env python3
"""
Test progressive platform type introduction system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, ProgressTracker, PlatformType

def test_basic_progressive_introduction():
    """Test that platform types are introduced progressively"""
    generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    
    print("Testing basic progressive introduction...")
    
    # Early game - should only have normal platforms
    platform_types = []
    for _ in range(20):
        platform_type = generator.select_platform_type(500, progress_tracker)
        platform_types.append(platform_type)
    
    # Should be mostly normal platforms
    normal_count = platform_types.count(PlatformType.NORMAL)
    assert normal_count >= 15, f"Expected mostly normal platforms, got {normal_count}/20"
    
    print("✅ Early game has mostly normal platforms")

def test_progressive_special_platform_increase():
    """Test that special platform frequency increases with progress"""
    generator = PlatformGenerator()
    
    print("\nTesting progressive special platform increase...")
    
    # Test at different heights with progress tracker
    heights = [1000, 3000, 5000, 8000]
    special_percentages = []
    
    for height in heights:
        # Create progress tracker with milestones reached
        progress_tracker = ProgressTracker()
        progress_tracker.current_height = height
        
        # Simulate milestones reached
        for milestone in progress_tracker.milestone_heights:
            if milestone <= height:
                progress_tracker.milestones_reached.add(milestone)
        
        # Generate platforms and count special types
        platform_types = []
        for _ in range(100):
            platform_type = generator.select_platform_type(height, progress_tracker)
            platform_types.append(platform_type)
        
        special_count = len([t for t in platform_types if t != PlatformType.NORMAL])
        special_percentage = special_count / len(platform_types) * 100
        special_percentages.append(special_percentage)
        
        print(f"Height {height}: {special_percentage:.1f}% special platforms")
    
    # Special platform percentage should generally increase with height
    assert special_percentages[1] > special_percentages[0], "Special platforms should increase with height"
    assert special_percentages[2] > special_percentages[1], "Special platforms should continue increasing"
    
    print("✅ Special platform frequency increases with progress")

def test_weighted_platform_selection():
    """Test that platform types have appropriate weights"""
    generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    progress_tracker.current_height = 5000
    
    # Simulate milestones
    for milestone in [1000, 2000, 3000, 3500, 3750, 4000]:
        progress_tracker.milestones_reached.add(milestone)
    
    print("\nTesting weighted platform selection...")
    
    # Generate many platforms to test distribution
    platform_counts = {}
    for _ in range(1000):
        platform_type = generator.select_platform_type(5000, progress_tracker)
        platform_counts[platform_type] = platform_counts.get(platform_type, 0) + 1
    
    print("Platform distribution at height 5000:")
    for platform_type, count in platform_counts.items():
        percentage = count / 1000 * 100
        print(f"  {platform_type.value}: {count} ({percentage:.1f}%)")
    
    # Conveyor should be most common special platform
    if PlatformType.CONVEYOR in platform_counts:
        conveyor_count = platform_counts[PlatformType.CONVEYOR]
        
        # Harmful should be least common
        if PlatformType.HARMFUL in platform_counts:
            harmful_count = platform_counts[PlatformType.HARMFUL]
            assert conveyor_count > harmful_count, "Conveyor should be more common than harmful"
    
    print("✅ Platform weights working correctly")

def test_anti_clustering():
    """Test that anti-clustering prevents too many similar platforms"""
    generator = PlatformGenerator()
    progress_tracker = ProgressTracker()
    progress_tracker.current_height = 4000
    
    print("\nTesting anti-clustering mechanism...")
    
    # Create some platforms of the same type to test clustering prevention
    for _ in range(5):
        platform = generator.create_platform(400, 300, PlatformType.CONVEYOR)
        generator.active_platforms.append(platform)
    
    # Generate new platforms - should avoid conveyor due to clustering
    platform_types = []
    for _ in range(50):
        platform_type = generator.select_platform_type(4000, progress_tracker)
        platform_types.append(platform_type)
    
    conveyor_count = platform_types.count(PlatformType.CONVEYOR)
    total_special = len([t for t in platform_types if t != PlatformType.NORMAL])
    
    if total_special > 0:
        conveyor_percentage = conveyor_count / total_special * 100
        print(f"Conveyor platforms: {conveyor_percentage:.1f}% of special platforms")
        
        # Should be reduced due to recent clustering
        assert conveyor_percentage < 50, "Anti-clustering should reduce conveyor frequency"
    
    print("✅ Anti-clustering mechanism working")

def test_milestone_bonus_effect():
    """Test that reaching milestones increases special platform frequency"""
    generator = PlatformGenerator()
    
    print("\nTesting milestone bonus effect...")
    
    # Test without milestones
    progress_tracker_no_milestones = ProgressTracker()
    progress_tracker_no_milestones.current_height = 3000
    
    platform_types_no_bonus = []
    for _ in range(100):
        platform_type = generator.select_platform_type(3000, progress_tracker_no_milestones)
        platform_types_no_bonus.append(platform_type)
    
    special_count_no_bonus = len([t for t in platform_types_no_bonus if t != PlatformType.NORMAL])
    
    # Test with milestones
    progress_tracker_with_milestones = ProgressTracker()
    progress_tracker_with_milestones.current_height = 3000
    progress_tracker_with_milestones.milestones_reached = {1000, 2000, 3000}
    
    platform_types_with_bonus = []
    for _ in range(100):
        platform_type = generator.select_platform_type(3000, progress_tracker_with_milestones)
        platform_types_with_bonus.append(platform_type)
    
    special_count_with_bonus = len([t for t in platform_types_with_bonus if t != PlatformType.NORMAL])
    
    print(f"Special platforms without milestones: {special_count_no_bonus}")
    print(f"Special platforms with milestones: {special_count_with_bonus}")
    
    # Milestone bonus should increase special platform frequency
    assert special_count_with_bonus >= special_count_no_bonus, "Milestones should increase special platforms"
    
    print("✅ Milestone bonus effect working")

def test_difficulty_progression():
    """Test that difficult platforms become more common at higher heights"""
    generator = PlatformGenerator()
    
    print("\nTesting difficulty progression...")
    
    # Test at low height
    progress_tracker_low = ProgressTracker()
    progress_tracker_low.current_height = 2000
    progress_tracker_low.milestones_reached = {1000, 2000}
    
    difficult_platforms_low = []
    for _ in range(200):
        platform_type = generator.select_platform_type(2000, progress_tracker_low)
        if platform_type in [PlatformType.MOVING, PlatformType.VERTICAL, PlatformType.BOUNCY, PlatformType.HARMFUL]:
            difficult_platforms_low.append(platform_type)
    
    # Test at high height
    progress_tracker_high = ProgressTracker()
    progress_tracker_high.current_height = 8000
    for milestone in progress_tracker_high.milestone_heights:
        if milestone <= 8000:
            progress_tracker_high.milestones_reached.add(milestone)
    
    difficult_platforms_high = []
    for _ in range(200):
        platform_type = generator.select_platform_type(8000, progress_tracker_high)
        if platform_type in [PlatformType.MOVING, PlatformType.VERTICAL, PlatformType.BOUNCY, PlatformType.HARMFUL]:
            difficult_platforms_high.append(platform_type)
    
    print(f"Difficult platforms at height 2000: {len(difficult_platforms_low)}")
    print(f"Difficult platforms at height 8000: {len(difficult_platforms_high)}")
    
    # Should have more difficult platforms at higher heights
    assert len(difficult_platforms_high) >= len(difficult_platforms_low), "Difficult platforms should increase with height"
    
    print("✅ Difficulty progression working")

def demo_progressive_platform_system():
    """Demo the progressive platform introduction system"""
    print("\n" + "="*60)
    print("🎮 PROGRESSIVE PLATFORM INTRODUCTION DEMO")
    print("="*60)
    
    generator = PlatformGenerator()
    
    heights = [500, 1500, 3000, 5000, 7500, 10000]
    
    for height in heights:
        print(f"\n📍 Height: {height}")
        
        # Create progress tracker for this height
        progress_tracker = ProgressTracker()
        progress_tracker.current_height = height
        
        # Add appropriate milestones
        for milestone in progress_tracker.milestone_heights:
            if milestone <= height:
                progress_tracker.milestones_reached.add(milestone)
        
        # Generate sample platforms
        platform_counts = {}
        for _ in range(100):
            platform_type = generator.select_platform_type(height, progress_tracker)
            platform_counts[platform_type] = platform_counts.get(platform_type, 0) + 1
        
        # Display distribution
        print(f"Milestones reached: {len(progress_tracker.milestones_reached)}")
        print("Platform distribution:")
        
        for platform_type in PlatformType:
            count = platform_counts.get(platform_type, 0)
            percentage = count / 100 * 100
            if count > 0:
                print(f"  {platform_type.value:10}: {count:2} ({percentage:4.1f}%)")
        
        special_count = sum(count for ptype, count in platform_counts.items() if ptype != PlatformType.NORMAL)
        print(f"Total special: {special_count}%")
    
    print("\n🎉 Progressive platform system working perfectly!")

if __name__ == '__main__':
    print("Testing Progressive Platform Introduction System...")
    test_basic_progressive_introduction()
    test_progressive_special_platform_increase()
    test_weighted_platform_selection()
    test_anti_clustering()
    test_milestone_bonus_effect()
    test_difficulty_progression()
    
    demo_progressive_platform_system()
    
    print("\n🎉 All progressive platform tests passed!")