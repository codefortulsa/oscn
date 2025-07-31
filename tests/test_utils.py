"""Test utilities for loading local HTML files"""

from pathlib import Path


def load_html_file(case_id):
    """Load HTML content from local data file

    Args:
        case_id (str): Case ID like "tulsa-CJ-2024-3204"

    Returns:
        str: HTML content from the file

    Raises:
        FileNotFoundError: If the HTML file doesn't exist
    """
    html_file = Path("data/html") / f"{case_id}.html"
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()


def get_available_test_files():
    """Get list of available HTML test files

    Returns:
        list: List of case IDs that have HTML files
    """
    html_dir = Path("data/html")
    if not html_dir.exists():
        return []

    return [f.stem for f in html_dir.glob("*.html")]


def load_test_html(case_id=None):
    """Load test HTML, using a default if no case_id provided

    Args:
        case_id (str, optional): Case ID to load. If None, uses a default.

    Returns:
        str: HTML content
    """
    if case_id is None:
        # Use a default test file
        case_id = "tulsa-CJ-2024-3204"

    return load_html_file(case_id)
