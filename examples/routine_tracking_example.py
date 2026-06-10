"""Example: Using routine progress tracking with pbi-cli.

This example demonstrates how to track routine execution time and status.
"""

from pbi_cli.core.output import track_routine
from pbi_cli.core.routines import RoutineTracker


def example_track_routine():
    """Example of tracking a routine execution."""
    # Track a routine operation
    with track_routine("fetch_sales_data", "dax execute 'EVALUATE Sales'"):
        # Simulate some work
        import time
        time.sleep(1)
        # Do something with Power BI
        pass

    # Track another routine
    with track_routine("create_measure", "measure create Revenue"):
        import time
        time.sleep(0.5)
        # Create a measure
        pass


def example_view_routines():
    """Example of viewing tracked routines."""
    tracker = RoutineTracker()

    # Get all routines
    all_routines = tracker.get_all_routines()
    print(f"Total routines tracked: {len(all_routines)}")

    for routine in all_routines:
        status = "✓" if routine["status"] == "success" else "✗"
        print(
            f"{status} {routine['name']}: "
            f"{routine['execution_time_seconds']}s - {routine['timestamp']}"
        )


def example_summary_stats():
    """Example of viewing routine summary statistics."""
    tracker = RoutineTracker()
    stats = tracker.get_routine_summary()

    print(f"Total routines: {stats['total']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Total time: {stats['total_time_seconds']}s")
    print(f"Average time: {stats['average_time_seconds']}s")


if __name__ == "__main__":
    print("=== Example: Tracking Routines ===\n")

    print("1. Tracking routine executions...")
    example_track_routine()
    print("   ✓ Routines tracked\n")

    print("2. Viewing all tracked routines...")
    example_view_routines()
    print()

    print("3. Viewing summary statistics...")
    example_summary_stats()
    print()

    print("You can also use CLI commands:")
    print("  pbi routines list")
    print("  pbi routines summary")
    print("  pbi routines export --format json")
    print("  pbi routines export --format csv --output report.csv")
