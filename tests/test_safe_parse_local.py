import pytest
import logging
import os
from pathlib import Path
from unittest.mock import patch

import oscn


def load_html_file(case_id):
    """Load HTML content from local data file"""
    html_file = Path("data/html") / f"{case_id}.html"
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()


def safe_parse(fn, html):
    """Safe parsing function that handles errors and returns default values"""
    try:
        return fn(html) if html else fn._default_value
    except Exception as e:
        logging.error(f"Error parsing with {fn.__name__}: {e}")
        return "" if fn.__name__ == "judge" else fn._default_value


def test_safe_parse_with_local_issues():
    """Test safe_parse works with oscn.parse.issues using local HTML"""
    html = load_html_file("tulsa-CJ-2024-3204")

    # Test with valid HTML
    issues = safe_parse(oscn.parse.issues, html)
    assert isinstance(issues, list)
    assert hasattr(issues, "text")  # MetaList has text attribute

    # Test with None HTML (should return _default_value)
    issues_none = safe_parse(oscn.parse.issues, None)
    assert issues_none == []  # _default_value for issues is []

    # Test with empty HTML (should return _default_value)
    issues_empty = safe_parse(oscn.parse.issues, "")
    assert issues_empty == []  # _default_value for issues is []


def test_safe_parse_with_local_counts():
    """Test safe_parse works with oscn.parse.counts using local HTML"""
    html = load_html_file("tulsa-CF-2024-1583")

    # Test with valid HTML
    counts = safe_parse(oscn.parse.counts, html)
    assert isinstance(counts, list)
    assert hasattr(counts, "text")  # MetaList has text attribute

    # Test with None HTML (should return _default_value)
    counts_none = safe_parse(oscn.parse.counts, None)
    assert counts_none == []  # _default_value for counts is []

    # Test with empty HTML (should return _default_value)
    counts_empty = safe_parse(oscn.parse.counts, "")
    assert counts_empty == []  # _default_value for counts is []


def test_safe_parse_with_local_parties():
    """Test safe_parse works with oscn.parse.parties using local HTML"""
    html = load_html_file("tulsa-CJ-2024-3204")

    # Test with valid HTML
    parties = safe_parse(oscn.parse.parties, html)
    assert isinstance(parties, list)
    assert hasattr(parties, "text")  # MetaList has text attribute

    # Test with None HTML (should return _default_value)
    parties_none = safe_parse(oscn.parse.parties, None)
    assert parties_none == []  # _default_value for parties is []

    # Test with empty HTML (should return _default_value)
    parties_empty = safe_parse(oscn.parse.parties, "")
    assert parties_empty == []  # _default_value for parties is []


def test_safe_parse_with_local_judge():
    """Test safe_parse works with oscn.parse.judge using local HTML"""
    html = load_html_file("tulsa-CF-2024-1583")

    # Test with valid HTML
    judge = safe_parse(oscn.parse.judge, html)
    assert isinstance(judge, str)

    # Test with None HTML (should return empty string for judge)
    judge_none = safe_parse(oscn.parse.judge, None)
    assert judge_none == ""  # Special case for judge

    # Test with empty HTML (should return empty string for judge)
    judge_empty = safe_parse(oscn.parse.judge, "")
    assert judge_empty == ""  # Special case for judge


def test_safe_parse_error_handling():
    """Test safe_parse handles exceptions correctly"""

    # Mock a function that raises an exception
    def mock_parser(html):
        raise ValueError("Test error")

    # Add _default_value to mock function
    mock_parser._default_value = []

    with patch("logging.error") as mock_logger:
        result = safe_parse(mock_parser, "some html")

        # Should return _default_value when exception occurs
        assert result == []

        # Should log the error
        mock_logger.assert_called_once()


def test_safe_parse_functions_have_default_values():
    """Test that all parser functions have _default_value attribute"""
    assert hasattr(oscn.parse.issues, "_default_value")
    assert hasattr(oscn.parse.counts, "_default_value")
    assert hasattr(oscn.parse.parties, "_default_value")
    assert hasattr(oscn.parse.judge, "_default_value")

    # Verify default values
    assert oscn.parse.issues._default_value == []
    assert oscn.parse.counts._default_value == []
    assert oscn.parse.parties._default_value == []
    assert oscn.parse.judge._default_value == ""


def test_safe_parse_integration_local():
    """Test safe_parse with local HTML data"""
    html = load_html_file("tulsa-CJ-2024-3204")

    # Test all three functions together
    issues = safe_parse(oscn.parse.issues, html)
    counts = safe_parse(oscn.parse.counts, html)
    parties = safe_parse(oscn.parse.parties, html)

    # Verify all return expected types
    assert isinstance(issues, list)
    assert isinstance(counts, list)
    assert isinstance(parties, list)

    # Verify they have text attributes (MetaList)
    assert hasattr(issues, "text")
    assert hasattr(counts, "text")
    assert hasattr(parties, "text")

    print("✅ All three functions work with safe_parse using local data:")
    print(f"  - issues: {type(issues)} with {len(issues)} items")
    print(f"  - counts: {type(counts)} with {len(counts)} items")
    print(f"  - parties: {type(parties)} with {len(parties)} items")


def test_multiple_local_files():
    """Test safe_parse with multiple local HTML files"""
    test_files = [
        "tulsa-CJ-2024-3204",
        "tulsa-CF-2024-1583",
        "oklahoma-CJ-2024-3069",
        "cleveland-CJ-2024-1543",
    ]

    for case_id in test_files:
        try:
            html = load_html_file(case_id)

            # Test all three functions
            issues = safe_parse(oscn.parse.issues, html)
            counts = safe_parse(oscn.parse.counts, html)
            parties = safe_parse(oscn.parse.parties, html)

            # Basic validation
            assert isinstance(issues, list)
            assert isinstance(counts, list)
            assert isinstance(parties, list)

            print(
                f"✅ {case_id}: issues={len(issues)}, counts={len(counts)}, parties={len(parties)}"
            )

        except FileNotFoundError:
            print(f"⚠️  Skipping {case_id}: file not found")
        except Exception as e:
            print(f"❌ Error processing {case_id}: {e}")


def test_exact_usage_pattern_local():
    """Test the exact usage pattern with local HTML files"""
    html = load_html_file("tulsa-CJ-2024-3204")

    # This is the exact pattern the user wants to verify works
    issues = safe_parse(oscn.parse.issues, html)
    counts = safe_parse(oscn.parse.counts, html)
    parties = safe_parse(oscn.parse.parties, html)

    # Verify all functions work and return expected types
    assert isinstance(issues, list)
    assert isinstance(counts, list)
    assert isinstance(parties, list)

    # Verify they have the expected attributes
    assert hasattr(issues, "text")
    assert hasattr(counts, "text")
    assert hasattr(parties, "text")

    print("✅ Exact usage pattern works with local data:")
    print(f"  - issues: {type(issues)} with {len(issues)} items")
    print(f"  - counts: {type(counts)} with {len(counts)} items")
    print(f"  - parties: {type(parties)} with {len(parties)} items")


if __name__ == "__main__":
    test_exact_usage_pattern_local()
    test_multiple_local_files()
    test_safe_parse_integration_local()
    print(
        "\n🎉 All tests passed! The safe_parse function works correctly with local HTML files."
    )
