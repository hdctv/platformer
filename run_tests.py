#!/usr/bin/env python3
"""
Test runner for Frog Platformer collision detection tests
"""

import subprocess
import sys

def run_collision_tests():
    """Run the collision detection unit tests"""
    print("Running collision detection tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_collision_detection.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All collision detection tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_collision_tests()
    sys.exit(0 if success else 1)