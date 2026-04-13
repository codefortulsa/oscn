"""
Unit tests for oscn.parse.events.get_events().

These tests exercise get_events() directly with synthetic payloads so they
run offline without touching OSCN.
"""
import pytest
from oscn.parse.events import get_events


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_json_payload(events: list[dict]) -> str:
    """Wrap a list of event dicts in a minimal JSON structure matching OSCN."""
    import json
    return json.dumps({"Events": events})


def make_raw_payload(events: list[dict]) -> str:
    """
    Build a deliberately non-parseable (malformed JSON) payload that still
    contains recognizable "date" and "description" keys, to exercise the
    regex fallback path.
    """
    parts = []
    for ev in events:
        # Use single quotes so json.loads will fail
        parts.append(
            '{\'date\': "' + ev["date"] + '", '
            '"description": "' + ev["description"] + '"}'
        )
    return "[" + ", ".join(parts) + "]"


# ---------------------------------------------------------------------------
# JSON parse path
# ---------------------------------------------------------------------------

class TestJsonPath:
    def test_single_event(self):
        payload = make_json_payload([
            {"date": "Monday, January 1, 2024 at 9:00 AM", "description": "Hearing"}
        ])
        result = get_events(payload)
        assert len(result) == 1
        assert result[0]["date"] == "Monday, January 1, 2024 at 9:00 AM"
        assert result[0]["description"] == "Hearing"

    def test_multiple_events_normal_descriptions(self):
        payload = make_json_payload([
            {"date": "Wednesday, May 25, 2022 at 9:30 AM", "description": "Parenting Plan Conference"},
            {"date": "Thursday, January 5, 2017 at 9:00 AM", "description": "Status Conference"},
        ])
        result = get_events(payload)
        assert len(result) == 2
        assert result[0]["description"] == "Parenting Plan Conference"
        assert result[1]["description"] == "Status Conference"

    def test_multiline_description_via_json(self):
        import json
        payload = json.dumps({
            "Events": [
                {"date": "Friday, April 24, 2026 at 2:30 PM", "description": "Jury Trial\nDay 2"},
                {"date": "Thursday, August 6, 2026 at 9:00 AM", "description": "Sentencing"},
            ]
        })
        result = get_events(payload)
        assert len(result) == 2
        # Internal newline in description should be collapsed to a space
        assert result[0]["description"] == "Jury Trial Day 2"
        assert result[1]["date"] == "Thursday, August 6, 2026 at 9:00 AM"

    def test_description_with_apostrophe(self):
        import json
        payload = json.dumps({
            "Events": [
                {"date": "Monday, March 3, 2025 at 10:00 AM",
                 "description": "Plaintiff's Motion\nHearing"},
            ]
        })
        result = get_events(payload)
        assert len(result) == 1
        assert "Plaintiff" in result[0]["description"]

    def test_nine_events_none_dropped(self):
        """Regression: ensure all 9 events are returned even with multiline descriptions."""
        import json
        events_data = [
            {"date": f"Day {i}", "description": f"Event {i}"}
            for i in range(7)
        ]
        # Add the two future events that were previously dropped
        events_data.append({"date": "Friday, April 24, 2026 at 2:30 PM", "description": "Jury Trial"})
        events_data.append({"date": "Thursday, August 6, 2026 at 9:00 AM", "description": "Sentencing"})
        payload = json.dumps({"Events": events_data})
        result = get_events(payload)
        assert len(result) == 9
        dates = [ev["date"] for ev in result]
        assert "Friday, April 24, 2026 at 2:30 PM" in dates
        assert "Thursday, August 6, 2026 at 9:00 AM" in dates


# ---------------------------------------------------------------------------
# Regex fallback path (malformed / non-JSON payload)
# ---------------------------------------------------------------------------

