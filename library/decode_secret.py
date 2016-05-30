#!/usr/bin/python
DOCUMENTATION = '''
---
module: decode_secret
short_description: Regenerate secret when configuration is updated
description:
    - This module will take in a json file, ignore comments and decode any b64 data and output to stdout
    - Specify a json file
author: "Daniel Soukhov"
'''

EXAMPLES = '''
- secret-generate: secret-generate jfile=somefile.json

'''

from ansible.module_utils.basic import *
import json
import base64

def main():

    module = AnsibleModule(
        argument_spec = dict(
            jfile = dict(required=True, default=None, type='str'),
        )
    )

    success = ''
    failure = ''
    params = module.params
    jfile = params['jfile']
    data_json = ''

    try:
        with open(jfile) as f:
            for line in f:
                if not line.strip().startswith("#"):
                    data_json += line
    except IOError as e:
        failure += [str(e)]

    data = json.loads(data_json)["data"]

    for filename, b64data in data.iteritems():
        success += str(filename+"\n"+"-----"+"\n"+base64.b64decode(b64data))

    if failure:
        module.fail_json(msg=str(failure))
    else:
        module.exit_json(changed=True, msg=str(success))

if __name__ == '__main__':
    main()
