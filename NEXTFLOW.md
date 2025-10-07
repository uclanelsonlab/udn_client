# UDN Gateway Client Pipeline

A Nextflow pipeline for downloading and processing data from the UDN Gateway API.

## Quick Start

### Prerequisites

- Nextflow (>= 22.10.0)
- Python 3.9+
- Docker or Singularity (optional, for containerized execution)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd udn_client
```

2. Install Nextflow (if not already installed):
```bash
curl -s https://get.nextflow.io | bash
```

3. Make the pipeline runner executable:
```bash
chmod +x bin/run_pipeline.sh
```

### Basic Usage

```bash
# Download all files for a participant
./bin/run_pipeline.sh --api_token_file token.txt --udn_id UDN970218

# Download only VCF files
./bin/run_pipeline.sh --api_token_file token.txt --udn_id UDN970218 --download_vcf

# Download to specific directory
./bin/run_pipeline.sh --api_token_file token.txt --udn_id UDN970218 --output_dir /data/udn
```

### Direct Nextflow Usage

```bash
# Download all files
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218

# Download only VCF files
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 --download_vcf

# Run with specific profile
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile slurm
```

## Pipeline Parameters

### Required Parameters
- `--api_token_file`: Path to file containing API token
- `--udn_id`: UDN participant ID

### Optional Parameters
- `--output_dir`: Output directory (default: ./results)
- `--download_all`: Download all available files (default: true)
- `--download_vcf`: Download only VCF files
- `--download_gvcf`: Download only GVCF files
- `--file_types`: Specific file types to download
- `--verbose`: Enable verbose logging
- `--process_sequencing`: Process sequencing files (default: true)
- `--generate_reports`: Generate processing reports (default: true)

## Execution Profiles

### Local Execution
```bash
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile local
```

### SLURM Cluster
```bash
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile slurm
```

### AWS Batch
```bash
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile awsbatch
```

### Docker
```bash
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile docker
```

### Singularity
```bash
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile singularity
```

## Pipeline Structure

```
udn_client/
├── main.nf                    # Main pipeline script
├── nextflow.config            # Pipeline configuration
├── modules/
│   ├── download_participant_data.nf
│   ├── process_sequencing_files.nf
│   └── generate_report.nf
├── bin/
│   ├── run_pipeline.sh       # Pipeline runner script
│   ├── build_docker.sh       # Docker build script
│   ├── setup.py              # Package setup
│   └── udn_gateway_cli.py    # CLI entry point
├── container/
│   ├── Dockerfile            # Docker image definition
│   ├── docker-compose.yml    # Docker Compose setup
│   └── DOCKER.md            # Docker documentation
├── udn_gateway/              # Python package
├── tests/                     # Test suite
└── README.md                 # Documentation
```

## Output Structure

```
results/
├── UDN970218/                # Participant-specific directory
│   ├── *.vcf.gz             # Downloaded VCF files
│   ├── *.gvcf.gz            # Downloaded GVCF files
│   ├── *.bam                # Downloaded BAM files
│   └── processed/           # Processed files
├── reports/                  # Generated reports
│   ├── execution_report.html
│   ├── execution_timeline.html
│   ├── execution_trace.txt
│   ├── pipeline_dag.svg
│   ├── processing_report.html
│   └── processing_report.json
└── logs/                     # Pipeline logs
    └── download_UDN970218.log
```

## Troubleshooting

### Common Issues

1. **Nextflow not found**
   - Install Nextflow: `curl -s https://get.nextflow.io | bash`
   - Add to PATH: `export PATH=$PATH:$PWD`

2. **API token issues**
   - Verify token file exists and is readable
   - Check token validity with UDN Gateway

3. **Permission errors**
   - Ensure write permissions to output directory
   - Check file system quotas

4. **Container issues**
   - Verify Docker/Singularity installation
   - Check container registry access

### Debug Mode

Enable verbose logging:
```bash
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 --verbose
```

### Logs

Pipeline logs are available in:
- `results/logs/` - Download and processing logs
- `results/reports/` - Execution reports and traces

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
