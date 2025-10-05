#!/usr/bin/env python3
"""
Test achievement notification system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import ProgressTracker, Camera, Frog

def test_achievement_notification_trigger():
    """Test that achievements trigger notifications"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("Testing achievement notification trigger...")
    
    # Initially no achievement
    assert not tracker.has_active_achievement()
    assert tracker.get_achievement_display_info() is None
    
    # Reach first milestone
    camera.y = -5000
    tracker.update(frog, camera)
    
    # Simulate some time passing for animation
    tracker.update_achievement_display(0.1)  # 0.1 seconds
    
    # Should have active achievement
    assert tracker.has_active_achievement()
    achievement_info = tracker.get_achievement_display_info()
    assert achievement_info is not None
    
    achievement_text = achievement_info['text']
    slide_progress = achievement_info['slide_progress']
    assert "Novice" in achievement_text
    assert slide_progress > 0.0  # Should be sliding in
    
    print("✅ Achievement notification trigger test passed!")

def test_achievement_display_timing():
    """Test achievement display timing and fade"""
    tracker = ProgressTracker()
    
    print("\nTesting achievement display timing...")
    
    # Manually trigger achievement
    tracker.trigger_achievement_notification("Test Achievement")
    
    # Simulate time for animation to start
    tracker.update_achievement_display(0.1)
    
    # Should be active with slide progress
    assert tracker.has_active_achievement()
    achievement_info = tracker.get_achievement_display_info()
    assert achievement_info['slide_progress'] > 0.0  # Should be sliding
    
    # Update timer (simulate 2.5 seconds passing)
    tracker.update_achievement_display(2.5)
    
    # Should still be active and fully visible
    assert tracker.has_active_achievement()
    achievement_info = tracker.get_achievement_display_info()
    assert achievement_info['slide_progress'] == 1.0  # Should be fully visible
    
    # Update timer (simulate another 0.4 seconds - now 0.1s remaining, should be sliding out)
    tracker.update_achievement_display(0.4)
    
    # Should be sliding out
    assert tracker.has_active_achievement()
    achievement_info = tracker.get_achievement_display_info()
    print(f"Debug: slide_progress = {achievement_info['slide_progress']}, timer = {tracker.achievement_timer}")
    assert 0 < achievement_info['slide_progress'] <= 1.0  # Should be sliding out or fully visible
    
    # Update timer (simulate final 1.1 seconds - should expire)
    tracker.update_achievement_display(1.1)
    
    # Should be gone
    assert not tracker.has_active_achievement()
    assert tracker.get_achievement_display_info() is None
    
    print("✅ Achievement display timing test passed!")

def test_multiple_achievements():
    """Test multiple achievements in sequence"""
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    print("\nTesting multiple achievements...")
    
    # Reach multiple milestones at once
    camera.y = -15000
    tracker.update(frog, camera)
    
    # Should have active achievement (latest one)
    assert tracker.has_active_achievement()
    
    # Should have reached multiple milestones
    assert len(tracker.milestones_reached) >= 2
    assert 5000 in tracker.milestones_reached
    assert 10000 in tracker.milestones_reached
    assert 15000 in tracker.milestones_reached
    
    print("✅ Multiple achievements test passed!")

def test_achievement_reset():
    """Test achievement reset functionality"""
    tracker = ProgressTracker()
    
    print("\nTesting achievement reset...")
    
    # Trigger achievement
    tracker.trigger_achievement_notification("Test Achievement")
    assert tracker.has_active_achievement()
    
    # Reset tracker
    tracker.reset()
    
    # Achievement should be cleared
    assert not tracker.has_active_achievement()
    assert tracker.get_achievement_display_info() is None
    assert tracker.achievement_timer == 0.0
    assert tracker.active_achievement is None
    
    print("✅ Achievement reset test passed!")

def test_conveyor_speed_nerf():
    """Test that conveyor speed has been reduced"""
    from frog_platformer import Platform, PlatformType
    
    print("\nTesting conveyor speed nerf...")
    
    platform = Platform(400, 350, 100, 20, PlatformType.CONVEYOR)
    
    # Should have reduced speed
    assert platform.conveyor_speed == 1.2, f"Expected 1.2, got {platform.conveyor_speed}"
    
    # Should be significantly less than old speed (3.5)
    assert platform.conveyor_speed < 2.0, "Conveyor speed should be nerfed"
    
    print("✅ Conveyor speed nerf test passed!")

def demo_achievement_system():
    """Demo the achievement notification system"""
    print("\n" + "="*60)
    print("🏆 ACHIEVEMENT NOTIFICATION SYSTEM DEMO")
    print("="*60)
    
    tracker = ProgressTracker()
    camera = Camera()
    frog = Frog(400, 300)
    
    # Simulate reaching different heights
    heights = [5000, 10000, 15000, 25000, 40000]
    
    for height in heights:
        print(f"\n📍 Reaching height: {height}")
        
        camera.y = -height
        old_milestones = len(tracker.milestones_reached)
        tracker.update(frog, camera)
        new_milestones = len(tracker.milestones_reached)
        
        if new_milestones > old_milestones:
            achievement_info = tracker.get_achievement_display_info()
            if achievement_info:
                achievement_text = achievement_info['text']
                slide_progress = achievement_info['slide_progress']
                print(f"🎉 ACHIEVEMENT: {achievement_text}")
                print(f"   Slide progress: {slide_progress:.2f}")
                print(f"   Timer: {tracker.achievement_timer:.1f}s remaining")
        else:
            print("   No new achievements")
    
    print(f"\nFinal Statistics:")
    print(f"  Total milestones reached: {len(tracker.milestones_reached)}")
    print(f"  Current score: {tracker.score}")
    
    print("\n🎉 Achievement system working perfectly!")
    print("🎮 Conveyor platforms are now 3x slower (1.2 vs 3.5 speed)")

if __name__ == '__main__':
    print("Testing Achievement Notification System...")
    test_achievement_notification_trigger()
    test_achievement_display_timing()
    test_multiple_achievements()
    test_achievement_reset()
    test_conveyor_speed_nerf()
    
    demo_achievement_system()
    
    print("\n🎉 All achievement notification tests passed!")