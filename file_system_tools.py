import os

def create_folder(folder_path: str) -> str:
    """
    Creates a new folder at the specified path.

    Args:
        folder_path: The path for the new folder.

    Returns:
        A string indicating success or failure.
    """
    try:
        if not folder_path or not isinstance(folder_path, str):
            return "Error: Invalid folder path provided."

        if os.path.exists(folder_path):
            return f"Error: Folder '{folder_path}' already exists."

        os.makedirs(folder_path)
        return f"Success: Folder '{folder_path}' created."
    except Exception as e:
        return f"Error: Failed to create folder '{folder_path}'. Reason: {e}"

def create_file(file_path: str, content: str) -> str:
    """
    Creates a new file with specified content.

    Args:
        file_path: The path for the new file.
        content: The content to write into the new file.

    Returns:
        A string indicating success or failure.
    """
    try:
        if not file_path or not isinstance(file_path, str):
            return "Error: Invalid file path provided."

        if os.path.exists(file_path):
            return f"Error: File '{file_path}' already exists."

        with open(file_path, 'w') as f:
            f.write(content)
        return f"Success: File '{file_path}' created."
    except Exception as e:
        return f"Error: Failed to create file '{file_path}'. Reason: {e}"

def edit_file(file_path: str, content: str) -> str:
    """
    Appends content to an existing file.

    Args:
        file_path: The path of the file to edit.
        content: The content to append to the file.

    Returns:
        A string indicating success or failure.
    """
    try:
        if not file_path or not isinstance(file_path, str):
            return "Error: Invalid file path provided."

        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist. Please create it first."

        with open(file_path, 'a') as f:
            f.write(content)
        return f"Success: Content appended to file '{file_path}'."
    except Exception as e:
        return f"Error: Failed to edit file '{file_path}'. Reason: {e}"

def list_files(directory_path: str = ".") -> str:
    """
    Lists all files and directories within a specified folder.

    Args:
        directory_path: The path of the directory to inspect. Defaults to the current directory.

    Returns:
        A string containing the list of files and directories, or an error message.
    """
    try:
        if not os.path.isdir(directory_path):
            return f"Error: The path '{directory_path}' is not a valid directory."
        files = os.listdir(directory_path)
        if not files:
            return f"The directory '{directory_path}' is empty."
        return f"Files in '{directory_path}':\n" + "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

def read_file(file_path: str) -> str:
    """
    Reads the entire content of a specified file.

    Args:
        file_path: The path of the file to read.

    Returns:
        The content of the file as a string, or an error message.
    """
    try:
        if not os.path.isfile(file_path):
            return f"Error: The path '{file_path}' is not a valid file."
        with open(file_path, 'r') as f:
            content = f.read()
        return f"Content of '{file_path}':\n{content}"
    except Exception as e:
        return f"Error reading file: {e}"
