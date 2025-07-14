#!/usr/bin/env python3
"""
Test runner for UDN Gateway API Client tests.
"""

import sys
import subprocess
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_test(test_file):
    """Run a specific test file."""
    test_path = Path(__file__).parent / test_file
    if not test_path.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Running test: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([
            sys.executable, str(test_path)
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ {test_file} completed successfully")
            return True
        else:
            print(f"❌ {test_file} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ {test_file} failed with exception: {e}")
        return False


def run_all_tests():
    """Run all available tests."""
    print("UDN Gateway API Client - Full Test Suite")
    print("=" * 60)
    
    # List of test files to run
    test_files = [
        "test_sequencing.py",
        "test_cli.py"
    ]
    
    results = {}
    for test_file in test_files:
        results[test_file] = run_test(test_file)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_file, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_file}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False


def run_specific_test(test_name):
    """Run a specific test by name."""
    if test_name == "sequencing":
        return run_test("test_sequencing.py")
    elif test_name == "cli":
        return run_test("test_cli.py")
    else:
        print(f"❌ Unknown test: {test_name}")
        print("Available tests: sequencing, cli")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
        sys.exit(0 if success else 1)
    else:
        # Run all tests
        success = run_all_tests()
        sys.exit(0 if success else 1) 