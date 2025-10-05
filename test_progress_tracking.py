#!/usr/bin/env python3
"""
Test progress tracking system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import ProgressTracker, Camera, Frog, PlatformType

def test_progress_tracker_initialization():
    """Test that progress tracker initializes correctly"""
    tracker = ProgressTracker()
    
    print("Testing progress tracker initialization...")
    assert tracker.current_height == 0.0
    assert tracker.max_height_reached == 0.0
    assert tracker.score == 0
    assert len(tracker.milestones_reached) == 0
    assert tracker.platforms_landed_on == 0
    assert tracker.bounces_performed == 0
    print("✅ Progress tracker initialization test passed!")

def test_height_tracking():
    """Test height tracking based on camera position"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("\nTesting height tracking...")
    
    # Simulate frog moving upward (camera.y becomes negative)
    camera.y = -500  # Frog has climbed 500 units
    tracker.update(frog, camera)
    
    assert tracker.current_height == 500
    assert tracker.max_height_reached == 500
    assert tracker.score == 500  # 1.0 multiplier
    
    # Simulate more progress
    camera.y = -1200  # Frog has climbed 1200 units
    tracker.update(frog, camera)
    
    assert tracker.current_height == 1200
    assert tracker.max_height_reached == 1200
    # Score should be 1200 (no milestone bonus since first milestone is at 5000)
    assert tracker.score == 1200
    
    print("✅ Height tracking test passed!")

def test_milestone_detection():
    """Test milestone detection and scoring"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("\nTesting milestone detection...")
    
    # Test first milestone at height 5000
    camera.y = -5000
    tracker.update(frog, camera)
    
    assert 5000 in tracker.milestones_reached
    assert tracker.score == 5000 + 100  # Height + milestone bonus
    
    # Test multiple milestones - jump directly to 15000 to trigger multiple milestones
    tracker2 = ProgressTracker()  # Fresh tracker
    camera2 = Camera()
    camera2.y = -15000  # Should trigger 5000, 10000, and 15000 milestones
    tracker2.update(frog, camera2)
    
    assert 5000 in tracker2.milestones_reached
    assert 10000 in tracker2.milestones_reached
    assert 15000 in tracker2.milestones_reached
    # Score should be 15000 + 300 (three milestone bonuses)
    assert tracker2.score == 15000 + 300
    
    print("✅ Milestone detection test passed!")

def test_platform_landing_tracking():
    """Test platform landing statistics"""
    tracker = ProgressTracker()
    
    print("\nTesting platform landing tracking...")
    
    # Test normal platform landing
    tracker.record_platform_landing(PlatformType.NORMAL)
    assert tracker.platforms_landed_on == 1
    assert tracker.bounces_performed == 0
    
    # Test bouncy platform landing
    tracker.record_platform_landing(PlatformType.BOUNCY)
    assert tracker.platforms_landed_on == 2
    assert tracker.bounces_performed == 1
    
    # Test multiple bounces
    tracker.record_platform_landing(PlatformType.BOUNCY)
    tracker.record_platform_landing(PlatformType.BOUNCY)
    assert tracker.platforms_landed_on == 4
    assert tracker.bounces_performed == 3
    
    print("✅ Platform landing tracking test passed!")

def test_progress_percentage():
    """Test progress percentage calculation"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("\nTesting progress percentage...")
    
    # Test 25% progress
    camera.y = -2500  # 25% of default 10000 target
    tracker.update(frog, camera)
    
    progress = tracker.get_progress_percentage()
    assert progress == 25.0
    
    # Test 100% progress
    camera.y = -10000
    tracker.update(frog, camera)
    
    progress = tracker.get_progress_percentage()
    assert progress == 100.0
    
    # Test over 100% (should cap at 100)
    camera.y = -15000
    tracker.update(frog, camera)
    
    progress = tracker.get_progress_percentage()
    assert progress == 100.0
    
    print("✅ Progress percentage test passed!")

