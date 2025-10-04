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

def run_camera_tests():
    """Run the camera system unit tests"""
    print("Running camera system tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_camera_system.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All camera system tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    print("🐸 Frog Platformer Test Suite")
    print("=" * 60)
    
    collision_success = run_collision_tests()
    print()
    camera_success = run_camera_tests()
    
    print("\n" + "=" * 60)
    if collision_success and camera_success:
        print("🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)