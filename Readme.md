# UDN Gateway API Client

A comprehensive Python client for the Undiagnosed Diseases Network (UDN) Gateway API. This project provides easy-to-use tools for accessing and downloading data from the UDN Gateway.

## Package Structure

The project is organized as a proper Python package:

```
udn_aws_to_dnanexus_copy/
├── udn_gateway/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── client.py            # API client implementation
│   ├── cli.py               # Command-line interface
│   └── utils.py             # Utility functions
├── tests/                    # Test suite
│   ├── __init__.py          # Test package initialization
│   ├── test_sequencing.py   # Sequencing data structure tests
│   ├── test_cli.py          # CLI functionality tests
│   └── run_tests.py         # Test runner
├── udn_gateway_cli.py       # Main CLI entry point
├── setup.py                 # Package installation
├── requirements.txt          # Dependencies
└── README.md               # This file
```

## Features

- **Complete API Coverage**: All UDN Gateway API endpoints are supported
- **Enhanced Error Handling**: Comprehensive error handling with detailed error messages
- **File Download Management**: Automated file downloading with progress tracking
- **Backward Compatibility**: Enhanced scripts maintain compatibility with existing workflows
- **Command Line Interface**: Easy-to-use CLI for common operations
- **Logging**: Detailed logging for debugging and monitoring

## Installation

### Option 1: Install as a Package

```bash
# Install the package in development mode
pip install -e .

# Or install directly from the repository
pip install .
```

### Option 2: Use Directly

## Testing

The project includes a comprehensive test suite to ensure functionality works correctly:

```bash
# Run all tests
python tests/run_tests.py

# Run specific test categories
python tests/run_tests.py sequencing
python tests/run_tests.py cli

# Run individual test files
python tests/test_sequencing.py
python tests/test_cli.py
```

### Test Categories

- **sequencing**: Tests API data structure parsing and file detection
- **cli**: Tests command-line interface functionality and flags

### Prerequisites

- Python 3.6 or higher
- `requests` library
- `curl` command-line tool (for file downloads)

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd udn_aws_to_dnanexus_copy
```

2. Install required Python packages:
```bash
pip install requests
```

3. Get your API token from the UDN Gateway and save it to a file (e.g., `token.txt`)

## Usage

### Quick Start

#### Using the Enhanced Script (Recommended)

```bash
# Download all files for a participant (new simplified way)
python udn_gateway_cli.py -a token.txt -u UDN970218 --all

# Download all files for a participant (legacy way)
python udn_gateway_cli.py -a token.txt -u UDN970218 --download

# Download only .gvcf.gz files
python udn_gateway_cli.py -a token.txt -u UDN970218 --download --gvcf

# Download only .vcf.gz files
python udn_gateway_cli.py -a token.txt -u UDN970218 --download --vcf

# Download files to a specific directory
python udn_gateway_cli.py -a token.txt -u UDN970218 --all -o /path/to/output

# List all available participants
python udn_gateway_cli.py -a token.txt --list-participants

# Get participant information only
python udn_gateway_cli.py -a token.txt -u UDN970218 --info-only
```

#### Using the Original Script

```bash
# Download files for a participant (new package structure)
python udn_gateway_cli.py -a token.txt -u UDN970218 --download
```

#### Using the API Client Directly

```python
from udn_gateway import UDNGatewayClient

# Initialize client
client = UDNGatewayClient("your_api_token_here")

# Get all participants
participants = client.get_participants()

# Get participant details
details = client.get_participant_details("UDN970218")

