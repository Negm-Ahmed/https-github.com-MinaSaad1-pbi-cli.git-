"""pbi routines: track and view command execution progress."""

from __future__ import annotations

import csv
from pathlib import Path

import click

from pbi_cli.core.output import print_error, print_info, print_json, print_success
from pbi_cli.core.routines import RoutineTracker
from pbi_cli.main import PbiContext, pass_context


@click.group()
def routines() -> None:
    """Manage routine progress tracking.

    Track execution time and status (success/failure) of CLI operations
    marked as routines. Results are stored in ~/.pbi-cli/routines.json
    """
    pass


@routines.command(name="list")
@pass_context
def list_routines(ctx: PbiContext) -> None:
    """List all tracked routines with execution details."""
    tracker = RoutineTracker()
    records = tracker.get_all_routines()

    if not records:
        if ctx.json_output:
            print_json([])
        else:
            print_info("No routines recorded yet.")
        return

    if ctx.json_output:
        print_json(records)
    else:
        print_info(f"Total routines: {len(records)}\n")
        for i, record in enumerate(records, 1):
            status = "✓" if record["status"] == "success" else "✗"
            timestamp = record["timestamp"]
            exec_time = record["execution_time_seconds"]
            name = record["name"]
            print_info(f"{i}. [{status}] {name}")
            print_info(f"   Time: {exec_time}s | {timestamp}")
            if "error" in record:
                print_error(f"   Error: {record['error']}")
            print_info("")


@routines.command(name="summary")
@pass_context
def summary(ctx: PbiContext) -> None:
    """Show summary statistics of all routines."""
    tracker = RoutineTracker()
    stats = tracker.get_routine_summary()

    if ctx.json_output:
        print_json(stats)
    else:
        if stats["total"] == 0:
            print_info("No routines recorded yet.")
            return

        print_info("Routine Execution Summary")
        print_info("=" * 40)
        print_info(f"Total routines: {stats['total']}")
        print_info(f"Successful: {stats['successful']}")
        print_info(f"Failed: {stats['failed']}")
        print_info(f"Total time: {stats['total_time_seconds']}s")
        print_info(f"Average time: {stats['average_time_seconds']}s")


@routines.command(name="export")
@click.option(
    "--format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Export format (json or csv).",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Output file path. Defaults to routines.json or routines.csv in current dir.",
)
@pass_context
def export_routines(ctx: PbiContext, format: str, output: str | None) -> None:
    """Export routine records to JSON or CSV file."""
    tracker = RoutineTracker()
    records = tracker.get_all_routines()

    if not records:
        print_error("No routines to export.")
        raise SystemExit(1)

    if output is None:
        output = f"routines.{format}"

    output_path = Path(output)

    try:
        if format == "json":
            _export_json(records, output_path)
        else:
            _export_csv(records, output_path)

        if ctx.json_output:
            print_json({
                "status": "success",
                "format": format,
                "output_file": str(output_path.absolute()),
                "records_exported": len(records),
            })
        else:
            print_success(f"Exported {len(records)} routines to {output_path}")
    except IOError as e:
        print_error(f"Failed to export: {e}")
        raise SystemExit(1)


def _export_json(records: list[dict], output_path: Path) -> None:
    """Export records to JSON file."""
    import json

    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)


def _export_csv(records: list[dict], output_path: Path) -> None:
    """Export records to CSV file."""
    if not records:
        return

    fieldnames = ["id", "name", "command", "timestamp", "execution_time_seconds", "status", "error"]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = {field: record.get(field, "") for field in fieldnames}
            writer.writerow(row)


@routines.command(name="clear")
@click.confirmation_option(prompt="Are you sure you want to clear all routine records?")
@pass_context
def clear_routines(ctx: PbiContext) -> None:
    """Clear all routine records."""
    tracker = RoutineTracker()
    tracker.clear_routines()

    if ctx.json_output:
        print_json({"status": "cleared"})
    else:
        print_success("All routine records cleared.")
