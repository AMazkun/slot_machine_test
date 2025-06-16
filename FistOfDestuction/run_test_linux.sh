#!/bin/bash

CURRENT_DIR=$(pwd)
SCRIPT_NAME="${1:-your_script.py}"
STREAM_COUNT=20

echo "Running on Wayland - using tmux for best experience..."

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "Installing tmux..."
    sudo apt update && sudo apt install -y tmux
fi

# Kill existing session if it exists
tmux kill-session -t python_scripts 2>/dev/null

# Create new session
tmux new-session -d -s python_scripts -c "$CURRENT_DIR"

# Create additional windows
for i in {2..20}; do
    tmux new-window -t python_scripts -n "Script-$i" -c "$CURRENT_DIR"
done

# Run scripts in each window
for i in {1..20}; do
    window_index=$((i-1))
    tmux send-keys -t python_scripts:$window_index "echo 'Terminal $i - Running $SCRIPT_NAME'" Enter
    tmux send-keys -t python_scripts:$window_index "/usr/bin/python3.12 $SCRIPT_NAME" Enter
done

# Set different pane layouts for variety
#tmux select-window -t python_scripts:1
#tmux split-window -h -t python_scripts:1
#tmux select-window -t python_scripts:2
#tmux split-window -v -t python_scripts:2

echo "Attaching to tmux session..."
echo "Use Ctrl+b then 0-4 to switch between windows"
echo "Use Ctrl+b then d to detach, 'tmux attach -t python_scripts' to reattach"

# Attach to session
tmux attach -t python_scripts