process downloadParticipantData {
    tag "${udn_id}"
    label 'download'
    
    container 'udn-gateway-client:latest'
    
    cpus 2
    memory '4.GB'
    time '1.h'
    
    input:
    path api_token_file
    val udn_id
    val output_dirs
    val download_all
    val download_vcf
    val download_gvcf
    val file_types
    val verbose
    
    output:
    path "participant_info.json", emit: participant_info
    path "downloaded_files.txt", emit: downloaded_files
    path "download_log.txt", emit: download_log
    val udn_id, emit: participant_id
    
    script:
    def verbose_flag = verbose ? '--verbose' : ''
    def file_types_flag = file_types ? "--file-types ${file_types}" : ''
    def output_dir_flag = "--output-dir ${output_dirs.participant_dir}"
    
    def download_cmd = if (download_vcf) {
        "--download --vcf"
    } else if (download_gvcf) {
        "--download --gvcf"
    } else if (download_all) {
        "--all"
    } else {
        "--info-only"
    }
    
    """
    # Create output directory
    mkdir -p ${output_dirs.participant_dir}
    mkdir -p ${output_dirs.logs_dir}
    
    # Download participant data using the pre-built client
    python udn_gateway_cli.py \\
        -a ${api_token_file} \\
        -u ${udn_id} \\
        ${download_cmd} \\
        ${output_dir_flag} \\
        ${file_types_flag} \\
        ${verbose_flag} \\
        > download_log.txt 2>&1
    
    # Get participant info
    python udn_gateway_cli.py \\
        -a ${api_token_file} \\
        -u ${udn_id} \\
        --info-only \\
        > participant_info.json 2>&1
    
    # List downloaded files
    find ${output_dirs.participant_dir} -type f -name "*" > downloaded_files.txt
    
    # Move logs to logs directory
    mv download_log.txt ${output_dirs.logs_dir}/download_${udn_id}.log
    """
}
