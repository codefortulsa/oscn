import oscn
import time
from oscn.parse.lax_counts import counts
from oscn.parse.bs4_counts import bs4_counts

def test_counts():

    cases = oscn.request.CaseList(
        types=["CF", "CM"],
        counties=["tulsa", "oklahoma", "bexar"],
        years=["2024", "2020"],
        start=4,
        stop=6,
    )    
    total_diff_percentage = 0
    total_cases = 0

    for case in cases:
        start_time_bs4 = time.perf_counter()
        bs4_result = bs4_counts(case.text)
        end_time_bs4 = time.perf_counter()
        bs4_time = end_time_bs4 - start_time_bs4

        start_time_lax = time.perf_counter()
        lax_result = counts(case.text)
        end_time_lax = time.perf_counter()
        lax_time = end_time_lax - start_time_lax

        time_diff_percentage = abs(bs4_time - lax_time) / ((bs4_time + lax_time) / 2) * 100
        total_diff_percentage += time_diff_percentage
        total_cases += 1

        print(f"Case {case.index} - BS4 Time: {bs4_time:.4f}s, Lax Time: {lax_time:.4f}s, Difference: {time_diff_percentage:.2f}%")
        
        # Extract the keys to compare from both results
        keys_to_check = ["party", "offense", "disposed", "violation"]

        for key in keys_to_check:
            bs4_values = [item[key] for item in bs4_result if key in item]
            lax_values = [item[key] for item in lax_result if key in item]
            assert bs4_values == lax_values, f"Mismatch in key '{key}' for case {case.index}"
    
    average_diff_percentage = total_diff_percentage / total_cases if total_cases > 0 else 0
    print(f"\nAverage Difference in Processing Time: {average_diff_percentage:.2f}%")
