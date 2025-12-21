#!/usr/bin/env python3
import sys, io, requests, json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ENV_FILE = Path.home() / '.claude' / '.env'
env_vars = {}
with open(ENV_FILE, 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()

NETWORK = env_vars.get('TWINGATE_NETWORK_NAME')
API_KEY = env_vars.get('TWINGATE_API_KEY')

def query(q):
    url = f"https://{NETWORK}.twingate.com/api/graphql/"
    r = requests.post(url, headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"}, json={"query": q})
    return r.json()

result = query("""
query {
  resources(first: 20) {
    edges {
      node {
        id
        name
        address { value }
        alias
        remoteNetwork { name }
      }
    }
  }
}
""")

print(json.dumps(result, indent=2))
