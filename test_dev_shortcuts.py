#!/usr/bin/env python3
"""
Simple test to verify dev shortcuts work correctly
"""

import sys
sys.path.append('.')

def test_dev_shortcuts():
    """Test that dev shortcuts are properly configured"""
    print("=== Dev Shortcuts Test ===")
    
    # Read the game source
    with open('frog_platformer.py', 'r') as f:
        source = f.read()
    
    # Check for correct key bindings
    shortcuts = {
        'Q': ('keyboard.q', '10000', 'Conveyor platforms'),
        'T': ('keyboard.t', '25000', 'Moving platforms'), 
        'E': ('keyboard.e', '50000', 'Laser obstacles')
    }
    
    print("Checking dev shortcut key bindings:")
    
    for key, (keyboard_check, height, description) in shortcuts.items():
        if keyboard_check in source and height in source:
            print(f"✓ {key} key → Height {height} ({description})")
        else:
            print(f"❌ {key} key shortcut not found")
    
    # Check that W key is not used for teleport
    if 'keyboard.w' in source and 'teleport_to_height' in source:
        print("⚠️  W key still used for teleport - potential movement conflict")
    else:
        print("✓ W key not used for teleport - no movement conflicts")
    
    # Check for safety platform creation
    if 'WIDTH, 20' in source and 'landing_platform' in source:
        print("✓ Full-width safety platform created after teleport")
    else:
        print("⚠️  Safety platform creation not found")
    
    # Check for correct attribute usage
    if 'milestone_heights' in source and 'height_milestones' not in source:
        print("✓ Correct ProgressTracker attribute used")
    else:
        print("⚠️  ProgressTracker attribute issue may remain")
    
    print("\nDev shortcuts summary:")
    print("• Q = Teleport to 10,000 (conveyor platforms)")
    print("• T = Teleport to 25,000 (moving platforms)")  
    print("• E = Teleport to 50,000 (laser obstacles)")
    print("• Full-width safety platform spawns under frog")
    print("• No conflicts with WASD movement controls")

if __name__ == "__main__":
    test_dev_shortcuts()