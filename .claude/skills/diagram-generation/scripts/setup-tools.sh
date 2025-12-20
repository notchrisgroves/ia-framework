#!/bin/bash
# Setup diagram generation tools
#
# Usage: ./setup-tools.sh [--all]
#
# Options:
#   --all    Install all tools including Kroki Docker

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         Diagram Generation Tools Setup                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

INSTALL_ALL=false
if [[ "$1" == "--all" ]]; then
    INSTALL_ALL=true
fi

# Check Node.js
echo "[CHECK] Node.js..."
if command -v node &> /dev/null; then
    echo "  ✓ Node.js $(node --version)"
else
    echo "  ✗ Node.js not found"
    echo "  Install from: https://nodejs.org/"
    exit 1
fi

# Check npm
echo "[CHECK] npm..."
if command -v npm &> /dev/null; then
    echo "  ✓ npm $(npm --version)"
else
    echo "  ✗ npm not found"
    exit 1
fi

# Install Mermaid CLI
echo ""
echo "[INSTALL] Mermaid CLI..."
if command -v mmdc &> /dev/null; then
    echo "  ✓ Already installed: $(mmdc --version 2>/dev/null || echo 'version unknown')"
else
    echo "  Installing @mermaid-js/mermaid-cli..."
    npm install -g @mermaid-js/mermaid-cli

    if command -v mmdc &> /dev/null; then
        echo "  ✓ Installed successfully"
    else
        echo "  ✗ Installation failed"
        exit 1
    fi
fi

# Optional: Docker + Kroki
if $INSTALL_ALL; then
    echo ""
    echo "[CHECK] Docker..."
    if command -v docker &> /dev/null; then
        echo "  ✓ Docker $(docker --version)"

        echo ""
        echo "[INSTALL] Kroki (Docker)..."

        # Check if already running
        if docker ps --format '{{.Names}}' | grep -q kroki; then
            echo "  ✓ Kroki container already running"
        else
            echo "  Starting Kroki container..."
            docker run -d --name kroki -p 8000:8000 yuzutech/kroki

            # Wait for startup
            sleep 3

            # Verify
            if curl -s http://localhost:8000/health > /dev/null 2>&1; then
                echo "  ✓ Kroki running at http://localhost:8000"
            else
                echo "  ⚠ Kroki started but health check failed"
            fi
        fi
    else
        echo "  ⚠ Docker not found - skipping Kroki installation"
        echo "    Kroki is optional. You can still use Mermaid CLI."
    fi
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Available tools:"
echo "  • mmdc (Mermaid CLI) - Export Mermaid diagrams to PNG/SVG"
if $INSTALL_ALL && command -v docker &> /dev/null; then
    echo "  • Kroki - Extended diagram format support"
fi
echo ""
echo "Usage:"
echo "  python skills/diagram-generation/scripts/export-diagram.py input.mmd -o output.png"
echo ""
