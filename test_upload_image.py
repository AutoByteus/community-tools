import subprocess
from AppKit import NSWorkspace

def get_frontmost_app_name():
    """Get the name of the frontmost application."""
    workspace = NSWorkspace.sharedWorkspace()
    frontmost_app = workspace.frontmostApplication()
    return frontmost_app.localizedName()

def interact_with_file_dialog(filename):
    """
    Interacts with an open file dialog to select a file from the Downloads folder and click Open.
    
    Args:
        filename (str): The name of the file to select in the Downloads folder.
    
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    frontmost_app = get_frontmost_app_name()
    
    script = f'''
    tell application "{frontmost_app}"
        activate
        tell application "System Events"
            tell process "{frontmost_app}"
                -- Wait for the file dialog to be the frontmost window
                repeat until (exists sheet 1 of window 1)
                    delay 0.1
                end repeat
                
                tell sheet 1 of window 1
                    -- Click the sidebar item "Downloads"
                    click button "Downloads" of outline 1 of scroll area 1 of splitter group 1
                    
                    -- Wait for the file list to update
                    delay 0.5
                    
                    -- Select the file
                    select row 1 of outline 1 of scroll area 2 of splitter group 1 whose value of static text 1 is "{filename}"
                    
                    -- Click the "Open" button
                    click button "Open" of group 1
                end tell
            end tell
        end tell
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing AppleScript: {e}")
        print(f"Script output: {e.output}")
        return False

# Example usage
if __name__ == "__main__":
    success = interact_with_file_dialog("example_image.jpg")
    if success:
        print("File selected and Open button clicked successfully")
    else:
        print("Failed to select file or click Open button")