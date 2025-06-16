#!/bin/bash

CURRENT_DIR=$(pwd)

NUMBER_OF_WINDOWS=8 #

# Individual window dimensions (calculated to fit the total cascade area)
# --- Cascade Configuration ---
WINDOW_WIDTH=1040
WINDOW_HEIGHT=500
# This ensures the last window's bottom-right corner is within the total dimensions
CASCADE_OFFSET_X=100
CASCADE_OFFSET_Y=70
# Starting position for the first window (e.g., top-left corner on screen)
START_X=50
START_Y=50

# Loop from 0 to NUMBER_OF_WINDOWS-1 to correctly create each window
for ((i=0; i<NUMBER_OF_WINDOWS; i++)); do
  # Calculate position for the current window to create a cascade effect
  x1=$((START_X + i * CASCADE_OFFSET_X))
  y1=$((START_Y + i * CASCADE_OFFSET_Y))
  x2=$((x1 + WINDOW_WIDTH))
  y2=$((y1 + WINDOW_HEIGHT))

  # Construct the terminal name
  TERMINAL_NAME="TEST SLOT $((i+1))"

  # Use osascript with 'on run args' to pass variables safely
  osascript -e "on run argv
    set _x1 to item 1 of argv as integer
    set _y1 to item 2 of argv as integer
    set _x2 to item 3 of argv as integer
    set _y2 to item 4 of argv as integer
    set _terminal_name to item 5 of argv as string
    set _current_dir to item 6 of argv as string

    tell app \"Terminal\"
      # Create a new tab or window and run the command
      # 'do script' creates a new window if no window is active
      # or a new tab in the frontmost window.
      # To explicitly create a new window each time:
      # set newWindow to make new window
      # do script \"cd '\" & _current_dir & \"' && /usr/local/bin/python3.11 FOD_SIM_TEST.py\" in newWindow

      do script \"cd '\" & _current_dir & \"' && /usr/local/bin/python3.11 FOD_SIM_TEST.py\"

      # Give Terminal a moment to create and focus the new window/tab
      delay 0.5

      # Get the frontmost window after the script has started in it
      set frontWindow to front window

      # Set bounds of the front window using the passed variables
      set bounds of frontWindow to {_x1, _y1, _x2, _y2}

      # Set the custom title of the selected tab within the front window
      # This is the correct way to change the title bar text.
      set custom title of selected tab of frontWindow to _terminal_name

      activate
    end tell
  end run" "$x1" "$y1" "$x2" "$y2" "$TERMINAL_NAME" "$CURRENT_DIR"
done
