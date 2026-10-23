# Ingestion module - design notes (Week 2, Day 2)

Answer in your own words, 2-4 sentences each. Replace every line that starts with
. (Delete nothing else.)

## 1. Exceptions or assertions?
In `validate_record` I raise exceptions for a negative duration, but in
`IngestionReport.check_invariants` I use `assert`. Why is each the right tool there?

A negative duration comes from bad input, so I use an exception to reject it. I use assertions to check that my own code is keeping track of records correctly. Input validation must always run, but assertions can be turned off with python -O.

## 2. Stop or collect?
Why is a malformed JSON file a `SourceError` that stops loading, while a record with
a bad status is a `RecordValidationError` that is collected? Who benefits from this split?

If a JSON file is malformed, the program cannot read its records properly, so it stops loading that file. A bad status only affects one record, so we can reject that record and keep the others. This lets the user keep the good data and see what needs fixing.

## 3. What did the context managers buy you?
Name two things that `open_source` / `LoadSession` do for the caller that you would otherwise
have to remember to do at every call site.

open_source closes the file even if something goes wrong, so I do not have to remember to close it myself. LoadSession tracks how long loading takes and whether it succeeds or fails. Both save me from repeating the same code.

## 4. Your hardest bad-input case
The boolean duration in the JSON data was confusing because Python treats True as a number and converts it to 1.0. I had to check for booleans before converting the duration. Without that check, the program would accept a value that should be rejected.


