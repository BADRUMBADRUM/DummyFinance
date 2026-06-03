#!/usr/bin/env bash

set -e

APP_NAME="DummyFinance"
INSTALL_DIR="/Applications"
TMP_DIR="$(mktemp -d)"

echo "Installing $APP_NAME for macOS..."

curl -L -o "$TMP_DIR/$APP_NAME-macos.zip" \
  https://github.com/BADRUMBADRUM/DummyFinance/releases/latest/download/DummyFinance-macos.zip

unzip -q "$TMP_DIR/$APP_NAME-macos.zip" -d "$TMP_DIR"

rm -rf "$INSTALL_DIR/$APP_NAME.app"

mv "$TMP_DIR/$APP_NAME.app" "$INSTALL_DIR/"

echo "Installed successfully!"
echo "Open it from /Applications/$APP_NAME.app"
