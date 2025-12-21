#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Twingate Resources for REAPER"""

import sys, io, requests, json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
env = {}
with open(Path.home() / '.claude' / '.env', 'r') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

url = f"https://{env['TWINGATE_NETWORK_NAME']}.twingate.com/api/graphql/"
headers = {'X-API-KEY': env['TWINGATE_API_KEY'], 'Content-Type': 'application/json'}

# Step 1: Get OHVCloud Remote Network ID
print("Finding OHVCloud Remote Network...")
r = requests.post(url, headers=headers, json={'query': '''
{
  remoteNetworks(first: 20) {
    edges {
      node {
        id
        name
      }
    }
  }
}
'''})

network_id = None
for edge in r.json()['data']['remoteNetworks']['edges']:
    if edge['node']['name'] == 'OHVCloud':
        network_id = edge['node']['id']
        print(f"✓ Found OHVCloud: {network_id}\n")
        break

if not network_id:
    print("Error: OHVCloud network not found")
    sys.exit(1)

# Step 2: Create REAPER Web UI Resource
print("Creating REAPER Web UI Resource (127.0.0.1:8000)...")
mutation = '''
mutation($networkId: ID!, $alias: String) {
  resourceCreate(
    name: "REAPER Web UI"
    address: "127.0.0.1"
    alias: $alias
    remoteNetworkId: $networkId
    protocols: {
      allowIcmp: false
      tcp: {
        policy: RESTRICTED
        ports: [{start: 8000, end: 8000}]
      }
      udp: {
        policy: RESTRICTED
        ports: []
      }
    }
  ) {
    entity {
      id
      name
      alias
    }
  }
}
'''

r = requests.post(url, headers=headers, json={'query': mutation, 'variables': {'networkId': network_id, 'alias': 'reaper-ui.internal'}})
result = r.json()

if 'errors' in result:
    print(f"Error: {json.dumps(result['errors'], indent=2)}")
else:
    resource_id = result['data']['resourceCreate']['entity']['id']
    resource_alias = result['data']['resourceCreate']['entity']['alias']
    print(f"✓ Created: REAPER Web UI (ID: {resource_id}, Alias: {resource_alias})\n")

# Step 3: Create REAPER API Resource
print("Creating REAPER API Resource (127.0.0.1:8080)...")
mutation = '''
mutation($networkId: ID!, $alias: String) {
  resourceCreate(
    name: "REAPER API"
    address: "127.0.0.1"
    alias: $alias
    remoteNetworkId: $networkId
    protocols: {
      allowIcmp: false
      tcp: {
        policy: RESTRICTED
        ports: [{start: 8080, end: 8080}]
      }
      udp: {
        policy: RESTRICTED
        ports: []
      }
    }
  ) {
    entity {
      id
      name
      alias
    }
  }
}
'''

r = requests.post(url, headers=headers, json={'query': mutation, 'variables': {'networkId': network_id, 'alias': 'reaper-api.internal'}})
result = r.json()

if 'errors' in result:
    print(f"Error: {json.dumps(result['errors'], indent=2)}")
else:
    resource_id = result['data']['resourceCreate']['entity']['id']
    resource_alias = result['data']['resourceCreate']['entity']['alias']
    print(f"✓ Created: REAPER API (ID: {resource_id}, Alias: {resource_alias})\n")

print("=== Resources Created ===")
print("\nNEXT STEP: Assign access in Twingate Admin Console")
print(f"Go to: https://{env['TWINGATE_NETWORK_NAME']}.twingate.com/admin/resources")
print("For each Resource:")
print("  1. Click on the Resource")
print("  2. Go to 'Access' tab")
print("  3. Add your user/group")
print("  4. Save")
