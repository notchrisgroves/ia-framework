#!/bin/bash
# IA Framework Installer - Unix (macOS/Linux)

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       Intelligence Adjacent (IA) Framework Installer      ║"
echo "╚═══════════════════════════════════════════════════════════╝"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$REPO_DIR/.claude"
TARGET_DIR="$HOME/.claude"

echo "[INFO] Repository: $REPO_DIR"
echo "[INFO] Target: $TARGET_DIR"

# Handle existing ~/.claude
if [ -e "$TARGET_DIR" ]; then
    if [ -L "$TARGET_DIR" ]; then
        echo "[WARN] Existing symlink found"
        read -p "Replace? (y/N) " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] && rm "$TARGET_DIR" || exit 0
    else
        echo "[WARN] Existing directory found"
        BACKUP="$HOME/.claude.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$TARGET_DIR" "$BACKUP"
        echo "[OK] Backed up to: $BACKUP"
    fi
fi

# Create symlink
ln -s "$CLAUDE_DIR" "$TARGET_DIR"
echo "[OK] Created symlink: $TARGET_DIR -> $CLAUDE_DIR"

# Copy .env.example
if [ -f "$REPO_DIR/.env.example" ] && [ ! -f "$HOME/.env" ]; then
    cp "$REPO_DIR/.env.example" "$HOME/.env"
    echo "[OK] Created ~/.env (add your API keys)"
fi

# Create user directories
for dir in sessions plans output; do
    mkdir -p "$CLAUDE_DIR/$dir"
    [ ! -f "$CLAUDE_DIR/$dir/README.md" ] && echo "# $dir" > "$CLAUDE_DIR/$dir/README.md"
done
echo "[OK] Created user directories"

echo ""
echo "Installation complete!"
echo "Next: Edit ~/.env to add your ANTHROPIC_API_KEY"
