#!/usr/bin/env python3
"""
Test script to examine sequencing data structure and file parsing.
"""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import our package
sys.path.insert(0, str(Path(__file__).parent.parent))

from udn_gateway import UDNGatewayClient


def test_sequencing_data_structure():
    """Test to examine the sequencing data structure and file parsing."""
    
    # Read API token
    api_key_file = Path(__file__).parent.parent / "api-key.txt"
    if not api_key_file.exists():
        print("Error: api-key.txt not found. Please ensure it exists in the project root.")
        return
    
    with open(api_key_file, 'r') as f:
        api_token = f.read().strip()

    client = UDNGatewayClient(api_token)

    # Get sequencing data
    print("=== Testing Sequencing Data Structure ===")
    sequencing_data = client.get_participant_sequencing("UDN287643")
    print("Sequencing data structure:")
    print(json.dumps(sequencing_data, indent=2))

    # Check for .gvcf.gz files in the data
    print("\n=== Testing File Parsing ===")
    print("Searching for .gvcf.gz files...")
    all_files = client.get_all_participant_files("UDN287643")
    gvcf_files = [f for f in all_files if f.get('filename', '').endswith('.gvcf.gz')]

    print(f"Total files found: {len(all_files)}")
    print(f"GVCF files found: {len(gvcf_files)}")

    print("\nAll files:")
    for file_info in all_files:
        filename = file_info.get('filename', 'unknown')
        source = file_info.get('source', 'unknown')
        filesize = file_info.get('filesize', 0)
        print(f"  - {filename} (source: {source}, size: {filesize} bytes)")

    print("\nGVCF files:")
    for file_info in gvcf_files:
        filename = file_info.get('filename', 'unknown')
        source = file_info.get('source', 'unknown')
        filesize = file_info.get('filesize', 0)
        print(f"  - {filename} (source: {source}, size: {filesize} bytes)")


def test_api_connection():
    """Test basic API connection and authentication."""
    print("=== Testing API Connection ===")
    
    api_key_file = Path(__file__).parent.parent / "api-key.txt"
    if not api_key_file.exists():
        print("Error: api-key.txt not found.")
        return
    
    with open(api_key_file, 'r') as f:
        api_token = f.read().strip()

    try:
        client = UDNGatewayClient(api_token)
        participant_info = client.get_participant("UDN287643")
        print(f"✅ API connection successful")
        print(f"✅ Participant found: {participant_info.get('nameFirst', '')} {participant_info.get('nameLast', '')}")
        return True
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False


if __name__ == "__main__":
    print("UDN Gateway API Client - Test Suite")
    print("=" * 50)
    
    # Test API connection first
    if test_api_connection():
        # If connection works, test sequencing data
        test_sequencing_data_structure()
    else:
        print("Skipping sequencing tests due to connection failure.") 