import webbrowser
import logging

def open_website(url: str) -> str:
    """
    Opens a given URL in the default web browser.

    Args:
        url: The full URL of the website to open.

    Returns:
        A string indicating success or failure.
    """
    try:
        if not url or not isinstance(url, str):
            return "Error: Invalid URL provided."

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # In a headless environment, webbrowser.open might not do anything visible,
        # but it should still execute without error if the command exists.
        # We will log that the function was called.
        logging.info(f"Attempting to open URL: {url}")

        # The following line would open a browser on a desktop machine.
        # In this sandboxed environment, it may not have a visible effect.
        webbrowser.open(url)

        return f"Success: Attempted to open URL '{url}'."
    except Exception as e:
        logging.error(f"Error opening website: {e}")
        return f"Error: An error occurred while trying to open the website. Reason: {e}"