# Download all files for a participant
downloaded_files = client.download_all_participant_files("UDN970218", "/output/directory")
```

### Command Line Interface

The CLI provides a comprehensive interface with the following options:

```bash
python udn_gateway_cli.py [OPTIONS]
```

#### Options

- `-a, --api_token_file`: API token file (required)
- `-u, --udn_id`: UDN participant ID to download data
- `-o, --output_dir`: Output directory for downloaded files (default: current directory)
- `--file-types`: File types to download (comma-separated: sequencing_file,medical_record,etc.)
- `--list-participants`: List all available participants
- `--info-only`: Only get participant information, don't download files
- `--all`: Download all available files for the participant (new simplified way)
- `--download`: Download files for the participant (legacy way, must be explicitly set)
- `--gvcf`: Only download files ending with .gvcf.gz (must be used with --download)
- `--vcf`: Only download files ending with .vcf.gz (must be used with --download)
- `--verbose`: Enable verbose logging

#### Examples

```bash
# Download all files for a participant (new simplified way)
python udn_gateway_cli.py -a token.txt -u UDN970218 --all

# Download all files for a participant (legacy way)
python udn_gateway_cli.py -a token.txt -u UDN970218 --download

# Download only .gvcf.gz files
python udn_gateway_cli.py -a token.txt -u UDN970218 --download --gvcf

# Download only .vcf.gz files
python udn_gateway_cli.py -a token.txt -u UDN970218 --download --vcf

# Download only sequencing files
python udn_gateway_cli.py -a token.txt -u UDN970218 --all --file-types sequencing_file

# Download files to a specific directory
python udn_gateway_cli.py -a token.txt -u UDN970218 --all -o /path/to/output

# List all available participants
python udn_gateway_cli.py -a token.txt --list-participants

# Get participant information only
python udn_gateway_cli.py -a token.txt -u UDN970218 --info-only

# Enable verbose logging
python udn_gateway_cli.py -a token.txt -u UDN970218 --all --verbose
```

### API Client Usage

The `UDNGatewayClient` class provides methods for all available API endpoints:

#### Applications

```python
# Get all applications
applications = client.get_applications()

# Get applications with specific status
accepted_apps = client.get_applications(filter_status="accepted")

# Get application details
app_details = client.get_application_details(application_id=123)

# Get application attachment details
attachment = client.get_application_attachment_details(123, "letter", 456)
```

#### Participants

```python
# Get all participants
participants = client.get_participants()

# Get participant details
details = client.get_participant_details("UDN970218")

# Get participant family
family = client.get_participant_family("UDN970218")

# Get sequencing requests
sequencing = client.get_participant_sequencing_requests("UDN970218")

# Get PhenoTips data
phenotips = client.get_participant_phenotips("UDN970218")
```

#### File Downloads

```python
# Get all available files for a participant
files = client.get_participant_files_for_download("UDN970218")

# Download a single file
file_path = client.download_file(download_link, filename, output_dir)

# Download all files for a participant
downloaded_files = client.download_all_participant_files("UDN970218", "/output/directory")
```

#### Reference Data

```python
# Get clinical sites
sites = client.get_clinical_sites()

# Get ethnicities
ethnicities = client.get_ethnicities()

# Get languages
languages = client.get_languages()

# Get races
races = client.get_races()

# Get relations
relations = client.get_relations()

# Get sexes
sexes = client.get_sexes()

# Get symptom categories
categories = client.get_symptom_categories()
```

#### Sequencing

```python
# Get sequencing cores
cores = client.get_sequencing_cores()

# Get sequencing requests
requests = client.get_sequencing_requests()

