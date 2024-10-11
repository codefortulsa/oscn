import oscn
import time

from oscn import settings
from oscn.parse.lax_docket import docket
from oscn.parse.bs4_docket import bs4_docket

OSCN_HEADER = settings.OSCN_REQUEST_HEADER

def test_lax_versus_bs4():
    cases = oscn.request.CaseList(
        types=["CJ", "CM"],
        counties=["tulsa", "oklahoma", "cleveland", "texas", "bexar"],
        years=["2024", "2018"],
        start=4,
        stop=5,
    )

    total_lax_time = 0
    total_bs4_time = 0
    for case in cases:
        # Measure BS4 parsing time
        start_time = time.time()
        bs4_result = bs4_docket(case.text)
        bs4_duration = time.time() - start_time

        # Measure LAX parsing time
        start_time = time.time()
        lax_result = docket(case.text)
        lax_duration = time.time() - start_time

        total_bs4_time += bs4_duration

        # Accumulate total LAX time
        total_lax_time += lax_duration

        # Calculate percentage difference
        if bs4_duration > 0:
            percentage = (lax_duration / bs4_duration) * 100
        else:
            percentage = float('inf')  # Handle division by zero if bs4_duration is zero
        print("." * 100)
        print(f"Case: {case.source}")
        # print(f"BS4 Result: {bs4_result}")
        # print(f"LAX Result: {lax_result}")
        # print(f"BS4 Time: {bs4_duration:.6f} seconds")
        # print(f"LAX Time: {lax_duration:.6f} seconds")
        print(f"LAX is {percentage:.2f}% of BS4 time")
        
        # Ensure both results have the same number of rows
        assert len(bs4_result) == len(lax_result)
        
        # Compare each row
        for bs4_row, lax_row in zip(bs4_result, lax_result):            
            assert bs4_row['date']==lax_row['date']
            assert bs4_row['code']==lax_row['code']
            assert bs4_row['description']==lax_row['description']
            assert bs4_row['count']==lax_row['count']
            assert bs4_row['party']==lax_row['party']
            assert bs4_row['amount']==lax_row['amount']
            
        # Check if lax_result matches the case docket
        assert lax_result == case.docket
        
    print("=" * 100)
    print(f"Total BS4 Time: {total_bs4_time:.6f} seconds")
    print(f"Total LAX Time: {total_lax_time:.6f} seconds")
            # Calculate percentage difference
    if total_bs4_time > 0:
        total_percentage = (total_lax_time / total_bs4_time) * 100
    else:
        total_percentage = float('inf')  # Handle division by zero if bs4_duration is zero
    print(f"Total LAX is {total_percentage:.2f}% of BS4 time")
