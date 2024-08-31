# Requirements:
# - For Linux: Xlib (install with: pip install python-xlib)
# - For macOS: PyObjC (typically pre-installed, but can be installed/upgraded with: pip install -U pyobjc)

import sys
import platform

if platform.system() == "Linux":
    from Xlib import display

elif platform.system() == "Darwin":  # macOS
    from AppKit import NSWorkspace, NSApplicationActivationPolicyRegular

def find_window_by_name(name):
    """
    Find a window by its name on both Linux and macOS.
    
    Args:
        name (str): The name of the window to find.
    
    Returns:
        object: The window object if found, None otherwise.
    """
    if platform.system() == "Linux":
        return find_window_by_name_linux(name)
    elif platform.system() == "Darwin":
        return find_window_by_name_mac(name)
    else:
        raise NotImplementedError(f"Unsupported operating system: {platform.system()}")

def find_window_by_name_linux(name):
    """
    Find a window by its name on Linux using Xlib.
    
    Args:
        name (str): The name of the window to find.
    
    Returns:
        object: The window object if found, None otherwise.
    """
    d = display.Display()
    root = d.screen().root
    windows = root.query_tree().children
    for window in windows:
        try:
            if window.get_wm_name() == name:
                return window
        except:
            pass
    return None

def find_window_by_name_mac(name):
    """
    Find a window by its name on macOS using AppKit.
    
    Args:
        name (str): The name of the window to find.
    
    Returns:
        object: The window object if found, None otherwise.
    """
    workspace = NSWorkspace.sharedWorkspace()
    for app in workspace.runningApplications():
        if app.activationPolicy() == NSApplicationActivationPolicyRegular:
            app_name = app.localizedName()
            if app_name == name:
                return app
    return None