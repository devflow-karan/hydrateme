#!/bin/bash
# A utility script to correctly build the HydrateMe .deb package

# Exit on error
set -e

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$PROJECT_ROOT"

# Get project version from package.json
VERSION=$(grep '"version"' package.json | cut -d '"' -f 4)

# Create a clean build staging directory
BUILD_DIR="build_deb_staging"
echo "Building deb version $VERSION into $BUILD_DIR..."

mkdir -p "$BUILD_DIR"

# Copy DEBIAN/ control files
cp -r DEBIAN "$BUILD_DIR/"

# Copy /usr resources
cp -r usr "$BUILD_DIR/"

# Update VERSION in control file if it doesn't match
sed -i "s/^Version:.*/Version: $VERSION-1/" "$BUILD_DIR/DEBIAN/control"

# Set correct permissions
chmod -R 755 "$BUILD_DIR/usr"
chmod 755 "$BUILD_DIR/DEBIAN"
chmod 644 "$BUILD_DIR/DEBIAN/control"
chmod +x "$BUILD_DIR/usr/bin/hydrateme"
chmod +x "$BUILD_DIR/usr/share/hydrateme/hydrateme.py"

# Build the package
DEB_NAME="hydrateme_${VERSION}-1_all.deb"
dpkg-deb --build "$BUILD_DIR" "$DEB_NAME"

# Clean up
rm -rf "$BUILD_DIR"

echo "Success! Package created: $DEB_NAME"
echo "You can test it with: sudo apt install ./$DEB_NAME"
