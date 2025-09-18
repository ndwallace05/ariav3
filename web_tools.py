import webbrowser
import logging
from livekit.agents import function_tool

@function_tool()
async def open_website(url: str) -> str:
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

        # Log the attempt (since webbrowser.open may not show a GUI in headless environments)
        logging.info(f"Attempting to open URL: {url}")
        webbrowser.open(url)

        return f"Success: Attempted to open URL '{url}'."
    except Exception as e:
        logging.error(f"Error opening website: {e}")
        return f"Error: An error occurred while trying to open the website. Reason: {e}"