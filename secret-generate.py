# Jiana Javier
# Daniel Soukhov

import argparse
import json
import base64

parser = argparse.ArgumentParser(description='Enter arguments')

parser.add_argument("--name", required=True, dest = 'name')
parser.add_argument("--label",required=True, dest = 'label')
parser.add_argument("--namespace",required=True,  dest = 'namespace')
parser.add_argument("--filename", required=True, dest = 'filename')
parser.add_argument("files", nargs = '+', type=str)

args = parser.parse_args()

file_data = {}

for f in args.files:
    with open(f, "rb") as output:
        file_read = output.read()
        file_data[f] = base64.b64encode(file_read).decode('UTF-8') 
        
data = {   
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {
        "name": args.name,
        "labels": {
            "app": args.label
        }
    },
    "namespace": args.namespace,
    "data": file_data
    
}

with open (args.filename, 'w') as outfile:
    json.dump(data, outfile)
