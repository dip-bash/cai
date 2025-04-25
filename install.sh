#!/bin/bash
set -e

# Detect package manager
if command -v apt >/dev/null 2>&1; then
    PKG_MANAGER="apt"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
else
    echo "Unsupported package manager"
    exit 1
fi

# Clone the repository to /tmp/cai
git clone https://github.com/dip-bash/cai.git /tmp/cai

# Remove existing /usr/local/cai if any and move the cloned repository
sudo rm -rf /usr/local/cai
sudo mv /tmp/cai /usr/local/

# Check and install python3 if necessary
if ! command -v python3 >/dev/null 2>&1; then
    if [ "$PKG_MANAGER" = "apt" ]; then
        sudo apt update
        sudo apt install -y python3
    elif [ "$PKG_MANAGER" = "dnf" ]; then
        sudo dnf install -y python3
    elif [ "$PKG_MANAGER" = "pacman" ]; then
        sudo pacman -Sy --noconfirm python
    fi
fi

# Check and install fish if necessary
if ! command -v fish >/dev/null 2>&1; then
    if [ "$PKG_MANAGER" = "apt" ]; then
        sudo apt install -y fish
    elif [ "$PKG_MANAGER" = "dnf" ]; then
        sudo dnf install -y fish
    elif [ "$PKG_MANAGER" = "pacman" ]; then
        sudo pacman -Sy --noconfirm fish
    fi
fi

# Add exec fish to .bashrc if not already present
if ! grep -q "exec fish" ~/.bashrc; then
    echo "exec fish" >> ~/.bashrc
fi

# Create the virtual environment
sudo python3 -m venv /usr/local/cai/cai_venv

# Install uv in the virtual environment
sudo /usr/local/cai/cai_venv/bin/pip install uv

# Install requirements using uv
sudo /usr/local/cai/cai_venv/bin/uv pip install -r /usr/local/cai/requirements.txt

# Add alias to Fish config
if ! grep -q "alias cai=" ~/.config/fish/config.fish; then
    echo 'alias cai="/usr/local/cai/cai_venv/bin/python /usr/local/cai/cai.py"' >> ~/.config/fish/config.fish
fi

# Print help message in bold green
echo -e "\033[1;32mAdd gemini api key in '/usr/local/cai/.env'. For help type cai -h/--help\033[0m"
