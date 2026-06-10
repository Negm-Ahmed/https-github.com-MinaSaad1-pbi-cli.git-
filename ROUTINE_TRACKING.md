# Routine Progress Tracking

Track execution time and status (success/failure) of CLI commands marked as routines.

## Features

- **Manual Routine Marking**: Explicitly mark commands to track them as routines
- **Persistent Storage**: All execution data stored in `~/.pbi-cli/routines.json`
- **REPL Integration**: View routine summary when exiting REPL session
- **Multiple Export Formats**: Export tracked data to JSON or CSV

## Usage

### Via Context Manager (Python Code)

For users writing Python scripts that use pbi-cli:

```python
from pbi_cli.core.output import track_routine
from pbi_cli.core.routines import RoutineTracker

# Track a routine using context manager
with track_routine("my_dax_query", "dax execute 'EVALUATE Sales'"):
    # Your code here
    pass

# Later, view tracked routines
tracker = RoutineTracker()
records = tracker.get_all_routines()
for record in records:
    print(f"{record['name']}: {record['execution_time_seconds']}s - {record['status']}")
```

### CLI Commands

#### List all routines
```bash
pbi routines list
pbi routines list --json    # JSON output for programmatic use
```

#### View summary statistics
```bash
pbi routines summary
pbi routines summary --json
```

#### Export tracking data
```bash
pbi routines export --format json
pbi routines export --format csv --output my_report.csv
pbi routines export --format json --output /tmp/tracking.json
```

#### Clear all routine records
```bash
pbi routines clear
```

## Storage Location

All routine data is stored in: `~/.pbi-cli/routines.json`

Example structure:
```json
[
  {
    "id": "my_routine_1718124567890",
    "name": "my_routine",
    "command": "dax execute 'EVALUATE Sales'",
    "timestamp": "2024-06-10T14:22:47.890123",
    "execution_time_seconds": 2.345,
    "status": "success"
  },
  {
    "id": "failed_routine_1718124570123",
    "name": "failed_routine",
    "command": "dax execute 'INVALID DAX'",
    "timestamp": "2024-06-10T14:22:50.123456",
    "execution_time_seconds": 0.156,
    "status": "failed",
    "error": "Syntax error in DAX expression"
  }
]
```

## REPL Integration

When you exit an interactive REPL session, you'll see a summary:

```
pbi> exit
Routines executed: 5 (4 successful, 1 failed)
Goodbye.
```

This summary only shows if routines were tracked during that REPL session.

## Export Formats

### JSON
Preserves all fields including error messages. Suitable for detailed analysis.

### CSV
Tabular format with columns: id, name, command, timestamp, execution_time_seconds, status, error

## Getting Started

1. **Install pbi-cli**: `pipx install pbi-cli-tool`
2. **Use routines**: Wrap your operations in `track_routine()` context manager
3. **View progress**: Run `pbi routines list` to see all tracked operations
4. **Export results**: Run `pbi routines export --format csv` to share results
