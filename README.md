# Traffic Counter

A Python command-line program that reads traffic counter data and produces four analyses:

1. **Total car count** across all recorded half-hour periods
2. **Daily totals** sorted by date
3. **Top 3 busiest half-hours** by car count
4. **Least busy 1.5-hour window** (3 consecutive records with the lowest combined count)

## Input Format

A plain-text file where each line contains an ISO 8601 timestamp and a car count separated by a space:

```
2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
2021-12-01T06:00:00 14
```

Each line represents the number of cars seen in that half-hour period. Blank lines are ignored.

## Example Output

Given the sample data in `data/sample.txt`:

```
398

2021-12-01 179
2021-12-05 81
2021-12-08 134
2021-12-09 4

2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-08T17:00:00 33

2021-12-01T15:00:00 9
2021-12-01T15:30:00 11
2021-12-01T23:30:00 0
```

The four sections (separated by blank lines) are:
1. Total cars counted: **398**
2. Cars per day, sorted by date
3. Top 3 half-hours with the most cars
4. The contiguous 1.5-hour period (3 consecutive records) with the fewest total cars

## Tech Stack

- **Python 3.10+** — uses modern features including type hints, `datetime.fromisoformat()`, `dataclasses` with `slots=True`, union types (`X | None`), and `pathlib.Path`
- **pytest** — the only external dependency, used for testing

No third-party runtime libraries are required. The program uses only the Python standard library.

## Project Structure

```
Seek-assessment/
├── pyproject.toml                # Project metadata, dependencies, pytest config, entry point
├── data/
│   └── sample.txt                # Sample input file (23 half-hour records across 4 days)
├── traffic_counter/              # Main application package
│   ├── __init__.py
│   ├── models.py                 # TrafficRecord dataclass
│   ├── parser.py                 # File and line parsing
│   ├── analysis.py               # Four analysis functions
│   ├── formatter.py              # Output formatting
│   └── main.py                   # CLI entry point
└── tests/                        # Test suite (24 tests)
    ├── __init__.py
    ├── conftest.py               # Shared pytest fixtures
    ├── test_parser.py            # Parsing tests
    ├── test_analysis.py          # Analysis function tests
    ├── test_formatter.py         # Formatting tests
    └── test_main.py              # End-to-end integration tests
```

## File Descriptions

### Source Code (`traffic_counter/`)

#### `models.py`
Defines `TrafficRecord`, a frozen and slotted dataclass with two fields:
- `timestamp` (`datetime`) — the start of the half-hour period
- `count` (`int`) — number of cars observed

Frozen makes instances immutable (hashable, safe to share). Slots reduce memory overhead.

#### `parser.py`
Two functions for reading input data:
- `parse_line(line)` — splits a single line into its timestamp and count, returns a `TrafficRecord`
- `parse_file(path)` — reads a file line by line, skips blank lines, returns a list of `TrafficRecord`

Uses `datetime.fromisoformat()` for timestamp parsing and `pathlib.Path` for file paths.

#### `analysis.py`
Four pure functions, each taking a list of `TrafficRecord`:
- `total_count(records)` — sums all counts using a generator expression
- `daily_counts(records)` — aggregates counts by date using `defaultdict(int)`, returns sorted `(date_string, total)` tuples
- `top_half_hours(records, n=3)` — sorts by count descending, returns the top `n` records
- `least_traffic_period(records, window=3)` — uses a sliding window (O(n)) to find the `window` consecutive records with the smallest combined count

#### `formatter.py`
Converts analysis results into the output string:
- `format_total(total)` — integer to string
- `format_daily(daily)` — date-count pairs, one per line
- `format_records(records)` — ISO timestamp and count, one per line
- `format_report(total, daily, top, least)` — joins all four sections with blank lines

#### `main.py`
CLI entry point using `argparse`. Accepts a file path as a positional argument, parses the file, runs all four analyses, formats the report, and prints it to stdout. Exits with an error message to stderr if the file is not found.

Can be invoked as a module (`python -m traffic_counter.main`) or as an installed script (`traffic-counter`).

### Test Suite (`tests/`)

#### `conftest.py`
Shared pytest fixtures:
- `sample_records` — the full set of 23 `TrafficRecord` objects matching `data/sample.txt`
- `sample_file` — a small temporary file with 3 records for parser tests

#### `test_parser.py` (5 tests)
- Parsing a normal line, a line with zero count, and a line with extra whitespace
- Parsing a complete file and verifying record count and values
- Verifying blank lines are skipped

#### `test_analysis.py` (12 tests)
- `total_count`: sample data (expects 398) and empty input
- `daily_counts`: sample data (verifies all 4 days and totals) and empty input
- `top_half_hours`: sample data (verifies top 3 counts), empty input, fewer records than requested, custom `n` parameter
- `least_traffic_period`: sample data (expects counts [9, 11, 0]), empty input, fewer records than window size, custom window size

#### `test_formatter.py` (5 tests)
- Total formatting, daily formatting, record formatting
- Report has 4 sections separated by blank lines
- Report ends with a trailing newline

#### `test_main.py` (2 tests)
- End-to-end: runs `main()` against `data/sample.txt` and asserts the full output string matches expected output
- Missing file: verifies `SystemExit` is raised for a nonexistent path

## Getting Started

### Prerequisites

- Python 3.10 or later

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Seek-assessment

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the project with dev dependencies
pip install -e ".[dev]"
```

### Run the Program

```bash
# Using the module
python -m traffic_counter.main data/sample.txt

# Or using the installed entry point
traffic-counter data/sample.txt

# With your own data file
python -m traffic_counter.main /path/to/your/data.txt
```

### Run Tests

```bash
# Run all 24 tests
pytest

# Verbose output
pytest -v
```

## Algorithms

| Analysis | Approach | Complexity |
|---|---|---|
| Total count | Generator sum | O(n) |
| Daily totals | `defaultdict(int)` + sorted output | O(n log n) |
| Top 3 half-hours | Sort descending, take first 3 | O(n log n) |
| Least 1.5hr period | Sliding window of size 3 | O(n) |

The sliding window for the least-traffic period treats "contiguous" as consecutive entries in the file, not consecutive in clock time. This means gaps between timestamps (e.g., across days) are allowed within a window.
