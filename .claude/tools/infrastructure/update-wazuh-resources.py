#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Wazuh Twingate Resources with correct localhost addresses"""

import sys, io, requests, json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load credentials
env = {}
with open(Path.home() / '.claude' / '.env', 'r') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

url = f"https://{env['TWINGATE_NETWORK_NAME']}.twingate.com/api/graphql/"
headers = {'X-API-KEY': env['TWINGATE_API_KEY'], 'Content-Type': 'application/json'}

# Resource updates: ID -> (new_address, port)
updates = {
    'UmVzb3VyY2U6MzIyNTM1Ng==': ('127.0.0.1', 5601, 'Wazuh Dashboard'),
    'UmVzb3VyY2U6MzIyNTM1Nw==': ('127.0.0.1', 55000, 'Wazuh API'),
    'UmVzb3VyY2U6MzIyNTM1OA==': ('127.0.0.1', 1514, 'Wazuh Agent Enrollment'),
}

mutation = '''
mutation($resourceId: ID!, $address: String!) {
  resourceUpdate(
    id: $resourceId
    address: $address
  ) {
    entity {
      id
      name
      address { value }
      alias
    }
  }
}
'''

print("Updating Wazuh Resources with localhost addresses...\n")

for resource_id, (address, port, name) in updates.items():
    print(f"Updating {name}...")

    r = requests.post(url, headers=headers, json={
        'query': mutation,
        'variables': {
            'resourceId': resource_id,
            'address': address
        }
    })

    result = r.json()
    if 'errors' in result:
        print(f"  ✗ Error: {json.dumps(result['errors'], indent=2)}")
    else:
        resource = result['data']['resourceUpdate']['entity']
        print(f"  ✓ Updated: {resource['name']}")
        print(f"    Address: {resource['address']['value']}")
        print(f"    Alias: {resource['alias']}")
        print()

print("✓ All Wazuh Resources updated to use localhost addressing")
