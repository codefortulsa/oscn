import pytest
import logging
from unittest.mock import patch

import oscn


def safe_parse(fn, html):
    """Test implementation of safe_parse function"""
    try:
        return fn(html) if html else fn._default_value
    except Exception as e:
        logging.error(f"Error parsing with {fn.__name__}: {e}")
        return "" if fn.__name__ == "judge" else fn._default_value


def test_safe_parse_with_issues():
    """Test safe_parse works with oscn.parse.issues"""
    # Load local HTML file instead of making network request
    with open("data/html/tulsa-CJ-2024-3204.html", "r", encoding="utf-8") as f:
        html = f.read()

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


def test_safe_parse_with_counts():
    """Test safe_parse works with oscn.parse.counts"""
    # Load local HTML file instead of making network request
    with open("data/html/tulsa-CF-2024-1583.html", "r", encoding="utf-8") as f:
        html = f.read()

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


def test_safe_parse_with_parties():
    """Test safe_parse works with oscn.parse.parties"""
    # Load local HTML file instead of making network request
    with open("data/html/tulsa-CJ-2024-3204.html", "r", encoding="utf-8") as f:
        html = f.read()

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


def test_safe_parse_with_judge():
    """Test safe_parse works with oscn.parse.judge (special case returning empty string)"""
    # Load local HTML file instead of making network request
    with open("data/html/tulsa-CF-2024-1583.html", "r", encoding="utf-8") as f:
        html = f.read()

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


def test_safe_parse_integration():
    """Test safe_parse with real case data"""
    # Load local HTML file instead of making network request
    with open("data/html/tulsa-CJ-2024-3204.html", "r", encoding="utf-8") as f:
        html = f.read()

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

    # Verify parties contains expected data (using local data)
    assert len(parties) > 0  # Should have at least one party
