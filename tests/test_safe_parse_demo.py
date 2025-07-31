import logging
import oscn


def safe_parse(fn, html):
    """Safe parsing function that handles errors and returns default values"""
    try:
        return fn(html) if html else fn._default_value
    except Exception as e:
        logging.error(f"Error parsing with {fn.__name__}: {e}")
        return "" if fn.__name__ == "judge" else fn._default_value


def test_exact_usage_pattern():
    """Test the exact usage pattern mentioned by the user"""
    # Load local HTML file instead of making network request
    with open("data/html/tulsa-CJ-2024-3204.html", "r", encoding="utf-8") as f:
        html = f.read()

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

    # Verify parties contains expected data (using local data)
    assert len(parties) > 0  # Should have at least one party

    print("✅ All three functions work with safe_parse:")
    print(f"  - issues: {type(issues)} with {len(issues)} items")
    print(f"  - counts: {type(counts)} with {len(counts)} items")
    print(f"  - parties: {type(parties)} with {len(parties)} items")


def test_default_values_work():
    """Test that default values are returned when HTML is None or empty"""

    # Test with None HTML
    issues_none = safe_parse(oscn.parse.issues, None)
    counts_none = safe_parse(oscn.parse.counts, None)
    parties_none = safe_parse(oscn.parse.parties, None)

    assert issues_none == []
    assert counts_none == []
    assert parties_none == []

    # Test with empty HTML
    issues_empty = safe_parse(oscn.parse.issues, "")
    counts_empty = safe_parse(oscn.parse.counts, "")
    parties_empty = safe_parse(oscn.parse.parties, "")

    assert issues_empty == []
    assert counts_empty == []
    assert parties_empty == []

    print("✅ Default values work correctly for None/empty HTML")


def test_functions_are_accessible():
    """Test that the functions are accessible from oscn.parse namespace"""

    # Verify functions exist in the namespace
    assert hasattr(oscn.parse, "issues")
    assert hasattr(oscn.parse, "counts")
    assert hasattr(oscn.parse, "parties")

    # Verify they have _default_value attributes
    assert hasattr(oscn.parse.issues, "_default_value")
    assert hasattr(oscn.parse.counts, "_default_value")
    assert hasattr(oscn.parse.parties, "_default_value")

    print("✅ All functions are accessible from oscn.parse namespace")
    print(f"  - oscn.parse.issues._default_value: {oscn.parse.issues._default_value}")
    print(f"  - oscn.parse.counts._default_value: {oscn.parse.counts._default_value}")
    print(f"  - oscn.parse.parties._default_value: {oscn.parse.parties._default_value}")


if __name__ == "__main__":
    test_exact_usage_pattern()
    test_default_values_work()
    test_functions_are_accessible()
    print(
        "\n🎉 All tests passed! The safe_parse function works correctly with the renamed parser functions."
    )
