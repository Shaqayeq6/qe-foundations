# qe-foundations

A Python project with reusable utilities for building and checking QA test data.

## Project 1 milestone - Week 2, Monday

Completed: utility package, virtual environment setup, dependency files,
smoke checks, documentation, and placeholders for data and tests.

Coming next:
- Tuesday: data ingestion.
- Wednesday: logging and unit tests.
- Thursday: SQL validation queries.
- Friday: joins validation and integration.

## Setup

1. Open a terminal in the project root.

2. Create a virtual environment:

   ```text
   python -m venv .venv
   ```

3. Activate it.

   PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   bash on Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   Git Bash on Windows:

   ```bash
   source .venv/Scripts/activate
   ```

4. Install runtime dependencies:

   ```text
   python -m pip install -r requirements.txt
   ```

   For development, install:

   ```text
   python -m pip install -r requirements-dev.txt
   ```

5. Verify the utilities:

   ```text
   python smoke_utils.py
   ```

   Expected result: 7/7 checks passed.

## Usage

Run Python from the project root:

```python
from qe_foundations.utils import slugify, mask_email

print(slugify("  Login Page: Happy Path "))
print(mask_email("tester@example.com"))
```

Output:

```text
login-page-happy-path
t***@example.com
```