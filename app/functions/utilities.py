import subprocess
import shutil
import os

def run_shell_command(command):
    """
    Execute a shell command and return the output.
    
    Args:
        command (str): The command to execute
        
    Returns:
        dict: Command output and status
    """
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            capture_output=True, 
            text=True
        )
        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "output": e.stdout,
            "error": e.stderr
        }

def list_directory(path="."):
    """
    List contents of a directory.
    
    Args:
        path (str): Directory path to list (default: current directory)
        
    Returns:
        list: Files and directories in the specified path
    """
    try:
        return os.listdir(path)
    except Exception as e:
        return {"error": str(e)}

def create_directory(path):
    """
    Create a new directory.
    
    Args:
        path (str): Path of directory to create
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False

def copy_file(source, destination):
    """
    Copy a file from source to destination.
    
    Args:
        source (str): Source file path
        destination (str): Destination path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        shutil.copy2(source, destination)
        return True
    except Exception:
        return False