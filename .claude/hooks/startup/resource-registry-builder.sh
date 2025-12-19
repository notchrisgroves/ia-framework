#!/bin/bash
# Resource Registry Builder - Startup Hook
# Scans resources/ directory and builds RESOURCE-REGISTRY.yaml for agent discovery
#
# Runs automatically at framework startup to ensure agents have latest resource inventory
# Similar to tool registry builder, but for reference materials (PDFs, benchmarks, frameworks)
#
# Author: Intelligence Adjacent Framework
# Date: 2025-12-12

# Get script directory and framework root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Resource registry builder path
BUILDER_SCRIPT="$FRAMEWORK_ROOT/tools/validation/build-resource-registry.py"

# Check if resources directory exists
if [ ! -d "$FRAMEWORK_ROOT/resources" ]; then
    echo "⚠️  Resources directory not found - creating empty registry"
    python "$BUILDER_SCRIPT"
    exit 0
fi

# Run resource registry builder
echo "🔍 Scanning resources directory..."
python "$BUILDER_SCRIPT"

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Resource Registry Updated"
    exit 0
else
    echo "❌ Resource Registry Build Failed"
    exit 1
fi
