import oscn
import time
from oscn.parse.lax_issues import issues
from oscn.parse.bs4_issues import bs4_issues


def test_counts():

    cases = oscn.request.CaseList(
        types=["CJ", "SC"],
        counties=["oklahoma", "bexar", "tulsa"],
        years=["2024", "2020"],
        start=4,
        stop=6,
    )
    total_diff_percentage = 0
    total_cases = 0

    for case in cases:
        print(f"source: {case.source}")
        bs4_text = case.text
        start_time_bs4 = time.perf_counter()
        bs4_result = bs4_issues(bs4_text)
        end_time_bs4 = time.perf_counter()
        bs4_time = end_time_bs4 - start_time_bs4

        lax_text = case.text
        start_time_lax = time.perf_counter()
        lax_result = issues(lax_text)
        end_time_lax = time.perf_counter()
        lax_time = end_time_lax - start_time_lax

        time_diff_percentage = (bs4_time - lax_time) / ((bs4_time + lax_time) / 2) * 100
        total_diff_percentage += time_diff_percentage
        total_cases += 1
        print(f"bs4 issues: {bs4_result}")
        print(f"lax issues: {lax_result}")
        print(
            f"Case {case.index} - BS4: {bs4_time:.4f}s, LAX: {lax_time:.4f}s, DIFF: {(lax_time-bs4_time):.4f} PCT:{time_diff_percentage:.2f}%"
        )
        assert bs4_result == lax_result

    average_diff_percentage = (
        total_diff_percentage / total_cases if total_cases > 0 else 0
    )
    print(f"\nAverage Difference in Processing Time: {average_diff_percentage:.2f}%")
