#!/usr/bin/env nextflow

/*
 * UDN Gateway Client Pipeline
 * 
 * A Nextflow pipeline for downloading and processing data from the UDN Gateway API.
 * This pipeline provides a scalable and reproducible way to download participant data.
 * 
 * @author UDN Gateway Client Team
 * @version 2.1.0
 */

nextflow.enable.dsl=2

// Import required modules
include { downloadParticipantData } from './modules/download_participant_data'
include { processSequencingFiles } from './modules/process_sequencing_files'
include { generateReport } from './modules/generate_report'

// Pipeline parameters
params {
    // Required parameters
    api_token_file = null
    udn_id = null
    
    // Optional parameters
    output_dir = './results'
    download_all = true
    download_vcf = false
    download_gvcf = false
    file_types = null
    verbose = false
    
    // Processing options
    process_sequencing = true
    generate_reports = true
    
    // Help
    help = false
}

// Show help information
if (params.help) {
    log.info """
    UDN Gateway Client Pipeline
    ==========================
    
    Usage:
        nextflow run main.nf --api_token_file <token_file> --udn_id <udn_id> [options]
    
    Required parameters:
        --api_token_file    Path to file containing API token
        --udn_id           UDN participant ID
    
    Optional parameters:
        --output_dir        Output directory (default: ./results)
        --download_all      Download all available files (default: true)
        --download_vcf      Download only VCF files
        --download_gvcf     Download only GVCF files
        --file_types        Specific file types to download
        --verbose           Enable verbose logging
        --process_sequencing Process sequencing files (default: true)
        --generate_reports  Generate processing reports (default: true)
    
    Examples:
        # Download all files for a participant
        nextflow run main.nf --api_token_file token.txt --udn_id UDN970218
        
        # Download only VCF files
        nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 --download_vcf
        
        # Download to specific directory
        nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 --output_dir /data/udn
        
        # Run with verbose logging
        nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 --verbose
    """
    exit 0
}

// Validate required parameters
if (!params.api_token_file) {
    error "API token file is required. Use --api_token_file parameter."
}

if (!params.udn_id) {
    error "UDN ID is required. Use --udn_id parameter."
}

// Create output directory
workflow {
    // Create output directory structure
    Channel.fromPath(params.output_dir).map { dir ->
        [
            participant_dir: "${dir}/${params.udn_id}",
            reports_dir: "${dir}/reports",
            logs_dir: "${dir}/logs"
        ]
    }.set { output_dirs }
    
    // Main workflow
    main:
    
    // Download participant data
    downloadParticipantData(
        params.api_token_file,
        params.udn_id,
        output_dirs,
        params.download_all,
        params.download_vcf,
        params.download_gvcf,
        params.file_types,
        params.verbose
    )
    
    // Process sequencing files if requested
    if (params.process_sequencing) {
        processSequencingFiles(
            downloadParticipantData.out.downloaded_files,
            output_dirs
        )
    }
    
    // Generate reports if requested
    if (params.generate_reports) {
        generateReport(
            downloadParticipantData.out.participant_info,
            downloadParticipantData.out.downloaded_files,
            output_dirs
        )
    }
    
    // Print summary
    downloadParticipantData.out.participant_info
        .map { info ->
            """
            Pipeline Summary
            ================
            Participant: ${info.nameFirst} ${info.nameLast} (${params.udn_id})
            Files downloaded: ${downloadParticipantData.out.downloaded_files.count()}
            Output directory: ${params.output_dir}
            """
        }
        .view { summary -> log.info summary }
}

// Workflow completion
workflow.onComplete {
    log.info """
    Pipeline completed successfully!
    
    Results:
    - Participant data downloaded to: ${params.output_dir}/${params.udn_id}
    - Reports generated in: ${params.output_dir}/reports
    - Logs available in: ${params.output_dir}/logs
    
    Next steps:
    - Review downloaded files
    - Check processing reports
    - Validate data integrity
    """
}

// Workflow error handling
workflow.onError {
    log.error """
    Pipeline failed with error: ${workflow.errorMessage}
    
    Troubleshooting:
    - Check API token validity
    - Verify UDN ID exists
    - Ensure sufficient disk space
    - Check network connectivity
    """
    exit 1
}
