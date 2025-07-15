#!/usr/bin/env python3
"""
UDN Gateway API Client

A comprehensive Python client for the Undiagnosed Diseases Network (UDN) Gateway API.
This client provides easy-to-use methods for accessing all available API endpoints.

Author: Generated based on UDN Gateway API documentation
Version: 2.0.0
"""

import os
import sys
import json
import requests
import argparse
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UDNGatewayAPIError(Exception):
    """Custom exception for UDN Gateway API errors"""
    pass


class UDNGatewayClient:
    """
    Client for the UDN Gateway API.
    
    This client provides methods to interact with all available endpoints
    of the UDN Gateway API, including participant information, sequencing data,
    and file downloads.
    """
    
    def __init__(self, api_token: str, base_url: str = "https://gateway.undiagnosed.hms.harvard.edu/api/2.0"):
        """
        Initialize the UDN Gateway API client.
        
        Args:
            api_token (str): Your API token for authentication
            base_url (str): Base URL for the API (defaults to v2.0)
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_token}'
        })
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the UDN Gateway API.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters
            data (dict, optional): Request body data
            
        Returns:
            dict: JSON response from the API
            
        Raises:
            UDNGatewayAPIError: If the request fails
        """
        # Construct URL explicitly to ensure /api/2.0 is included
        if endpoint.startswith('/'):
            url = f"{self.base_url}{endpoint}"
        else:
            url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )
            
            # Log request details for debugging
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Response Status: {response.status_code}")
            logger.debug(f"Response Headers: {dict(response.headers)}")
            logger.debug(f"Response Content: {response.text[:500]}...")
            
            response.raise_for_status()
            
            # Check if response is empty
            if not response.text.strip():
                raise UDNGatewayAPIError("Empty response from API")
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise UDNGatewayAPIError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise UDNGatewayAPIError(f"Failed to parse JSON response: {e}")
    
    def get_participants(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a list of all participants.
        
        Args:
            limit (int, optional): Maximum number of participants to return
            offset (int, optional): Number of participants to skip
            
        Returns:
            dict: List of participants
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        return self._make_request('GET', '/participants', params=params)
    
    def get_participant(self, udn_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific participant.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            dict: Participant information
        """
        return self._make_request('GET', f'/participants/{udn_id}')
    
    def get_participant_sequencing(self, udn_id: str) -> Dict[str, Any]:
        """
        Get sequencing information for a specific participant.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            dict: Sequencing information
        """
        return self._make_request('GET', f'/participants/{udn_id}/sequencing')
    
    def get_participant_sequencing_file_details(self, udn_id: str, file_id: int) -> Dict[str, Any]:
        """
        Get details of a specific sequencing file including download link.
        
        Args:
            udn_id (str): The UDN ID of the participant
            file_id (int): The ID of the sequencing file
            
        Returns:
            dict: File details including download link
        """
        return self._make_request('GET', f'/participants/{udn_id}/sequencing/files/{file_id}')
    
    def get_participant_medical_records(self, udn_id: str) -> Dict[str, Any]:
        """
        Get medical records for a specific participant.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            dict: Medical records information
        """
        return self._make_request('GET', f'/participants/{udn_id}/medical_records')
    
    def get_participant_consents(self, udn_id: str) -> Dict[str, Any]:
        """
        Get consent information for a specific participant.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            dict: Consent information
        """
        return self._make_request('GET', f'/participants/{udn_id}/consents')
    
    def get_participant_evaluation(self, udn_id: str) -> Dict[str, Any]:
        """
        Get evaluation information for a specific participant.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            dict: Evaluation information
        """
        return self._make_request('GET', f'/participants/{udn_id}/evaluation')
    
    def get_participant_wrapup_documents(self, udn_id: str) -> Dict[str, Any]:
        """
        Get wrapup documents for a specific participant.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            dict: Wrapup documents information
        """
        return self._make_request('GET', f'/participants/{udn_id}/wrapup_documents')
    
    def get_reference_data(self, data_type: str) -> Dict[str, Any]:
        """
        Get reference data for various types.
        
        Args:
            data_type (str): Type of reference data (e.g., 'clinical_sites', 'states', etc.)
            
        Returns:
            dict: Reference data
        """
        return self._make_request('GET', f'/reference_data/{data_type}')
    
    def download_file(self, file_url: str, output_path: str) -> bool:
        """
        Download a file from the UDN Gateway.
        
        Args:
            file_url (str): URL of the file to download
            output_path (str): Local path where to save the file
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            # Use curl for downloads as it handles large files better
            import subprocess
            result = subprocess.run([
                'curl', '-L', '-o', output_path, file_url
            ], capture_output=True, text=True, timeout=3600)  # 1 hour timeout
            
            if result.returncode == 0:
                logger.info(f"Successfully downloaded: {output_path}")
                return True
            else:
                logger.error(f"Download failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Download timed out for: {output_path}")
            return False
        except Exception as e:
            logger.error(f"Download error: {e}")
            return False
    
    def get_all_participant_files(self, udn_id: str) -> List[Dict[str, Any]]:
        """
        Get all available files for a participant from all sources.
        
        Args:
            udn_id (str): The UDN ID of the participant
            
        Returns:
            list: List of file information dictionaries
        """
        all_files = []
        
        # Get sequencing files
        try:
            sequencing_data = self.get_participant_sequencing(udn_id)
            if 'requests' in sequencing_data:
                for request in sequencing_data['requests']:
                    if 'files' in request:
                        for file_info in request['files']:
                            file_info['source'] = 'sequencing'
                            # Try to get download URL for sequencing files
                            try:
                                file_id = file_info.get('id')
                                if file_id:
                                    file_details = self.get_participant_sequencing_file_details(udn_id, file_id)
                                    if 'url' in file_details:
                                        file_info['url'] = file_details['url']
                                    elif 'downloadUrl' in file_details:
                                        file_info['url'] = file_details['downloadUrl']
                                    elif 'downloadLink' in file_details:
                                        file_info['url'] = file_details['downloadLink']
                            except Exception as e:
                                logger.debug(f"Could not get download URL for file {file_info.get('filename', 'unknown')}: {e}")
                            all_files.append(file_info)
            logger.debug(f"Found {len([f for f in all_files if f['source'] == 'sequencing'])} sequencing files")
        except Exception as e:
            logger.debug(f"Could not get sequencing files for {udn_id}: {e}")
        
        # Get medical records
        try:
            medical_data = self.get_participant_medical_records(udn_id)
            if 'medical_records' in medical_data:
                for file_info in medical_data['medical_records']:
                    file_info['source'] = 'medical_record'
                    all_files.append(file_info)
            logger.debug(f"Found {len([f for f in all_files if f['source'] == 'medical_record'])} medical record files")
        except Exception as e:
            logger.debug(f"Could not get medical records for {udn_id}: {e}")
        
        # Get consents
        try:
            consents_data = self.get_participant_consents(udn_id)
            if 'consents' in consents_data:
                for consent in consents_data['consents']:
                    if 'documents' in consent:
                        for file_info in consent['documents']:
                            file_info['source'] = 'consent'
                            all_files.append(file_info)
            logger.debug(f"Found {len([f for f in all_files if f['source'] == 'consent'])} consent files")
        except Exception as e:
            logger.debug(f"Could not get consent files for {udn_id}: {e}")
        
        # Get wrapup documents
        try:
            wrapup_data = self.get_participant_wrapup_documents(udn_id)
            if 'wrapup_documents' in wrapup_data:
                for file_info in wrapup_data['wrapup_documents']:
                    file_info['source'] = 'wrapup_document'
                    all_files.append(file_info)
            logger.debug(f"Found {len([f for f in all_files if f['source'] == 'wrapup_document'])} wrapup document files")
        except Exception as e:
            logger.debug(f"Could not get wrapup documents for {udn_id}: {e}")
        
        return all_files 