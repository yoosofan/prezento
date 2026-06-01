#!/bin/bash

pwd

# Script: Clean hidden files/folders (except .git) and Python artifacts
# Usage: ./cleanup_root.sh

# Duck.ai based on Claude Haiko 4.5

# Safety confirmation
#read -p "⚠️  This will remove hidden files/folders (except .git) and Python cache files from root. Continue? (y/N) " -n 1 -r
#echo
#if [[ ! $REPLY =~ ^[Yy]$ ]]; then
#    echo "Aborted."
#    exit 1
#fi

# Step 1: Remove hidden files and directories (except .git)
echo "Removing hidden files and directories (except .git)..."
for item in .*; do
    # Skip . and .. and .git
    if [[ "$item" != "." && "$item" != ".." && "$item" != ".git" ]]; then
        if [[ -e "$item" ]]; then
            rm -rf "$item"
            echo "  Removed: $item"
        fi
    fi
done

# Step 2: Remove Python cache and generated files
echo "Removing Python cache and generated files..."

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null

# Remove .pyo files
find . -type f -name "*.pyo" -delete 2>/dev/null

# Remove .pyd files
find . -type f -name "*.pyd" -delete 2>/dev/null

# Remove .so files (compiled extensions)
find . -type f -name "*.so" -delete 2>/dev/null

# Remove egg-info directories
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null

# Remove eggs directories
find . -type d -name "*.eggs" -exec rm -rf {} + 2>/dev/null

# Remove build directories
find . -type d -name "build" -exec rm -rf {} + 2>/dev/null

# Remove dist directories
find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null

# Remove .pytest_cache
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null

# Remove .mypy_cache
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null

# Remove .coverage
find . -type f -name ".coverage" -delete 2>/dev/null

# Remove htmlcov directory
find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null

# Remove *.egg file
find . -type f -name "*.egg" -delete 2>/dev/null

echo "✓ Cleanup complete!"
