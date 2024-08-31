import subprocess
from AppKit import NSWorkspace, NSAppleScript

def select_file_in_downloads(filename):
    """
    Opens Finder, navigates to the Downloads folder, and selects the specified file.
    
    Args:
        filename (str): The name of the file to select in the Downloads folder.
    
    Returns:
        bool: True if the file was successfully selected, False otherwise.
    """
    # Activate Finder
    workspace = NSWorkspace.sharedWorkspace()
    finder_app = workspace.launchApplication_("Finder")
    
    if not finder_app:
        print("Failed to launch Finder")
        return False

    # AppleScript to navigate to Downloads and select the file
    script = f'''
    tell application "Finder"
        activate
        set downloadsFolder to path to downloads folder
        open downloadsFolder
        select file "{filename}" of downloadsFolder
    end tell
    '''
    
    # Execute the AppleScript
    ns_script = NSAppleScript.alloc().initWithSource_(script)
    result, error = ns_script.executeAndReturnError_(None)
    
    if error:
        print(f"Error executing AppleScript: {error}")
        return False
    
    return True

def click_open_button():
    """
    Simulates clicking the 'Open' button in a standard file dialog.
    
    Returns:
        bool: True if the action was successful, False otherwise.
    """
    script = '''
    tell application "System Events"
        keystroke return
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing AppleScript: {e}")
        return False

def upload_file_from_downloads(filename):
    """
    Selects a file from the Downloads folder and simulates clicking the Open button.
    
    Args:
        filename (str): The name of the file to upload from the Downloads folder.
    
    Returns:
        bool: True if the file was successfully selected and the Open button clicked, False otherwise.
    """
    if select_file_in_downloads(filename):
        return click_open_button()
    return False

# Example usage
if __name__ == "__main__":
    success = upload_file_from_downloads("testimaging.jpg")
    if success:
        print("File selected and Open button clicked successfully")
    else:
        print("Failed to select file or click Open button")