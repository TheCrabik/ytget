#!/bin/bash
#Build.sh

if [[ $EUID -ne 0 ]]; then
    echo "Run with sudo!"
    exit 1
fi

SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR"
USER_HOME=$(eval echo ~${SUDO_USER})
mkdir -p "${USER_HOME}/yt"
mkdir -p "${USER_HOME}/yt/audio"
mkdir -p "${USER_HOME}/yt/video"

if ! command -v pyinstaller &> /dev/null; then
    echo "Error: pyinstaller is not detected or not in PATH"
    exit 1
fi

echo "Pyinstaller found: $(which pyinstaller)"
echo "Starting build..."
echo "Build started at: $(date)"
echo "Python version: $(sudo -u "$SUDO_USER" python --version 2>/dev/null || echo "Python not found")"
sudo -u $SUDO_USER echo "Building ytget as user: $SUDO_USER"
sudo -u $SUDO_USER pyinstaller ytget.spec

echo ""
echo "Build completed. Do you want to install ytget to /usr/local/bin/? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    cp "$(dirname "$0")/dist/ytget" /usr/local/bin/
    FILE=$(ls /usr/local/bin/ | grep ytget)

    if [[ $FILE == "ytget" ]]; then
        echo "Installation completed successfully."

        # Remove build and dist directories
        echo "Cleaning up build directories..."
        rm -rfi "${SCRIPT_DIR}/build" 2>/dev/null
        rm -rfi "${SCRIPT_DIR}/dist" 2>/dev/null
        echo "Cleanup completed."
    else
        echo "Installation has failed."
        echo "Check above for errors."
        exit 1
    fi

    chown -R ${SUDO_USER}:${SUDO_USER} "${USER_HOME}/yt"
    echo "ytget has been installed to /usr/local/bin/"
else
    echo "Installation cancelled."
    echo "The built binary is available at: $(dirname "$0")/dist/ytget"
fi
