import pytest
from oscn.parse.lax_counts import counts
from oscn.request.cases import Case


def test_counts_by_case_type():
    """Test that counts are found in CM and CF cases but not in CJ cases"""

    # Test cases with different case types
    test_cases = [
        # CM cases (should have counts)
        ("tulsa-CM-2024-3974", "CM"),
        ("oklahoma-CM-2024-3843", "CM"),
        # CF cases (should have counts)
        ("cleveland-CF-2024-280", "CF"),
        ("tulsa-CF-2024-1583", "CF"),
        ("oklahoma-CF-2024-2093", "CF"),
        # CJ cases (should not have counts)
        ("cleveland-CJ-2024-1543", "CJ"),
        ("tulsa-CJ-2024-3204", "CJ"),
        ("oklahoma-CJ-2024-3069", "CJ"),
    ]

    for case_id, expected_type in test_cases:
        # Load the case HTML
        case = Case(case_id)

        # Parse counts
        counts_result = counts(case.text)

        if expected_type in ["CM", "CF"]:
            # Criminal cases should have counts
            assert (
                len(counts_result) > 0
            ), f"Case {case_id} ({expected_type}) should have counts but found none"
            print(f"✅ {case_id} ({expected_type}): Found {len(counts_result)} counts")

            # Verify count structure
            for count in counts_result:
                assert isinstance(
                    count, dict
                ), f"Count should be a dictionary in {case_id}"
                # All counts should have at least a description
                assert (
                    "description" in count
                ), f"Count missing 'description' key in {case_id}"
                # Check for other expected keys (some may be empty strings or missing)
                expected_keys = ["party", "offense", "disposed", "violation"]
                for key in expected_keys:
                    if key not in count:
                        print(f"  Warning: Count missing key '{key}' in {case_id}")

        else:  # CJ cases
            # Civil cases should not have counts
            assert (
                len(counts_result) == 0
            ), f"Case {case_id} ({expected_type}) should not have counts but found {len(counts_result)}"
            print(f"✅ {case_id} ({expected_type}): Correctly has no counts")


def test_counts_structure_for_criminal_cases():
    """Test that criminal cases have properly structured count data"""

    criminal_cases = [
        "tulsa-CF-2024-1583",  # Known to have counts
        "oklahoma-CM-2024-3843",  # Known to have counts
        "tulsa-CM-2024-3974",  # Known to have counts
    ]

    for case_id in criminal_cases:
        case = Case(case_id)
        counts_result = counts(case.text)

        assert len(counts_result) > 0, f"Case {case_id} should have counts"

        # Check that at least one count has meaningful data
        meaningful_counts = 0
        for count in counts_result:
            if count.get("description") and count.get("description").strip():
                meaningful_counts += 1

        assert (
            meaningful_counts > 0
        ), f"Case {case_id} should have at least one count with description"

        print(
            f"✅ {case_id}: Found {len(counts_result)} counts with {meaningful_counts} meaningful descriptions"
        )


def test_civil_cases_no_counts():
    """Test that civil cases consistently have no counts"""

    civil_cases = [
        "cleveland-CJ-2024-1543",
        "tulsa-CJ-2024-3204",
        "oklahoma-CJ-2024-3069",
        "cleveland-CS-2024-1154",  # Civil Small Claims
        "tulsa-CS-2024-2897",  # Civil Small Claims
    ]

    for case_id in civil_cases:
        case = Case(case_id)
        counts_result = counts(case.text)

        assert (
            len(counts_result) == 0
        ), f"Civil case {case_id} should have no counts but found {len(counts_result)}"
        print(f"✅ {case_id}: Correctly has no counts")


if __name__ == "__main__":
    # Run the tests
    test_counts_by_case_type()
    test_counts_structure_for_criminal_cases()
    test_civil_cases_no_counts()
    print("\n🎉 All tests passed!")
