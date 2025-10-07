#!/bin/bash

# UDN Gateway Client Pipeline Runner
# This script provides a convenient way to run the Nextflow pipeline

set -e

# Default values
PROFILE="local"
OUTPUT_DIR="./results"
VERBOSE=false
HELP=false

# Function to show usage
show_usage() {
    cat << EOF
UDN Gateway Client Pipeline Runner
=================================

Usage: $0 [OPTIONS] --api_token_file <token_file> --udn_id <udn_id>

Required parameters:
    --api_token_file    Path to file containing API token
    --udn_id           UDN participant ID

Optional parameters:
    --profile           Execution profile (local, slurm, awsbatch, docker, singularity) [default: local]
    --output_dir        Output directory [default: ./results]
    --download_all      Download all available files [default: true]
    --download_vcf      Download only VCF files
    --download_gvcf     Download only GVCF files
    --file_types        Specific file types to download
    --verbose           Enable verbose logging
    --process_sequencing Process sequencing files [default: true]
    --generate_reports  Generate processing reports [default: true]
    --help              Show this help message

Examples:
    # Download all files for a participant
    $0 --api_token_file token.txt --udn_id UDN970218
    
    # Download only VCF files using SLURM
    $0 --api_token_file token.txt --udn_id UDN970218 --download_vcf --profile slurm
    
    # Download to specific directory with verbose logging
    $0 --api_token_file token.txt --udn_id UDN970218 --output_dir /data/udn --verbose
    
    # Run with Docker
    $0 --api_token_file token.txt --udn_id UDN970218 --profile docker

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --api_token_file)
            API_TOKEN_FILE="$2"
            shift 2
            ;;
        --udn_id)
            UDN_ID="$2"
            shift 2
            ;;
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --output_dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --download_all)
            DOWNLOAD_ALL="true"
            shift
            ;;
        --download_vcf)
            DOWNLOAD_VCF="true"
            shift
            ;;
        --download_gvcf)
            DOWNLOAD_GVCF="true"
            shift
            ;;
        --file_types)
            FILE_TYPES="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE="true"
            shift
            ;;
        --process_sequencing)
            PROCESS_SEQUENCING="true"
            shift
            ;;
        --generate_reports)
            GENERATE_REPORTS="true"
            shift
            ;;
        --help)
            HELP=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Show help if requested
if [ "$HELP" = true ]; then
    show_usage
    exit 0
fi

# Validate required parameters
if [ -z "$API_TOKEN_FILE" ]; then
    echo "Error: API token file is required"
    show_usage
    exit 1
fi

if [ -z "$UDN_ID" ]; then
    echo "Error: UDN ID is required"
    show_usage
    exit 1
fi

# Check if API token file exists
if [ ! -f "$API_TOKEN_FILE" ]; then
    echo "Error: API token file not found: $API_TOKEN_FILE"
    exit 1
fi

# Check if Nextflow is available
if ! command -v nextflow &> /dev/null; then
    echo "Error: Nextflow is not installed or not in PATH"
    echo "Please install Nextflow: https://www.nextflow.io/docs/latest/getstarted.html"
    exit 1
fi

# Build Nextflow command
NEXTFLOW_CMD="nextflow run main.nf"
NEXTFLOW_CMD="$NEXTFLOW_CMD --api_token_file $API_TOKEN_FILE"
NEXTFLOW_CMD="$NEXTFLOW_CMD --udn_id $UDN_ID"
NEXTFLOW_CMD="$NEXTFLOW_CMD --output_dir $OUTPUT_DIR"
NEXTFLOW_CMD="$NEXTFLOW_CMD -profile $PROFILE"

# Add optional parameters
if [ "$DOWNLOAD_ALL" = "true" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --download_all"
fi

if [ "$DOWNLOAD_VCF" = "true" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --download_vcf"
fi

if [ "$DOWNLOAD_GVCF" = "true" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --download_gvcf"
fi

if [ -n "$FILE_TYPES" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --file_types $FILE_TYPES"
fi

if [ "$VERBOSE" = "true" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --verbose"
fi

if [ "$PROCESS_SEQUENCING" = "true" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --process_sequencing"
fi

if [ "$GENERATE_REPORTS" = "true" ]; then
    NEXTFLOW_CMD="$NEXTFLOW_CMD --generate_reports"
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Print command and run
echo "Running UDN Gateway Client Pipeline..."
echo "Command: $NEXTFLOW_CMD"
echo "Output directory: $OUTPUT_DIR"
echo "Profile: $PROFILE"
echo ""

# Run the pipeline
eval $NEXTFLOW_CMD

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "Pipeline completed successfully!"
    echo "Results are available in: $OUTPUT_DIR"
    echo "Reports are available in: $OUTPUT_DIR/reports"
else
    echo ""
    echo "Pipeline failed with errors."
    echo "Check the logs in: $OUTPUT_DIR/logs"
    exit 1
fi