# Get specific sequencing request
request = client.get_sequencing_request_by_id(123)
```

## API Endpoints

The client supports all available UDN Gateway API endpoints:

### Applications
- `GET /applications` - Get applications list
- `GET /applications/{id}` - Get application details
- `GET /applications/{id}/attachments/{type}/{attachmentId}` - Get attachment details
- `GET /applications/{id}/review/attachments/{type}/{attachmentId}` - Get review attachment details

### Participants
- `GET /participants` - Get participants list
- `GET /participants/{participantId}` - Get participant details
- `GET /participants/{participantId}/family` - Get participant family
- `GET /participants/{participantId}/sequencing` - Get sequencing requests
- `GET /participants/{participantId}/sequencing/files/{id}` - Get sequencing file details
- `GET /participants/{participantId}/sequencing/reports/{id}` - Get sequencing report details
- `GET /participants/{participantId}/medicalrecords/{id}` - Get medical record details
- `GET /participants/{participantId}/consentdocuments/{id}` - Get consent document details
- `GET /participants/{participantId}/wrapupdocuments/{id}` - Get wrap-up document details
- `GET /participants/{participantId}/phenotips` - Get PhenoTips data
- `GET /participants/{participantId}/phenotips/suggestedgenepanels` - Get suggested gene panels
- `GET /participants/{participantId}/modelorganism` - Get model organism requests

### Reference Data
- `GET /clinicalsites` - Get clinical sites
- `GET /ethnicities` - Get ethnicities
- `GET /genderidentities` - Get gender identities
- `GET /languages` - Get languages
- `GET /races` - Get races
- `GET /relations` - Get relations
- `GET /sexes` - Get sexes
- `GET /symptomcategories` - Get symptom categories

### Sequencing
- `GET /sequencing/cores` - Get sequencing cores
- `GET /sequencing/requests` - Get sequencing requests
- `GET /sequencing/requests/{id}` - Get sequencing request details

### Families
- `GET /families/{familyId}` - Get family details

## Error Handling

The client provides comprehensive error handling:

```python
from src.udn_api_client import UDNGatewayClient, UDNGatewayAPIError

try:
    client = UDNGatewayClient("your_token")
    participants = client.get_participants()
except UDNGatewayAPIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

Common error codes:
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found

## Logging

The client uses Python's logging module for detailed output:

```python
import logging

# Set logging level
logging.basicConfig(level=logging.INFO)

# Use the client
client = UDNGatewayClient("your_token")
```

## Nextflow Integration

The enhanced script is compatible with the existing Nextflow workflow:

```groovy
process bwa_mem {
    container "gvcn/request_udn_files:v0.0.4"
    cpus 12
    tag "Download UDN gateway data for $udn_id"

    input:
    val udn_id
    val proband_id
    val relative_status
    path api_token_file

    output:
    tuple val(meta), path("*.bwa.bam"), emit: bwa_bam
    
    script:
    """
    python /home/bin/request_udn_files_enhanced.py -a ${api_token_file} -u ${udn_id}
    """
}
```

## Configuration

### API Token

Store your API token in a text file:
```
your_api_token_here
```

### Environment Variables

You can also set the API token as an environment variable:
```bash
export UDN_API_TOKEN="your_api_token_here"
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your API token is correct
   - Check that the token file exists and is readable
   - Ensure the token hasn't expired

2. **Permission Errors**
   - Contact UDN Gateway support for access to specific endpoints
   - Verify your account has the necessary permissions

3. **Download Failures**
   - Check that `curl` is installed and accessible
   - Verify you have write permissions to the output directory
   - Check network connectivity

4. **File Not Found Errors**
   - Verify the participant ID is correct
   - Check that the participant has available files
   - Ensure the file IDs are valid

### Debug Mode

Enable verbose logging for detailed output:
```bash
python src/request_udn_files_enhanced.py -a token.txt -u UDN970218 --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues related to:
- API access and permissions: Contact UDN Gateway support
- Client functionality: Open an issue in this repository
- Documentation: Submit a pull request with improvements

## Changelog

### Version 2.1.0
- Added `--all` parameter for simplified downloading of all available files
- Enhanced CLI usability with more intuitive download options
- Maintained backward compatibility with existing `--download` parameter

### Version 2.0.0
- Added comprehensive UDN Gateway API client
- Enhanced error handling and logging
- Added support for all API endpoints
- Improved file download functionality
- Added command-line interface
- Maintained backward compatibility

### Version 1.0.0
- Initial release with basic file download functionality
