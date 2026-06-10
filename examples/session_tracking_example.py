"""Example: Using Claude Code session tracking with pbi-cli.

This example demonstrates how to log and track Claude Code sessions.
"""

from pbi_cli.core.sessions import SessionTracker


def example_log_session():
    """Example of logging a Claude Code session."""
    tracker = SessionTracker()

    # Log a session with chat history
    chat_history = [
        {"role": "user", "content": "Help me create a Power BI sales model"},
        {
            "role": "assistant",
            "content": "I'll help you create a star schema with Sales, Products, and Calendar tables.",
        },
        {
            "role": "user",
            "content": "Add DAX measures for total revenue and average order value",
        },
        {
            "role": "assistant",
            "content": "Created two measures: TotalRevenue and AvgOrderValue with proper formatting.",
        },
    ]

    tracker.log_session(
        title="Sales Model Creation",
        chat_history=chat_history,
        last_prompt="Add DAX measures for total revenue and average order value",
        last_result="Created two measures: TotalRevenue and AvgOrderValue with proper formatting.",
        session_duration_seconds=425.5,
        success=True,
    )

    # Log another session
    tracker.log_session(
        title="Dashboard Performance Optimization",
        chat_history=[
            {"role": "user", "content": "Why is my dashboard loading slowly?"},
            {
                "role": "assistant",
                "content": "Let's analyze the trace logs and identify bottlenecks.",
            },
        ],
        last_prompt="What's the recommended approach?",
        last_result="Implement aggregations and reduce visual complexity on the main page.",
        session_duration_seconds=180.0,
        success=True,
    )


def example_view_sessions():
    """Example of viewing tracked sessions."""
    tracker = SessionTracker()

    # Get all sessions
    all_sessions = tracker.get_all_sessions()
    print(f"Total sessions tracked: {len(all_sessions)}\n")

    for session in all_sessions:
        print(f"Title: {session['title']}")
        print(f"Date: {session['date']}")
        print(f"Duration: {session['duration_seconds']}s")
        print(f"Status: {session['status']}")
        print(f"Chats: {session['chat_count']}")
        print(f"Last prompt: {session['last_prompt'][:50]}...")
        print()


def example_daily_sessions():
    """Example of viewing sessions from a specific date."""
    tracker = SessionTracker()

    # Get today's sessions
    today_sessions = tracker.get_daily_sessions()
    print(f"Today's sessions: {len(today_sessions)}\n")

    for session in today_sessions:
        print(f"✓ {session['title']} - {session['duration_seconds']}s")


def example_summary_stats():
    """Example of viewing session summary statistics."""
    tracker = SessionTracker()
    stats = tracker.get_session_summary()

    print("Claude Code Session Summary")
    print("=" * 40)
    print(f"Total sessions: {stats['total_sessions']}")
    print(f"Successful: {stats['successful_sessions']}")
    print(f"Failed: {stats['failed_sessions']}")
    print(f"Total time: {stats['total_duration_seconds']}s")
    print(f"Average time: {stats['average_duration_seconds']}s")
    print(f"Total chats: {stats['total_chats']}")


if __name__ == "__main__":
    print("=== Example: Tracking Claude Code Sessions ===\n")

    print("1. Logging sessions...")
    example_log_session()
    print("   ✓ Sessions logged\n")

    print("2. Viewing all sessions...")
    example_view_sessions()

    print("3. Viewing today's sessions...")
    example_daily_sessions()
    print()

    print("4. Viewing summary statistics...")
    example_summary_stats()
    print()

    print("You can also use CLI commands:")
    print("  pbi sessions list")
    print("  pbi sessions list --date 2024-06-10")
    print("  pbi sessions summary")
    print("  pbi sessions export --format json")
    print("  pbi sessions export --format csv --output sessions.csv")
