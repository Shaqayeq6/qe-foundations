# Expected-defect checklist (fill in as you go)

<!--
PURPOSE: this is your "answer sheet" for the data. Writing the PREDICTION before you run a
query is the single best habit for catching false passes.
HOW: for each rule, (1) write what you EXPECT in the "Predicted" column BEFORE running the
query, (2) run it, (3) write the run_ids it actually returned in "Defects found (run_ids)"
(comma-separated, 4-digit ids), (4) note anything surprising. Do not delete rows.
check_exercise.py compares this table with what your queries return.
-->

| Rule | Defects found (run_ids) | Predicted (before running) | Notes / surprises |
|---|---|---|---|
| R-01 | 5006, 5019, 5025 | Not recorded before running | NULL, empty text and spaces-only text all count as missing. |
| R-02 | 5011, 5022 | 5011, 5022 | Results matched prediction: missing @ or missing a dot after @. |
| R-03 | 5008, 5014, 5027, 5029 | 5008, 5014, 5027, 5029 | Extra whitespace was difficult to see; LENGTH revealed it. |
| R-04 | 5009, 5016 | 5009, 5016 | Negative and NULL durations are invalid; zero is legal. |
| R-05 | 5030, 5023 | 5023, 5030 | Prediction match even though the order is different. |
| R-06 | 5013, 5020 | Check for values not in between 0 and 3 and NULL | Prediction matched. Check if NULL values are present alongside. |
| R-07 | 5017, 5024, 5026 | 5017, 5024, 5026 | Prediction matched. Check for NULL, correct environment names, case-insensitive. |
| R-08 | 5014, 5018, 5028 | 5014, 5018, 5028 | Prediction matched. Check whether whitespaces are visually difficult to identify. |
| R-09 | | | |
| R-10 | | | |
| R-11 | | | |
| R-12 | | | |

## Decoys: rows that look odd but are LEGAL (we must not flag them)

<!-- List at least two run_ids and say why they are fine, e.g. "run 5xxx: SKIPPED with 0 ms -- skipped tests take no time." -->

- Run 5004: SKIPPED with duration_ms = 0. Zero is legal under R-04.
- Run 5041: duration_ms = 600000. R-05 flags only values above 600000.

## Rows reported by more than one rule

<!-- Which run_ids appear in two or more rules? Is that OK? (Each rule must be testable on its own.) -->

No overlapping run_ids among R-01 to R-04. Recheck after completing all rules.
A row may violate multiple rules because each rule is checked independently.

## Open questions for the product owner

<!-- Rules that are really business decisions (like "is a price of 0 allowed?" in the lesson). -->

- Should durations above 600000 ms always fail validation, or trigger a review warning?
- Should malformed emails be rejected when submitted or accepted and flagged later