class TestRegexFallback:
    def _malformed(self, events: list[dict]) -> str:
        """
        Produce a payload that json.loads will reject but that contains
        properly quoted "date" and "description" keys per object.
        """
        parts = []
        for ev in events:
            desc = ev["description"].replace('"', '\\"')
            parts.append(
                '{"date": "' + ev["date"] + '", '
                '"description": "' + desc + '"}'
            )
        # Wrap in an outer structure that isn't valid JSON (unquoted key)
        return 'Events: [' + ", ".join(parts) + ']'

    def test_single_event_fallback(self):
        payload = self._malformed([
            {"date": "Monday, January 1, 2024 at 9:00 AM", "description": "Hearing"}
        ])
        result = get_events(payload)
        assert len(result) == 1
        assert result[0]["date"] == "Monday, January 1, 2024 at 9:00 AM"
        assert result[0]["description"] == "Hearing"

    def test_multiline_description_fallback(self):
        """Multiline descriptions must not cause count mismatch in fallback path."""
        parts = [
            '{"date": "Friday, April 24, 2026 at 2:30 PM", "description": "Jury Trial\nDay 2"}',
            '{"date": "Thursday, August 6, 2026 at 9:00 AM", "description": "Sentencing"}',
        ]
        payload = 'Events: [' + ', '.join(parts) + ']'
        result = get_events(payload)
        assert len(result) == 2
        assert result[0]["date"] == "Friday, April 24, 2026 at 2:30 PM"
        assert result[1]["date"] == "Thursday, August 6, 2026 at 9:00 AM"
        # Newline in description collapsed to space
        assert result[0]["description"] == "Jury Trial Day 2"

    def test_apostrophe_and_newline_fallback(self):
        parts = [
            '{"date": "Monday, March 3, 2025 at 10:00 AM", "description": "Plaintiff\'s Motion\\nHearing"}',
        ]
        payload = 'Events: [' + ', '.join(parts) + ']'
        result = get_events(payload)
        assert len(result) == 1
        assert "Plaintiff" in result[0]["description"]

    def test_seven_plus_two_regression_fallback(self):
        """
        Regression for tulsa-FD-2025-458: 7 normal events + 2 future events
        where 2 descriptions are multiline — all 9 must be returned.
        """
        normal = [
            '{"date": "Day ' + str(i) + '", "description": "Event ' + str(i) + '"}'
            for i in range(7)
        ]
        future = [
            '{"date": "Friday, April 24, 2026 at 2:30 PM", "description": "Jury Trial\nContinued"}',
            '{"date": "Thursday, August 6, 2026 at 9:00 AM", "description": "Sentencing\nHearing"}',
        ]
        payload = 'Events: [' + ', '.join(normal + future) + ']'
        result = get_events(payload)
        assert len(result) == 9
        dates = [ev["date"] for ev in result]
        assert "Friday, April 24, 2026 at 2:30 PM" in dates
        assert "Thursday, August 6, 2026 at 9:00 AM" in dates


# ---------------------------------------------------------------------------
# Regression: simulate tulsa-FD-2025-458 fixture via proper JSON
# ---------------------------------------------------------------------------

class TestTulsaFD2025458Regression:
    """
    Simulates the tulsa-FD-2025-458 payload shape: 9 events, last 2 future,
    some descriptions containing raw newlines that broke the old zip() approach.
    """

    def _build_payload(self) -> str:
        import json
        events_data = [
            {"date": "Wednesday, May 25, 2022 at 9:30 AM", "description": "Parenting Plan Conference"},
            {"date": "Thursday, January 5, 2023 at 9:00 AM", "description": "Status Conference"},
            {"date": "Monday, March 6, 2023 at 1:00 PM", "description": "Hearing"},
            {"date": "Tuesday, June 13, 2023 at 2:00 PM", "description": "Mediation"},
            {"date": "Friday, September 15, 2023 at 10:00 AM", "description": "Pre-Trial"},
            {"date": "Monday, December 4, 2023 at 9:00 AM", "description": "Motion Hearing"},
            {"date": "Thursday, February 29, 2024 at 3:00 PM", "description": "Review Hearing"},
            # These two had multiline descriptions causing zip() to drop them
            {"date": "Friday, April 24, 2026 at 2:30 PM", "description": "Jury Trial\nDay 1 of 3"},
            {"date": "Thursday, August 6, 2026 at 9:00 AM", "description": "Final Sentencing\nHearing"},
        ]
        return json.dumps({"Events": events_data})

    def test_returns_nine_events(self):
        result = get_events(self._build_payload())
        assert len(result) == 9

    def test_april_2026_present(self):
        result = get_events(self._build_payload())
        dates = [ev["date"] for ev in result]
        assert "Friday, April 24, 2026 at 2:30 PM" in dates

    def test_august_2026_present(self):
        result = get_events(self._build_payload())
        dates = [ev["date"] for ev in result]
        assert "Thursday, August 6, 2026 at 9:00 AM" in dates

    def test_descriptions_collapsed(self):
        result = get_events(self._build_payload())
        april = next(ev for ev in result if "April 24" in ev["date"])
        assert april["description"] == "Jury Trial Day 1 of 3"
