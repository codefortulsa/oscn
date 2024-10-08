import oscn
import time

from oscn import settings
from oscn.parse.lax_events import events
from oscn.parse.bs4_events import bs4_events

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

    for case in cases:
        # Measure BS4 parsing time
        start_time = time.time()
        bs4_result = bs4_events(case.text)
        bs4_duration = time.time() - start_time

        # Measure LAX parsing time
        start_time = time.time()
        lax_result = events(case.text)
        lax_duration = time.time() - start_time

        # Accumulate total LAX time
        total_lax_time += lax_duration

        # Calculate percentage difference
        if bs4_duration > 0:
            percentage = (lax_duration / bs4_duration) * 100
        else:
            percentage = float('inf')  # Handle division by zero if bs4_duration is zero

        print("." * 100)
        print(f"Case: {case.source}")
        print(f"BS4 Result: {bs4_result}")
        print("." * 100)
        print(f"LAX Result: {lax_result}")
        print("." * 100)
        print(f"BS4 Time: {bs4_duration:.6f} seconds")
        print(f"LAX Time: {lax_duration:.6f} seconds")
        print(f"LAX is {percentage:.2f}% of BS4 time")
        assert bs4_result == lax_result
    print("=" * 100)
    print(f"Total LAX Time: {total_lax_time:.6f} seconds")
    