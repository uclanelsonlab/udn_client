"""
UDN Gateway API Package

A comprehensive Python package for interacting with the Undiagnosed Diseases Network (UDN) Gateway API.
"""

__version__ = "2.0.0"
__author__ = "UDN Gateway API Client"
__description__ = "Python client for the UDN Gateway API"

from .client import UDNGatewayClient, UDNGatewayAPIError
from .cli import main as cli_main

__all__ = [
    "UDNGatewayClient",
    "UDNGatewayAPIError", 
    "cli_main"
] 