def test_next_milestone():
    """Test next milestone detection"""
    tracker = ProgressTracker()
    
    print("\nTesting next milestone detection...")
    
    # Initially, first milestone should be 5000
    next_milestone = tracker.get_next_milestone()
    assert next_milestone[0] == 5000
    assert "Novice" in next_milestone[1]
    
    # After reaching 5000, next should be 10000
    tracker.milestones_reached.add(5000)
    next_milestone = tracker.get_next_milestone()
    assert next_milestone[0] == 10000
    assert "Master" in next_milestone[1]
    
    print("✅ Next milestone test passed!")

def test_statistics_summary():
    """Test comprehensive statistics"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("\nTesting statistics summary...")
    
    # Set up some progress
    camera.y = -8000
    tracker.update(frog, camera)
    tracker.record_platform_landing(PlatformType.NORMAL)
    tracker.record_platform_landing(PlatformType.BOUNCY)
    tracker.record_harmful_platform_avoided()
    
    stats = tracker.get_statistics()
    
    assert stats['current_height'] == 8000
    assert stats['max_height_reached'] == 8000
    assert stats['score'] > 8000  # Should include bonuses
    assert stats['milestones_reached'] >= 1  # Should have reached 5000
    assert stats['platforms_landed_on'] == 2
    assert stats['bounces_performed'] == 1
    assert stats['harmful_platforms_avoided'] == 1
    assert stats['progress_percentage'] == 80.0  # 8000/10000 = 80%
    
    print("✅ Statistics summary test passed!")

def test_reset_functionality():
    """Test progress tracker reset"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("\nTesting reset functionality...")
    
    # Set up some progress
    camera.y = -5000
    tracker.update(frog, camera)
    tracker.record_platform_landing(PlatformType.BOUNCY)
    tracker.record_harmful_platform_avoided()
    
    # Verify progress exists
    assert tracker.current_height > 0
    assert tracker.score > 0
    assert len(tracker.milestones_reached) > 0
    
    # Reset and verify everything is cleared
    tracker.reset()
    
    assert tracker.current_height == 0.0
    assert tracker.max_height_reached == 0.0
    assert tracker.score == 0
    assert len(tracker.milestones_reached) == 0
    assert tracker.platforms_landed_on == 0
    assert tracker.bounces_performed == 0
    assert tracker.harmful_platforms_avoided == 0
    
    print("✅ Reset functionality test passed!")

def demo_progress_tracking():
    """Demo the progress tracking system"""
    print("\n" + "="*50)
    print("🎯 PROGRESS TRACKING SYSTEM DEMO")
    print("="*50)
    
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    # Simulate a game session
    heights = [0, 2000, 5000, 10000, 15000, 25000]
    
    for height in heights:
        camera.y = -height
        tracker.update(frog, camera)
        
        print(f"\nHeight: {height}")
        print(f"Score: {tracker.score}")
        print(f"Progress: {tracker.get_progress_percentage():.1f}%")
        
        # Check for new milestones
        new_milestones = tracker.check_milestones()
        if new_milestones:
            for milestone in new_milestones:
                print(f"🎉 Milestone reached: {milestone}")
        
        # Simulate some platform landings
        if height >= 1000:
            tracker.record_platform_landing(PlatformType.CONVEYOR)
        if height >= 3750:
            tracker.record_platform_landing(PlatformType.BOUNCY)
    
    print(f"\nFinal Statistics:")
    stats = tracker.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n🎉 Progress tracking system working perfectly!")

if __name__ == '__main__':
    print("Testing Progress Tracking System...")
    test_progress_tracker_initialization()
    test_height_tracking()
    test_milestone_detection()
    test_platform_landing_tracking()
    test_progress_percentage()
    test_next_milestone()
    test_statistics_summary()
    test_reset_functionality()
    
    demo_progress_tracking()
    
    print("\n🎉 All progress tracking tests passed!")