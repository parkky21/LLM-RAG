import webbrowser
import os
import subprocess
import platform

def open_chrome(url="https://www.google.com"):
    """
    Open Google Chrome browser with the specified URL.
    
    Args:
        url (str): The URL to open in Chrome (default: Google homepage)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Different approaches based on OS
        system = platform.system()
        if system == "Windows":
            os.startfile(f"chrome {url}")
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "-a", "Google Chrome", url])
        else:  # Linux
            subprocess.run(["google-chrome", url])
        return True
    except Exception:
        return False

def open_calculator():
    """
    Open the calculator application based on the operating system.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        system = platform.system()
        if system == "Windows":
            os.system("calc")
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "-a", "Calculator"])
        else:  # Linux
            subprocess.run(["gnome-calculator"])
        return True
    except Exception:
        return False

def open_notepad(filename=None):
    """
    Open Notepad (Windows) or equivalent text editor on other platforms.
    
    Args:
        filename (str, optional): Path to file to open
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        system = platform.system()
        if system == "Windows":
            if filename:
                os.system(f"notepad {filename}")
            else:
                os.system("notepad")
        elif system == "Darwin":  # macOS
            if filename:
                subprocess.run(["open", "-a", "TextEdit", filename])
            else:
                subprocess.run(["open", "-a", "TextEdit"])
        else:  # Linux
            if filename:
                subprocess.run(["gedit", filename])
            else:
                subprocess.run(["gedit"])
        return True
    except Exception:
        return False