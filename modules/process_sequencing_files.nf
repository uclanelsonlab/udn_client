process processSequencingFiles {
    tag "${file_name}"
    label 'process'
    
    container 'udn-gateway-client:latest'
    
    cpus 4
    memory '8.GB'
    time '2.h'
    
    input:
    path downloaded_files
    val output_dirs
    
    output:
    path "processed_files.txt", emit: processed_files
    path "processing_log.txt", emit: processing_log
    path "file_stats.json", emit: file_stats
    
    script:
    """
    # Create processing directory
    mkdir -p ${output_dirs.participant_dir}/processed
    
    # Process each downloaded file using the pre-built client
    while IFS= read -r file_path; do
        if [ -f "\$file_path" ]; then
            filename=\$(basename "\$file_path")
            echo "Processing: \$filename"
            
            # Determine file type and process accordingly
            case "\$filename" in
                *.vcf.gz|*.gvcf.gz)
                    echo "VCF/GVCF file detected: \$filename"
                    # Add VCF processing logic here
                    # Example: validate VCF, extract variants, etc.
                    ;;
                *.bam|*.sam)
                    echo "BAM/SAM file detected: \$filename"
                    # Add BAM processing logic here
                    # Example: validate BAM, extract reads, etc.
                    ;;
                *.fastq.gz|*.fq.gz)
                    echo "FASTQ file detected: \$filename"
                    # Add FASTQ processing logic here
                    # Example: quality control, trimming, etc.
                    ;;
                *)
                    echo "Other file type: \$filename"
                    # Add generic processing logic here
                    ;;
            esac
            
            # Copy processed file to processed directory
            cp "\$file_path" "${output_dirs.participant_dir}/processed/"
            echo "\$file_path" >> processed_files.txt
        fi
    done < downloaded_files
    
    # Generate file statistics
    echo "{" > file_stats.json
    echo "  \"total_files\": \$(wc -l < downloaded_files)," >> file_stats.json
    echo "  \"processed_files\": \$(wc -l < processed_files.txt)," >> file_stats.json
    echo "  \"processing_date\": \"\$(date -Iseconds)\"" >> file_stats.json
    echo "}" >> file_stats.json
    
    # Create processing log
    echo "Sequencing file processing completed" > processing_log.txt
    echo "Total files processed: \$(wc -l < processed_files.txt)" >> processing_log.txt
    echo "Processing date: \$(date)" >> processing_log.txt
    """
}
