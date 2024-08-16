#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse
from subprocess import call


def curl_file(download_link, file_name, ):
    """ Curl command to download file """
    cmd = f"curl '{download_link}' -o '{file_name}'"
    print("# Downloading ", file_name)
    print(cmd)
    call(cmd, shell=1)

def request_data(token, url):
    """ Request JSON data from API """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token
    }
    response = requests.request('GET', url, headers=headers)
    data = json.loads(response.text)
    return data

def main(args):
    """ Args function to run downsampled """
    api_token_file = os.path.abspath(args.api_token_file)
    udn_id = str(args.udn_id)
    # Check prefix
    print(api_token_file)
    print(udn_id)
    # Get files ID available for download
    with open(api_token_file) as f:
        token = f.readline().strip()
    url = 'https://gateway.undiagnosed.hms.harvard.edu/api/2.0/participants/' + udn_id + '/sequencing'
    sequencing_data = request_data(token, url)
    files_id_lst = []
    for sequencing_request in sequencing_data['requests']:
        for sequencing_file in sequencing_request['files']:
            # Only files in s3
            if sequencing_file['storageType'].lower().startswith("standard"):
                files_id_lst.append(sequencing_file["id"])
    print("Number of files to download: ", len(files_id_lst))
    # Download each file available
    for file_id in files_id_lst:
        url_files = f"https://gateway.undiagnosed.hms.harvard.edu/api/2.0/participants/{udn_id}/sequencing/files/{file_id}"
        files_data = request_data(token, url_files)
        try:
            download_link = files_data["downloadLink"]
            file_name = files_data["filename"]
            curl_file(download_link, file_name)
        except KeyError as e:
            print(f"# ERROR: Tried to download file ID {file_id}: {e}")
            print(files_data)
            pass

if __name__ == "__main__":
    """ Arguments for the main function """
    parser = argparse.ArgumentParser(
        description="Script to download data from UDN gateway for a given UDN id patient", usage='''Usage:
        python src/request_udn_files.py -a file-GX6P76j02k8Q5f0QgBV90By0 -u UDN970218 ''')
    parser.add_argument("-u", "--udn_id", help="UDN participan ID to download data", type=str)
    parser.add_argument("-a", "--api_token_file", help="API token file", type=str)
    parser.set_defaults(func=main)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)
