# Claude Code Session Tracking

Track and log Claude Code sessions, conversations, and their results.

## Features

- **Session Logging**: Record Claude Code sessions with titles, chat history, and results
- **Daily Tracking**: Filter and view sessions by date
- **Persistent Storage**: All session data stored in `~/.pbi-cli/sessions.json`
- **Chat History**: Store conversation history and chat counts
- **Export Formats**: Export tracked sessions to JSON or CSV
- **Summary Statistics**: View aggregate data about all sessions

## Usage

### Via Python API

For users tracking Claude Code sessions:

```python
from pbi_cli.core.sessions import SessionTracker

tracker = SessionTracker()

# Log a session
tracker.log_session(
    title="Power BI DAX Optimization",
    chat_history=[
        {"role": "user", "content": "Help me optimize this DAX measure"},
        {"role": "assistant", "content": "Here's an optimized version..."},
    ],
    last_prompt="Can you explain the performance benefits?",
    last_result="The optimization reduces evaluation time by 40%...",
    session_duration_seconds=125.5,
    success=True,
)

# View all sessions
sessions = tracker.get_all_sessions()
for session in sessions:
    print(f"Title: {session['title']}")
    print(f"Duration: {session['duration_seconds']}s")
    print(f"Chats: {session['chat_count']}")
```

### CLI Commands

#### List all sessions
```bash
pbi sessions list
pbi sessions list --date 2024-06-10    # Filter by date
pbi sessions list --json               # JSON output
```

#### View session summary statistics
```bash
pbi sessions summary
pbi sessions summary --json
```

#### Export session data
```bash
pbi sessions export --format json
pbi sessions export --format csv --output my_sessions.csv
pbi sessions export --format json --output /tmp/sessions.json
```

#### Clear all session records
```bash
pbi sessions clear
```

## Storage Location

All session data is stored in: `~/.pbi-cli/sessions.json`

### Session Record Structure

```json
{
  "id": "session_1718124567890",
  "title": "Power BI DAX Optimization",
  "date": "2024-06-10T14:22:47.890123",
  "duration_seconds": 125.5,
  "status": "success",
  "last_prompt": "Can you explain the performance benefits?",
  "last_result": "The optimization reduces evaluation time by 40%...",
  "chat_count": 5,
  "chat_summary": [
    {
      "role": "user",
      "content": "Help me optimize this DAX measure"
    },
    {
      "role": "assistant",
      "content": "Here's an optimized version..."
    }
  ]
}
```

## Field Descriptions

| Field | Description |
|-------|-------------|
| `id` | Unique session identifier (timestamp-based) |
| `title` | Session title/topic |
| `date` | Session date and time in ISO format |
| `duration_seconds` | Total session duration |
| `status` | Session status (`success` or `failed`) |
| `last_prompt` | The last user message in the session |
| `last_result` | The last assistant response |
| `chat_count` | Total number of messages in the session |
| `chat_summary` | Array of conversation messages |

## Daily Logging

Filter sessions by date to see daily activity:

```bash
pbi sessions list --date 2024-06-10
```

This is useful for:
- Daily progress reports
- Session frequency analysis
- Weekly/monthly reviews

## Export Formats

### JSON
Preserves all fields including full chat history. Best for detailed analysis and long-term archival.

### CSV
Tabular format with fields: id, title, date, duration_seconds, status, chat_count, last_prompt, last_result

## Integration with Routine Tracking

Sessions and routines are tracked separately but work together:

- **Routines**: Track individual CLI commands and their execution time
- **Sessions**: Track overall Claude Code interaction sessions and conversations

Use both to understand:
- Command-level performance (routines)
- Session-level productivity (sessions)

## Examples

### Track a power BI modeling session
```python
from pbi_cli.core.sessions import SessionTracker

tracker = SessionTracker()
tracker.log_session(
    title="Sales Model Creation",
    chat_history=[
        {"role": "user", "content": "Create a sales star schema"},
        {"role": "assistant", "content": "Created tables: Sales, Products, Calendar..."},
    ],
    last_prompt="Add relationships between tables",
    last_result="Relationships created successfully",
    session_duration_seconds=300.0,
)
```

### Export daily sessions
```bash
# Export today's sessions to CSV
pbi sessions export --format csv --date 2024-06-10
```

### View session statistics
```bash
pbi sessions summary
# Output:
# Claude Code Session Summary
# ========================================
# Total sessions: 10
# Successful: 9
# Failed: 1
# Total duration: 1250s
# Average duration: 125s
# Total chats: 45
```
