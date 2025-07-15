#!/usr/bin/env python3
"""
Test script for CLI functionality.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the parent directory to the path so we can import our package
sys.path.insert(0, str(Path(__file__).parent.parent))

from udn_gateway.cli import main
import argparse


def test_cli_help():
    """Test that CLI help works correctly."""
    print("=== Testing CLI Help ===")
    
    try:
        # Test the main CLI script
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "udn_gateway_cli.py"),
            "--help"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ CLI help works correctly")
            print("Help output preview:")
            print(result.stdout[:500] + "...")
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ CLI help test failed: {e}")


def test_cli_argument_parsing():
    """Test CLI argument parsing."""
    print("\n=== Testing CLI Argument Parsing ===")
    
    # Test that required arguments are enforced
    try:
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "udn_gateway_cli.py")
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("✅ CLI correctly enforces required arguments")
        else:
            print("❌ CLI should require arguments")
            
    except Exception as e:
        print(f"❌ CLI argument test failed: {e}")


def test_gvcf_flag_logic():
    """Test the --gvcf flag logic."""
    print("\n=== Testing --gvcf Flag Logic ===")
    
    # Test that --gvcf without --download shows info but doesn't download
    api_key_file = Path(__file__).parent.parent / "api-key.txt"
    if not api_key_file.exists():
        print("❌ api-key.txt not found, skipping gvcf test")
        return
    
    try:
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "udn_gateway_cli.py"),
            "-a", str(api_key_file),
            "-u", "UDN287643",
            "--gvcf"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            if "Found" in output and "gvcf" in output.lower():
                print("✅ --gvcf flag works correctly (shows info without downloading)")
            else:
                print("❌ --gvcf flag output unexpected")
        else:
            print(f"❌ --gvcf test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ --gvcf test failed: {e}")


def test_info_only_flag():
    """Test the --info-only flag."""
    print("\n=== Testing --info-only Flag ===")
    
    api_key_file = Path(__file__).parent.parent / "api-key.txt"
    if not api_key_file.exists():
        print("❌ api-key.txt not found, skipping info-only test")
        return
    
    try:
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "udn_gateway_cli.py"),
            "-a", str(api_key_file),
            "-u", "UDN287643",
            "--info-only"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            if "Info-only mode" in output and "not downloading" in output:
                print("✅ --info-only flag works correctly")
            else:
                print("❌ --info-only flag output unexpected")
        else:
            print(f"❌ --info-only test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ --info-only test failed: {e}")


if __name__ == "__main__":
    print("UDN Gateway CLI - Test Suite")
    print("=" * 50)
    
    test_cli_help()
    test_cli_argument_parsing()
    test_gvcf_flag_logic()
    test_info_only_flag()
    
    print("\n" + "=" * 50)
    print("CLI Test Suite Complete") 