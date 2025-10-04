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

def run_game_over_tests():
    """Run the game over system unit tests"""
    print("Running game over system tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_game_over.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All game over system tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_platform_generator_tests():
    """Run the platform generator unit tests"""
    print("Running platform generator tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_platform_generator.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All platform generator tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_platform_cleanup_tests():
    """Run the platform cleanup system unit tests"""
    print("Running platform cleanup tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_platform_cleanup.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All platform cleanup tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_platform_reachability_tests():
    """Run the platform reachability validation unit tests"""
    print("Running platform reachability tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_platform_reachability.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All platform reachability tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_platform_types_tests():
    """Run the platform types and behaviors unit tests"""
    print("Running platform types tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_platform_types.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All platform types tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_harmful_platform_tests():
    """Run the harmful platform mechanics unit tests"""
    print("Running harmful platform tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "test_harmful_platforms.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All harmful platform tests passed!")
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
    print()
    game_over_success = run_game_over_tests()
    print()
    platform_gen_success = run_platform_generator_tests()
    print()
    platform_cleanup_success = run_platform_cleanup_tests()
    print()
    platform_reachability_success = run_platform_reachability_tests()
    print()
    platform_types_success = run_platform_types_tests()
    print()
    harmful_platform_success = run_harmful_platform_tests()
    
    print("\n" + "=" * 60)
    all_success = (collision_success and camera_success and game_over_success and 
                   platform_gen_success and platform_cleanup_success and platform_reachability_success and
                   platform_types_success and harmful_platform_success)
    
    if all_success:
        print("🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)