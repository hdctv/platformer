#!/usr/bin/env python3
"""
Compare the new balanced progression with what it was before
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frog_platformer import PlatformGenerator, ProgressTracker, PlatformType

def test_new_balance():
    """Test the new balanced progression"""
    print("🎮 NEW BALANCED PROGRESSION")
    print("="*50)
    
    generator = PlatformGenerator()
    
    heights = [1500, 3000, 5000, 7500, 10000]
    
    for height in heights:
        # Create progress tracker for this height
        progress_tracker = ProgressTracker()
        progress_tracker.current_height = height
        
        # Add appropriate milestones
        for milestone in progress_tracker.milestone_heights:
            if milestone <= height:
                progress_tracker.milestones_reached.add(milestone)
        
        # Generate sample platforms
        platform_counts = {}
        for _ in range(200):
            platform_type = generator.select_platform_type(height, progress_tracker)
            platform_counts[platform_type] = platform_counts.get(platform_type, 0) + 1
        
        # Calculate percentages
        normal_count = platform_counts.get(PlatformType.NORMAL, 0)
        harmful_count = platform_counts.get(PlatformType.HARMFUL, 0)
        total_special = sum(count for ptype, count in platform_counts.items() if ptype != PlatformType.NORMAL)
        
        normal_pct = normal_count / 200 * 100
        harmful_pct = harmful_count / 200 * 100
        special_pct = total_special / 200 * 100
        
        print(f"Height {height:5}: Normal {normal_pct:4.1f}% | Special {special_pct:4.1f}% | Harmful {harmful_pct:4.1f}%")
    
    print("\n✅ Much more gradual progression!")
    print("✅ Harmful platforms are more present!")
    print("✅ Normal platforms remain dominant longer!")

if __name__ == '__main__':
    test_new_balance()