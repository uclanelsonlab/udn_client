#!/usr/bin/env python3
"""
UDN Gateway CLI - Main Entry Point

This is the main entry point for the UDN Gateway API client.
It provides a command-line interface for downloading files and getting participant information.
"""

import sys
import os

# Add the current directory to the Python path so we can import our package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from udn_gateway.cli import main

if __name__ == "__main__":
    main() 