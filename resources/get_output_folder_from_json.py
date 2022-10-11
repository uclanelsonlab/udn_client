import json
with open('dnanexus-job.json') as f:
  data = json.load(f)
print(data['folder'])
