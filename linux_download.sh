#!/usr/bin/env bash

set -e

APP_NAME="DummyFinance"
INSTALL_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Installing $APP_NAME..."

mkdir -p "$INSTALL_DIR" "$ICON_DIR" "$DESKTOP_DIR"

# download binary (replace URL with your GitHub raw link)
curl -L -o "$INSTALL_DIR/$APP_NAME" \
  https://github.com/BADRUMBADRUM/DummyFinance/releases/latest/download/dummyfinance-linux

chmod +x "$INSTALL_DIR/$APP_NAME"

# install icon
curl -L -o "$ICON_DIR/$APP_NAME.png" \
  https://raw.githubusercontent.com/BADRUMBADRUM/DummyFinance/main/dummyfinance.png

# create desktop entry
cat > "$DESKTOP_DIR/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Name=DummyFinance
Exec=$INSTALL_DIR/$APP_NAME
Icon=$ICON_DIR/$APP_NAME.png
Type=Application
Terminal=false
Categories=Office;Finance;
EOF

echo "Done! You may need to log out and back in."
