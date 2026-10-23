# Retrospective

## What worked well

We both contributed to the shared branch under our own names.
The project combined SQL rules with a Python runner, custom exceptions,
logging and unit tests. Running individual rules made it easier to
inspect evidence before checking the complete suite.

## What was difficult

R-09 was initially confused with R-10. Checking whether a run finishes
before it starts does not check timestamp format. Another difficulty
was editing test_validation.py inside starter_code while Python executed
the file inside qe_foundations/tests. The unchanged TODO failures helped
us identify the incorrect file location.

## What we learned

A violation query returns bad rows, so zero rows means the rule passes.
An expectation query passes when its expected row count matches.
NULL requires explicit handling because NOT IN alone does not catch it.
Zero-duration skipped runs are legal and must not be reported as defects.
Whitespace can also make a value invalid even when it looks correct
in the terminal.

## Testing and debugging

We replaced the unfinished test stubs and obtained seven passing tests.
The tests cover exception evidence, known bad durations, missing expected
rows and legal zero-duration runs. We corrected R-09 to check both
timestamp columns for missing values and incorrect shape. We also added
DEBUG logging for each query while keeping the console handler at INFO.

## Collaboration and improvements

Shaqayeq drove Blocks 1, 3 and 5, while Vanella drove Blocks 2 and 4.
We contributed commits to the shared feature branch.
The pairing log was reconstructed afterward because exact swap times
were not recorded. Next time, we should document handoffs immediately,
record predictions before running queries and confirm the active file
path before editing.

## Final review

All fourteen SQL rules passed their checks, and all seven unit tests
passed. The runner checks also confirmed logging, evidence output and
exit-code behavior. After completing the documentation, we will rerun
the checker, review the documents together and submit the reviewed
pull request.