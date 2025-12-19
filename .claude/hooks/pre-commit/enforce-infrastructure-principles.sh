#!/bin/bash
# Infrastructure Principles Enforcement Hook
# Enforces critical infrastructure principles at git commit time

set -e

echo "🔍 Checking infrastructure principles compliance..."

# Principle #1: On-demand containers for security tools
# Security tool containers MUST use "restart: no" (not "restart: unless-stopped")
check_restart_policies() {
    if git diff --cached --name-only | grep -q "servers/docker-compose.yml"; then
        if git diff --cached servers/docker-compose.yml | grep -E "^\+.*restart:.*unless-stopped" | grep -qE "kali|metasploit|web3|mobile|reaper"; then
            echo "❌ VIOLATION: Principle #1 - On-Demand Containers"
            echo ""
            echo "Security tool containers MUST use 'restart: no' (not 'restart: unless-stopped')"
            echo ""
            echo "Affected containers: kali-pentest, metasploit, web3-security, mobile-tools, reaper"
            echo "Reason: Prevents disk space exhaustion from always-running containers"
            echo ""
            echo "See: servers/ON-DEMAND-CONTAINER-MODEL.md"
            echo "See: skills/infrastructure-ops/reference/PRINCIPLES.md (Principle #1)"
            exit 1
        fi
        echo "✅ Principle #1: On-demand container restart policies compliant"
    fi
}

# Principle #2: Twingate registration mandatory
# docker-compose.yml changes MUST be accompanied by inventory updates
check_twingate_registration() {
    if git diff --cached --name-only | grep -q "servers/docker-compose.yml"; then
        # Check if new services added (lines starting with service name at root level)
        if git diff --cached servers/docker-compose.yml | grep -E "^\+  [a-z0-9-]+:" | grep -q .; then
            if ! git diff --cached --name-only | grep -q "skills/infrastructure-ops/inventory/twingate-resources.md"; then
                echo "❌ VIOLATION: Principle #2 - Twingate Registration Mandatory"
                echo ""
                echo "New services added to docker-compose.yml require Twingate Resource registration"
                echo "Expected: skills/infrastructure-ops/inventory/twingate-resources.md updated"
                echo ""
                echo "See: skills/infrastructure-ops/reference/PRINCIPLES.md (Principle #2)"
                exit 1
            fi
            echo "✅ Principle #2: Twingate Resources inventory updated"
        fi
    fi
}

# Principle #3: Inventory updates mandatory
# docker-compose.yml changes MUST update docker-services.md
check_inventory_updates() {
    if git diff --cached --name-only | grep -q "servers/docker-compose.yml"; then
        if ! git diff --cached --name-only | grep -q "skills/infrastructure-ops/inventory/docker-services.md"; then
            echo "❌ VIOLATION: Principle #3 - Inventory Updates Mandatory"
            echo ""
            echo "docker-compose.yml changed without docker-services.md inventory update"
            echo "Expected: skills/infrastructure-ops/inventory/docker-services.md updated"
            echo ""
            echo "See: skills/infrastructure-ops/reference/PRINCIPLES.md (Principle #3)"
            exit 1
        fi
        echo "✅ Principle #3: Docker services inventory updated"
    fi
}

# Principle #8: Security by default
# Prevent public port bindings (0.0.0.0) in docker-compose.yml
check_port_bindings() {
    if git diff --cached --name-only | grep -q "servers/docker-compose.yml"; then
        # Check for port bindings without 127.0.0.1 prefix (except 80/443 for Traefik)
        if git diff --cached servers/docker-compose.yml | grep -E '^\+.*ports:' -A 1 | grep -E '^\+.*"[0-9]+:[0-9]+"' | grep -vE "127.0.0.1|80:|443:"; then
            echo "⚠️  WARNING: Principle #8 - Security by Default"
            echo ""
            echo "Port binding without 127.0.0.1 prefix detected"
            echo "Internal services SHOULD bind to localhost (127.0.0.1:PORT:PORT)"
            echo ""
            echo "Exceptions: Traefik (ports 80/443), public reverse proxy"
            echo ""
            echo "See: skills/infrastructure-ops/reference/PRINCIPLES.md (Principle #3)"
            echo ""
            echo "Continue? (y/n)"
            read -r response
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    fi
}

# Run all checks
check_restart_policies
check_twingate_registration
check_inventory_updates
check_port_bindings

echo "✅ All infrastructure principle checks passed"
exit 0
