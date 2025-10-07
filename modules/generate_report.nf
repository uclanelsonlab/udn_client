process generateReport {
    tag "${udn_id}"
    label 'report'
    
    container 'udn-gateway-client:latest'
    
    cpus 1
    memory '2.GB'
    time '30.m'
    
    input:
    path participant_info
    path downloaded_files
    val output_dirs
    
    output:
    path "processing_report.html", emit: report_html
    path "processing_report.json", emit: report_json
    path "summary.txt", emit: summary
    
    script:
    """
    # Generate HTML report using the pre-built client
    cat > generate_report.py << 'EOF'
import json
import os
from datetime import datetime

# Read participant info
with open('participant_info', 'r') as f:
    participant_data = json.load(f)

# Count downloaded files
with open('downloaded_files', 'r') as f:
    file_list = f.readlines()

# Generate HTML report
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>UDN Gateway Processing Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        .file-list {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>UDN Gateway Processing Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>Participant Information</h2>
        <p><strong>Name:</strong> {participant_data.get('nameFirst', 'N/A')} {participant_data.get('nameLast', 'N/A')}</p>
        <p><strong>UDN ID:</strong> {participant_data.get('udnId', 'N/A')}</p>
        <p><strong>Date of Birth:</strong> {participant_data.get('dateOfBirth', 'N/A')}</p>
        <p><strong>Sex:</strong> {participant_data.get('sex', 'N/A')}</p>
    </div>
    
    <div class="section">
        <h2>Download Summary</h2>
        <p><strong>Total Files Downloaded:</strong> {len(file_list)}</p>
        <p><strong>Download Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>Downloaded Files</h2>
        <div class="file-list">
            <ul>
"""
for file_path in file_list:
    filename = os.path.basename(file_path.strip())
    html_content += f"<li>{filename}</li>"

html_content += """
            </ul>
        </div>
    </div>
    
    <div class="section">
        <h2>Processing Notes</h2>
        <p>All files have been successfully downloaded and are available for analysis.</p>
        <p>For questions or issues, please contact the UDN Gateway support team.</p>
    </div>
</body>
</html>
"""

# Write HTML report
with open('processing_report.html', 'w') as f:
    f.write(html_content)

# Generate JSON report
json_report = {
    "participant": participant_data,
    "download_summary": {
        "total_files": len(file_list),
        "download_date": datetime.now().isoformat(),
        "files": [f.strip() for f in file_list]
    },
    "processing_status": "completed",
    "report_generated": datetime.now().isoformat()
}

with open('processing_report.json', 'w') as f:
    json.dump(json_report, f, indent=2)

# Generate summary
summary_content = f"""
UDN Gateway Processing Summary
============================

Participant: {participant_data.get('nameFirst', 'N/A')} {participant_data.get('nameLast', 'N/A')}
UDN ID: {participant_data.get('udnId', 'N/A')}
Files Downloaded: {len(file_list)}
Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Status: Completed Successfully
"""

with open('summary.txt', 'w') as f:
    f.write(summary_content)
EOF

    python generate_report.py
    
    # Move reports to reports directory
    mv processing_report.html ${output_dirs.reports_dir}/
    mv processing_report.json ${output_dirs.reports_dir}/
    mv summary.txt ${output_dirs.reports_dir}/
    """
}
