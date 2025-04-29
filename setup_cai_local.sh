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

# Ensure ~/.local/share exists
mkdir -p ~/.local/share

# Remove existing ~/.local/share/cai if any and move the cloned repository
rm -rf ~/.local/share/cai
mv /tmp/cai ~/.local/share/

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
python3 -m venv ~/.local/share/cai/cai_venv

# Update pip in the virtual environment
~/.local/share/cai/cai_venv/bin/python -m pip install --upgrade pip

# Install uv in the virtual environment
~/.local/share/cai/cai_venv/bin/pip install uv

# Install requirements using uv
~/.local/share/cai/cai_venv/bin/uv pip install -r ~/.local/share/cai/requirements.txt

# Add alias to Fish config
if ! grep -q "alias cai=" ~/.config/fish/config.fish; then
    echo 'alias cai="~/.local/share/cai/cai_venv/bin/python ~/.local/share/cai/cai.py"' >> ~/.config/fish/config.fish
fi

# Print help message in bold green
echo -e "\033[1;32mAdd gemini api key in '~/.local/share/cai/.env' file. For help type cai -h/--help\033[0m"
