import argparse
import json
import base64

parser = argparse.ArgumentParser(description='Enter arguments')

parser.add_argument("filename", nargs=1, type=str)

args = parser.parse_args()
data_json = ''

with open(args.filename[0]) as f:
    for line in f:
        if not line.strip().startswith("#"):
            data_json += line

data = json.loads(data_json)["data"]

for filename, b64data in data.iteritems():
    print(filename+"\n"+"-----"+"\n"+base64.b64decode(b64data))
