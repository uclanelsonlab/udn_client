#!/usr/bin/env python3
"""
UDN Gateway CLI

Command-line interface for the UDN Gateway API client.
Provides easy-to-use commands for common operations.
"""

import os
import sys
import json
import argparse
from typing import List, Optional, Callable
import logging

from .client import UDNGatewayClient, UDNGatewayAPIError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def download_participant_files(client: UDNGatewayClient, udn_id: str, 
                              output_dir: str = ".", file_types: Optional[List[str]] = None,
                              file_filter: Optional[Callable] = None) -> List[str]:
    """
    Download all available files for a participant.
    
    Args:
        client (UDNGatewayClient): API client instance
        udn_id (str): UDN ID of the participant
        output_dir (str): Directory to save files in
        file_types (list, optional): List of file types to download
        file_filter (callable, optional): Function to filter files before downloading
        
    Returns:
        list: List of successfully downloaded file paths
    """
    downloaded_files = []
    
    try:
        # Get all files for the participant
        files = client.get_all_participant_files(udn_id)
        
        if not files:
            logger.warning(f"No files found for participant {udn_id}")
            return downloaded_files
        
        logger.info(f"Found {len(files)} files for participant {udn_id}")
        
        # Filter by file types if specified
        if file_types:
            files = [f for f in files if f.get('source') in file_types]
            logger.info(f"Filtered to {len(files)} files of specified types")
        
        # Before downloading, filter files if file_filter is provided
        if file_filter is not None:
            files = [f for f in files if file_filter(f)]
            logger.info(f"Filtered to {len(files)} files after applying filter")
        
        # Download each file
        for file_info in files:
            filename = file_info.get('filename', 'unknown')
            file_url = file_info.get('url')
            
            if not file_url:
                logger.warning(f"No download URL for file: {filename}")
                continue
            
            # Create output path
            output_path = os.path.join(output_dir, filename)
            
            # Skip if file already exists
            if os.path.exists(output_path):
                logger.info(f"File already exists, skipping: {output_path}")
                downloaded_files.append(output_path)
                continue
            
            # Download the file
            logger.info(f"Downloading: {filename}")
            if client.download_file(file_url, output_path):
                downloaded_files.append(output_path)
            else:
                logger.error(f"Failed to download: {filename}")
        
        logger.info(f"Successfully downloaded {len(downloaded_files)} files")
        
    except Exception as e:
        logger.error(f"Error downloading files for {udn_id}: {e}")
    
    return downloaded_files


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="UDN Gateway API Client - Download files and get participant information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get participant info only
  python -m udn_gateway.cli -a api-key.txt -u UDN287643 --info-only
  
  # Download all files
  python -m udn_gateway.cli -a api-key.txt -u UDN287643 --download
  
  # Download only .gvcf.gz files
  python -m udn_gateway.cli -a api-key.txt -u UDN287643 --download --gvcf
  
  # List all participants
  python -m udn_gateway.cli -a api-key.txt --list-participants
        """
    )
    
    parser.add_argument("-a", "--api-token-file", required=True,
                       help="File containing the API token")
    parser.add_argument("-u", "--udn-id", 
                       help="UDN ID of the participant")
    parser.add_argument("-o", "--output-dir", default=".",
                       help="Output directory for downloaded files (default: current directory)")
    parser.add_argument("--file-types", nargs="+",
                       help="Specific file types to download (sequencing_file, medical_record, etc.)")
    parser.add_argument("--list-participants", 
                       help="List all available participants", 
                       action="store_true")
    parser.add_argument('--info-only', action='store_true', 
                       help='Print participant info only (default behavior if --download is not specified)')
    parser.add_argument('--download', action='store_true', 
                       help='Download files for the participant (must be explicitly set)')
    parser.add_argument('--gvcf', action='store_true', 
                       help='Only download files ending with .gvcf.gz (must be used with --download)')
    parser.add_argument("--verbose", 
                       help="Enable verbose logging", 
                       action="store_true")
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate inputs
    api_token_file = os.path.abspath(args.api_token_file)
    output_dir = args.output_dir
    
    logger.info(f"API token file: {api_token_file}")
    logger.info(f"Output directory: {output_dir}")
    
    # Check if API token file exists
    if not os.path.exists(api_token_file):
        logger.error(f"API token file not found: {api_token_file}")
        sys.exit(1)
    
    # Read API token
    try:
        with open(api_token_file, 'r') as f:
            api_token = f.read().strip()
    except Exception as e:
        logger.error(f"Error reading API token file: {e}")
        sys.exit(1)
    
    # Initialize client
    try:
        client = UDNGatewayClient(api_token)
        logger.info("Successfully initialized UDN Gateway API client")
    except Exception as e:
        logger.error(f"Failed to initialize client: {e}")
        sys.exit(1)
    
    # Handle list participants
    if args.list_participants:
        try:
            participants = client.get_participants()
            print(json.dumps(participants, indent=2))
        except UDNGatewayAPIError as e:
            logger.error(f"Failed to get participants: {e}")
            sys.exit(1)
        return
    
    # Validate UDN ID is provided for other operations
    if not args.udn_id:
        logger.error("UDN ID is required for participant operations")
        sys.exit(1)
    
    udn_id = str(args.udn_id)
    logger.info(f"UDN ID: {udn_id}")
    
    # Get participant information
    try:
        participant_info = client.get_participant(udn_id)
        logger.info(f"Participant: {participant_info.get('nameFirst', '')} {participant_info.get('nameLast', '')}")
    except UDNGatewayAPIError as e:
        logger.error(f"Failed to get participant information: {e}")
        sys.exit(1)
    
    # Print participant info
    print(json.dumps(participant_info, indent=2))
    
    # If --info-only is set, exit after printing info
    if args.info_only:
        logger.info('Info-only mode: not downloading any files.')
        return
    
    # If --download is not set, warn and exit
    if not args.download:
        logger.warning('No action taken. Use --download to download files, or --info-only to print info.')
        return
    
    # If --download is set, proceed to download files
    # If --gvcf is set, filter files to only .gvcf.gz
    file_types = args.file_types
    
    if args.gvcf:
        logger.info('Filtering to only .gvcf.gz files for download.')
        def gvcf_filter(fileinfo):
            return fileinfo.get('filename', '').endswith('.gvcf.gz')
        downloaded_files = download_participant_files(client, udn_id, output_dir, file_types, file_filter=gvcf_filter)
    else:
        downloaded_files = download_participant_files(client, udn_id, output_dir, file_types)
    
    if downloaded_files:
        logger.info(f"Downloaded {len(downloaded_files)} files to {output_dir}")
    else:
        logger.warning("No files were downloaded")


if __name__ == "__main__":
    main() 