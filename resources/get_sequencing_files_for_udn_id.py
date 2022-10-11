import requests
import json
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
parser.add_argument('--udn_id', required=True, help='udn participant id')
parser.add_argument('--api_token_file', required=True, help='api token file')
args = parser.parse_args()

with open(args.api_token_file) as f:
  token = f.readline().strip()

url = 'https://gateway.undiagnosed.hms.harvard.edu/api/2.0/participants/' + args.udn_id + '/sequencing'

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token ' + token
}

response = requests.request('GET', url, headers=headers)

# with open('list_of_sequencing_requests_output.json', 'w') as g:
#   g.write(response.text)

data = json.loads(response.text)

for sequencing_request in data['requests']:
  for sequencing_file in sequencing_request['files']:
    if sequencing_file['storageType'] == 'standard':
      print(sequencing_file['storageLocation'])
    else:
      pass
        # if you want to list manually which files are archived, uncomment the next line
        # print(sequencing_file['storageLocation'])
