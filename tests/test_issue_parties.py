"""Regression tests for per-issue party/disposition extraction in
oscn.parse.issues.

These run OFFLINE — they feed hand-built OSCN-shaped HTML straight to the
parser, so no live oscn.net call is made. They pin two behaviors the old
suite never asserted:

  1. A disposition row whose party-NAME cell is blank but whose disposition
     cell carries a value (e.g. "Pending.") must NOT be dropped — the prior
     `if not name_detail_text: continue` discarded it, yielding parties:[].
  2. Each party name must stay paired with the disposition in its OWN row
     (the prior positional `zip(name_details, dispositions)` could mis-pair).
"""

import oscn


def _case_html(disposition_rows):
    """Wrap disposition <tr> rows in the minimal scaffold the parser needs:
    an Issues header + issue table (rich layout, has "Issue #"), the
    Disposition table, then a Dockets header + table so docket_table is
    distinct from the issue/disposition tables."""
    return f"""
    <h2 class="section issues">Issues</h2>
    <table>
      <tr>
        <td valign="top" width="100px"><strong>Issue # 1.</strong></td>
        <td>Issue: BREACH OF AGREEMENT - CONTRACT (CONTRACT)<br>
            Filed By: Discover Bank<br>Filed Date: 06/27/2024<br></td>
      </tr>
    </table>
    <table class="Disposition">
      <thead>
        <tr><th class="paddedContainer"></th>
            <th class="partyName">Party Name</th>
            <th class="dispositionInformation">Disposition Information</th></tr>
      </thead>
      <tbody>
        {disposition_rows}
      </tbody>
    </table>
    <h2 class="section dockets">Dockets</h2>
    <table><tr><td>Docket</td></tr></table>
    """


PITTSER_ROW = (
    '<tr><td width="100px"></td>'
    '<td class="countpartyname" width="20%" valign="top">'
    "<strong><u></u></strong>&nbsp;<nobr></nobr></td>"
    '<td class="countdisposition" valign="top">Pending.</td></tr>'
)

NAMED_PENDING_ROW = (
    '<tr><td></td>'
    '<td class="countpartyname" width="20%" valign="top">'
    "<strong><u>Defendant:</u></strong>&nbsp;<nobr>WHITE, PAMELA M</nobr></td>"
    '<td class="countdisposition" valign="top"></td></tr>'
)

NAMED_DISPOSED_ROW = (
    '<tr><td></td>'
    '<td class="countpartyname" width="20%" valign="top">'
    "<strong><u>Defendant:</u></strong>&nbsp;<nobr>SMITH, JOHN</nobr></td>"
    '<td class="countdisposition" valign="top">'
    '<font color="red"><strong>Disposed: DEFAULT JUDGEMENT, 01/23/2025. '
    "Default Judgment</strong></font></td></tr>"
)

EMPTY_ROW = (
    '<tr><td></td>'
    '<td class="countpartyname"></td>'
    '<td class="countdisposition"></td></tr>'
)


def _parties(rows):
    issues = oscn.parse.issues(_case_html(rows))
    assert len(issues) == 1
    return issues[0]["parties"]


def test_blank_name_with_disposition_is_kept():
    """The Pittser regression: empty name cell, 'Pending.' disposition."""
    parties = _parties(PITTSER_ROW)
    assert len(parties) == 1
    assert parties[0]["name"] == ""
    assert parties[0]["disposed"] == "Pending."


def test_named_party_blank_disposition():
    parties = _parties(NAMED_PENDING_ROW)
    assert len(parties) == 1
    assert parties[0]["type"] == "defendant"
    assert parties[0]["name"] == "WHITE, PAMELA M"
    assert parties[0]["disposed"] == ""


def test_disposed_prefix_is_stripped():
    parties = _parties(NAMED_DISPOSED_ROW)
    assert len(parties) == 1
    assert parties[0]["name"] == "SMITH, JOHN"
    assert parties[0]["disposed"].startswith("DEFAULT JUDGEMENT")
    assert "Disposed:" not in parties[0]["disposed"]


def test_rows_stay_paired():
    """A disposed named party AND a blank-name pending row in one table:
    each disposition must stay with its own row (guards the old zip mis-pair
    and the dropped-blank-name row)."""
    parties = _parties(NAMED_DISPOSED_ROW + PITTSER_ROW)
    assert len(parties) == 2
    assert parties[0]["name"] == "SMITH, JOHN"
    assert parties[0]["disposed"].startswith("DEFAULT JUDGEMENT")
    assert parties[1]["name"] == ""
    assert parties[1]["disposed"] == "Pending."


def test_empty_row_yields_no_party():
    assert _parties(EMPTY_ROW) == []
    # A spacer row alongside a real row must not add a phantom party.
    parties = _parties(EMPTY_ROW + PITTSER_ROW)
    assert len(parties) == 1
    assert parties[0]["disposed"] == "Pending."
