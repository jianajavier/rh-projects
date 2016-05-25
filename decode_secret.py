import argparse
import json
import base64

parser = argparse.ArgumentParser(description='Enter arguments')

parser.add_argument("f", nargs=1, type=str)

args = parser.parse_args()

with open(args.f[0]) as data_json:
    data = json.load(data_json)["data"]

for filename, b64data in data.iteritems():
    print(filename+"\n"+"-----"+"\n"+base64.b64decode(b64data)+"\n")
