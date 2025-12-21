#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add DNS Alias to Existing Twingate Resource

Critical Fix: Twingate requires DNS aliases for proper routing.
This script updates existing Resources that were created without aliases.

Usage:
    python add-alias-to-resource.py --resource-id "UmVzb3VyY2U6MzIyNTM1Ng==" --alias "wazuh-dashboard.internal"
    python add-alias-to-resource.py --resource-name "Wazuh Dashboard" --alias "wazuh-dashboard.internal"
"""

import sys
import io
import json
import argparse
import requests
from pathlib import Path

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load credentials from ~/.claude/.env
env = {}
with open(Path.home() / '.claude' / '.env', 'r') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

TWINGATE_API_KEY = env.get('TWINGATE_API_KEY')
TWINGATE_NETWORK = env.get('TWINGATE_NETWORK_NAME')

if not all([TWINGATE_API_KEY, TWINGATE_NETWORK]):
    print("Error: Missing TWINGATE_API_KEY or TWINGATE_NETWORK_NAME in .env")
    sys.exit(1)

# Twingate API configuration
API_URL = f"https://{TWINGATE_NETWORK}.twingate.com/api/graphql/"
HEADERS = {
    "X-API-KEY": TWINGATE_API_KEY,
    "Content-Type": "application/json"
}

def graphql_request(query, variables=None):
    """Execute GraphQL request against Twingate API"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"API Error {response.status_code}: {response.text}")
        return None

    data = response.json()

    if "errors" in data:
        print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
        return None

    return data.get("data")

def find_resource_by_name(name):
    """Find Resource ID by name"""
    query = """
    {
      resources(first: 100) {
        edges {
          node {
            id
            name
            address {
              value
            }
            alias
          }
        }
      }
    }
    """

    data = graphql_request(query)
    if not data:
        return None

    for edge in data["resources"]["edges"]:
        if edge["node"]["name"] == name:
            return edge["node"]

    return None

def update_resource_alias(resource_id, alias):
    """Update Resource with DNS alias"""

    mutation = """
    mutation($resourceId: ID!, $alias: String) {
      resourceUpdate(
        id: $resourceId
        alias: $alias
      ) {
        entity {
          id
          name
          alias
          address {
            value
          }
        }
      }
    }
    """

    print(f"Updating Resource {resource_id} with alias: {alias}")

    data = graphql_request(mutation, {
        "resourceId": resource_id,
        "alias": alias
    })

    if data and "resourceUpdate" in data:
        resource = data["resourceUpdate"]["entity"]
        print(f"\n✓ Successfully updated Resource!")
        print(f"  Name: {resource['name']}")
        print(f"  Address: {resource['address']['value']}")
        print(f"  Alias: {resource['alias']}")
        print(f"\nYou can now access via: http://{alias}")
        return True
    else:
        print("\n✗ Failed to update Resource")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Add DNS alias to existing Twingate Resource",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # By Resource ID
  python add-alias-to-resource.py --resource-id "UmVzb3VyY2U6MzIyNTM1Ng==" --alias "wazuh-dashboard.internal"

  # By Resource name
  python add-alias-to-resource.py --resource-name "Wazuh Dashboard" --alias "wazuh-dashboard.internal"

  # List all Resources to find ID
  python list-twingate-resources.py
        """
    )

    parser.add_argument('--resource-id', help='Twingate Resource ID')
    parser.add_argument('--resource-name', help='Twingate Resource name')
    parser.add_argument('--alias', required=True, help='DNS alias (e.g., service.internal)')

    args = parser.parse_args()

    if not args.resource_id and not args.resource_name:
        parser.error("Either --resource-id or --resource-name is required")

    resource_id = args.resource_id

    # If name provided, look up ID
    if args.resource_name:
        print(f"Looking up Resource: {args.resource_name}")
        resource = find_resource_by_name(args.resource_name)
        if not resource:
            print(f"✗ Resource not found: {args.resource_name}")
            print("\nRun 'python list-twingate-resources.py' to see all Resources")
            sys.exit(1)

        resource_id = resource["id"]
        print(f"✓ Found Resource: {resource['name']}")
        print(f"  Current Address: {resource['address']['value']}")
        print(f"  Current Alias: {resource.get('alias', 'None')}")
        print()

    # Update alias
    success = update_resource_alias(resource_id, args.alias)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
