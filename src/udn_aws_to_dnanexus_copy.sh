#!/bin/bash
#
# Basic execution pattern: Your app will run on a single machine from
# beginning to end.
#
# Your job's input variables (if any) will be loaded as environment
# variables before this script runs.  Any array inputs will be loaded
# as bash arrays.
#
# Any code outside of main() (or any entry point you may add) is
# ALWAYS executed, followed by running the entry point itself.
#
# See https://documentation.dnanexus.com/developer for tutorials on how
# to modify this file.

main() {

    echo "Value of udn_id_list: '$udn_id_list'"

    # The following line(s) use the dx command-line tool to download your file
    # inputs to the local file system using variable names for the filenames. To
    # recover the original filenames, you can use the output of "dx describe
    # "$variable" --name".

    dx download "$udn_id_list" -o udn_id_list

    # install pip3
    sudo apt-get update
    sudo apt-get install -y python3-pip
    # we need to do this otherwise pip3 doesn't work on dnanexus
    sudo rm -rf /usr/share/dnanexus/lib/python2.7/site-packages/concurrent
    # # pip3 install --upgrade pip==20.0.2 # version that cloud workstation uses

    latest_config_filename=$(dx ls "$DX_PROJECT_CONTEXT_ID:/assets/udn_aws_s3_config/udn_s3_config_????????.txt" | sort | tail -n 1)

    echo pip3 install requests
    pip3 install requests

    while read p || [[ -n "$p" ]]; do # allow for POSIX non-compliant missing newline at end of file
      if [[ -n "$p" ]]; then # skip extra newlines
        echo processing $p
        python3 /get_sequencing_files_for_udn_id.py --api_token_file /api_token.txt --udn_id ${p} >> file_list
      fi
    done < udn_id_list

    # In order to run aws_s3_to_platform_files with specified output folder, we must parse it out of dnanexus-job.json on the local instance.
    dnanexus_output_path=$(python3 /get_output_folder_from_json.py)

    while read url; do
      echo processing $url

      # if there's only one sample in the input file, get the individually called VCF
      if [ $(grep -c "^UDN" udn_id_list) = 1 ]; then
        if [[ ${url} =~ vcf ]] || [[ ${url} =~ bam ]] || [[ ${url} =~ bai ]]; then
          # if it's some S3 bucket other than udnarchive, let's ignore it
          if [[ ${url} =~ udnarchive/ ]]; then
            p=${url#"S3://udnarchive/"}
            dx run aws_s3_to_platform_files -if_urls=${p} -iupload_direct_to_proj=True -iconfig_file=UCLA-UDN:/assets/udn_aws_s3_config/${latest_config_filename} -itarget_s3=udnarchive --brief -y --folder "$DX_PROJECT_CONTEXT_ID:${dnanexus_output_path}"
          else
            echo skipping ${url} for now due to unexpected bucket
          fi
        fi

      # otherwise only get the joint called VCF
      else
        if [[ ${url} =~ joint ]] || [[ ${url} =~ bam ]] || [[ ${url} =~ bai ]]; then
          # if it's some S3 bucket other than udnarchive, let's ignore it
          if [[ ${url} =~ udnarchive/ ]]; then
            p=${url#"S3://udnarchive/"}
            dx run aws_s3_to_platform_files -if_urls=${p} -iupload_direct_to_proj=True -iconfig_file=UCLA-UDN:/assets/udn_aws_s3_config/${latest_config_filename} -itarget_s3=udnarchive --brief -y --folder "$DX_PROJECT_CONTEXT_ID:${dnanexus_output_path}"
          else
            echo skipping ${url} for now due to unexpected bucket
          fi
        fi

      fi
    done < file_list

    # Fill in your application code here.
    #
    # To report any recognized errors in the correct format in
    # $HOME/job_error.json and exit this script, you can use the
    # dx-jobutil-report-error utility as follows:
    #
    #   dx-jobutil-report-error "My error message"
    #
    # Note however that this entire bash script is executed with -e
    # when running in the cloud, so any line which returns a nonzero
    # exit code will prematurely exit the script; if no error was
    # reported in the job_error.json file, then the failure reason
    # will be AppInternalError with a generic error message.

}
