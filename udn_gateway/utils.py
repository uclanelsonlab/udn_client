"""
UDN Gateway Utilities

Utility functions for the UDN Gateway API client.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_udn_id(udn_id: str) -> bool:
    """
    Validate UDN ID format.
    
    Args:
        udn_id (str): UDN ID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not udn_id:
        return False
    
    # UDN IDs typically start with "UDN" followed by numbers
    if not udn_id.startswith("UDN"):
        return False
    
    # Check if the rest is numeric
    try:
        int(udn_id[3:])
        return True
    except ValueError:
        return False


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (str): Directory path to ensure exists
        
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def save_json_data(data: Dict[str, Any], filepath: str) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data (dict): Data to save
        filepath (str): Path to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON file {filepath}: {e}")
        return False


def load_json_data(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        dict or None: Loaded data or None if failed
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON file {filepath}: {e}")
        return None


def filter_files_by_extension(files: List[Dict[str, Any]], extension: str) -> List[Dict[str, Any]]:
    """
    Filter files by file extension.
    
    Args:
        files (list): List of file dictionaries
        extension (str): File extension to filter by (e.g., '.gvcf.gz')
        
    Returns:
        list: Filtered list of files
    """
    return [f for f in files if f.get('filename', '').endswith(extension)]


def get_file_info_summary(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get a summary of file information.
    
    Args:
        files (list): List of file dictionaries
        
    Returns:
        dict: Summary information about the files
    """
    if not files:
        return {"total_files": 0, "total_size": 0, "file_types": {}}
    
    total_size = sum(f.get('size', 0) for f in files)
    file_types = {}
    
    for file_info in files:
        filename = file_info.get('filename', '')
        file_type = file_info.get('source', 'unknown')
        
        if file_type not in file_types:
            file_types[file_type] = {
                'count': 0,
                'total_size': 0,
                'files': []
            }
        
        file_types[file_type]['count'] += 1
        file_types[file_type]['total_size'] += file_info.get('size', 0)
        file_types[file_type]['files'].append(filename)
    
    return {
        "total_files": len(files),
        "total_size": total_size,
        "total_size_formatted": format_file_size(total_size),
        "file_types": file_types
    }


def create_download_report(downloaded_files: List[str], failed_files: List[str], 
                          output_dir: str) -> str:
    """
    Create a download report.
    
    Args:
        downloaded_files (list): List of successfully downloaded files
        failed_files (list): List of files that failed to download
        output_dir (str): Output directory where files were saved
        
    Returns:
        str: Path to the report file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"download_report_{timestamp}.json")
    
    report = {
        "timestamp": timestamp,
        "output_directory": output_dir,
        "summary": {
            "total_downloaded": len(downloaded_files),
            "total_failed": len(failed_files),
            "success_rate": len(downloaded_files) / (len(downloaded_files) + len(failed_files)) if (len(downloaded_files) + len(failed_files)) > 0 else 0
        },
        "downloaded_files": downloaded_files,
        "failed_files": failed_files
    }
    
    if save_json_data(report, report_file):
        logger.info(f"Download report saved to: {report_file}")
        return report_file
    else:
        logger.error("Failed to save download report")
        return ""


def format_timestamp(timestamp_ms: int) -> str:
    """
    Format a millisecond timestamp to a readable date string.
    
    Args:
        timestamp_ms (int): Timestamp in milliseconds
        
    Returns:
        str: Formatted date string
    """
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return "Unknown" 