#!/usr/bin/python

DOCUMENTATION = '''
---
module: secret-generate
short_description: Regenerate secret when configuration is updated
description:
    - This module will generate a json file with base64 encoded contents of input files
    - Specify name, label, namespace, output file name, and input files
author: "Jiana Javier, @jianajavier"
'''

EXAMPLES = '''
- secret-generate: secret-generate name=arg1 label=arg2 namespace=arg3 filename=arg4 files=arg5,arg6,...
'''

from ansible.module_utils.basic import *
import json
import base64

def main():

    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=True, default=None),
            label = dict(required=True, default=None),
            namespace = dict(required=True, default=None),
            filename = dict(required=True, default=None), 
            files = dict(required=True, default=None, type='list'),
        )
    )
        
    params = module.params
    name = params['name']
    label = params['label']
    namespace = params['namespace']
    filename = params['filename']
    files = params['files']

    file_data = {}
    successes = []
    failure = []

    for f in files:
        try:
            with open(f, "rb") as output:
                file_read = output.read()
                file_data[f.split('/')[-1]] = base64.b64encode(file_read).decode('UTF-8')
                successes += [f]
        except IOError as e:
            failure += [str(e)]

    data = {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {
            "name": name,
            "labels": {
                "app": label
            }
        },
        "namespace": namespace,
        "data": file_data
    }

    if file_data:
        try:
            with open (filename, 'w') as outfile:
                json.dump(data, outfile)
        except IOError as e:
            failure += [str(e)]
    
    if failure:
        module.fail_json(msg=str(failure))
    else:
        module.exit_json(changed=True, msg=str(successes)) 

if __name__ == '__main__':
    main()
