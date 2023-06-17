# Script to request UDN files for a given sample
Script to request UDN files for a given sample. Example:
```bash
dx run /apps/wdl_wf/udn_aws_to_dnanexus_copy/request_udn_files_wf \
    -istage-common.api_token_file=file-GX6P76j02k8Q5f0QgBV90By0 \
    -istage-common.udn_id="UDN133150" \
    --folder /Analysis/hg38_udn/UDN133150 \
    --name UDN133150_request_udn_files_wf -y --brief
```