#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy Twingate Connector on OVHcloud VPS

Follows infrastructure-ops runbook procedures:
1. Creates Remote Network via API
2. Generates Connector tokens via API
3. Deploys Connector container on VPS
"""

import os
import sys
import io
import json
import time
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load credentials from ~/.claude/.env
load_dotenv(Path.home() / ".claude" / ".env")

TWINGATE_API_KEY = os.getenv("TWINGATE_API_KEY")
TWINGATE_NETWORK = os.getenv("TWINGATE_NETWORK_NAME")
VPS_IP = os.getenv("IPv4_address")
VPS_USER = os.getenv("Username")
SSH_KEY = os.getenv("SSH_PRIV")

if not all([TWINGATE_API_KEY, TWINGATE_NETWORK, VPS_IP, VPS_USER, SSH_KEY]):
    print("Error: Missing required credentials in .env")
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

def get_or_create_remote_network(name="security-testing-ovh"):
    """Get existing or create new Remote Network"""

    print(f"Checking for Remote Network: {name}")

    # Query existing networks
    query = """
    {
      remoteNetworks(first: 100) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """

    data = graphql_request(query)

    if data and "remoteNetworks" in data:
        for edge in data["remoteNetworks"]["edges"]:
            if edge["node"]["name"] == name:
                network_id = edge["node"]["id"]
                print(f"✓ Found existing Remote Network: {name}")
                return network_id

    # Create new Remote Network
    print(f"Creating new Remote Network: {name}")

    mutation = """
    mutation($name: String!) {
      remoteNetworkCreate(name: $name) {
        entity {
          id
          name
        }
      }
    }
    """

    data = graphql_request(mutation, {"name": name})

    if data and "remoteNetworkCreate" in data:
        network_id = data["remoteNetworkCreate"]["entity"]["id"]
        print(f"✓ Created Remote Network: {name}")
        return network_id

    print("Error: Failed to create Remote Network")
    return None

def create_connector(network_id, name="ovh-vps-connector"):
    """Create Connector and generate tokens"""

    print(f"Creating Connector: {name}")

    mutation = """
    mutation($remoteNetworkId: ID!, $name: String!) {
      connectorCreate(
        remoteNetworkId: $remoteNetworkId
        name: $name
      ) {
        entity {
          id
          name
        }
        accessToken
        refreshToken
      }
    }
    """

    data = graphql_request(mutation, {
        "remoteNetworkId": network_id,
        "name": name
    })

    if data and "connectorCreate" in data:
        connector = data["connectorCreate"]
        print(f"✓ Connector created: {connector['entity']['name']}")
        return {
            "id": connector["entity"]["id"],
            "name": connector["entity"]["name"],
            "accessToken": connector["accessToken"],
            "refreshToken": connector["refreshToken"]
        }

    print("Error: Failed to create Connector")
    return None

def deploy_connector_container(tokens):
    """Deploy Twingate Connector on VPS using Docker"""

    print(f"\nDeploying Connector container on VPS ({VPS_IP})...")

    docker_cmd = f"""docker run -d \\
  --name twingate-connector \\
  --restart unless-stopped \\
  -e TWINGATE_NETWORK="{TWINGATE_NETWORK}" \\
  -e TWINGATE_ACCESS_TOKEN="{tokens['accessToken']}" \\
  -e TWINGATE_REFRESH_TOKEN="{tokens['refreshToken']}" \\
  -e TWINGATE_LOG_LEVEL="info" \\
  twingate/connector:latest"""

    ssh_cmd = [
        "ssh",
        "-i", SSH_KEY,
        "-p", "2222",
        f"{VPS_USER}@{VPS_IP}",
        docker_cmd
    ]

    result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)

    if result.returncode == 0:
        container_id = result.stdout.strip()
        print(f"✓ Connector deployed successfully")
        print(f"  Container ID: {container_id}")
        return True
    else:
        print(f"Error deploying Connector:")
        print(result.stderr)
        return False

def verify_connector():
    """Verify Connector is running and connected"""

    print("\nVerifying Connector status...")
    time.sleep(5)  # Wait for container to start

    ssh_cmd = [
        "ssh",
        "-i", SSH_KEY,
        "-p", "2222",
        f"{VPS_USER}@{VPS_IP}",
        "docker logs --tail 30 twingate-connector"
    ]

    result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=10)

    print("\n=== Connector Logs ===")
    print(result.stdout)

    if "connected" in result.stdout.lower() or "ready" in result.stdout.lower():
        print("\n✓ Connector is ONLINE and connected!")
        return True
    else:
        print("\n⚠ Connector is starting up. Check status in Twingate Admin Console.")
        return False

if __name__ == "__main__":
    print("=== Twingate Connector Deployment ===\n")

    # Step 1: Get or create Remote Network
    network_id = get_or_create_remote_network()
    if not network_id:
        print("\nFailed at: Remote Network creation")
        sys.exit(1)

    # Step 2: Create Connector and generate tokens
    tokens = create_connector(network_id)
    if not tokens:
        print("\nFailed at: Connector creation")
        sys.exit(1)

    # Step 3: Deploy Connector container
    if not deploy_connector_container(tokens):
        print("\nFailed at: Container deployment")
        sys.exit(1)

    # Step 4: Verify Connector
    verify_connector()

    print("\n=== Deployment Complete ===")
    print(f"Remote Network: security-testing-ovh")
    print(f"Connector: {tokens['name']}")
    print(f"\nNext Steps:")
    print("1. Verify Connector status in Admin Console")
    print("2. Create Twingate Resources for Reaper (ports 8000, 8080)")
    print("3. Test connectivity through Twingate")
