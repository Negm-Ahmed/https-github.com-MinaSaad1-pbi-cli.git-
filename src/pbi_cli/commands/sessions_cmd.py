"""pbi sessions: track and view Claude Code sessions and chats."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import click

from pbi_cli.core.output import print_error, print_info, print_json, print_success
from pbi_cli.core.sessions import SessionTracker
from pbi_cli.main import PbiContext, pass_context


@click.group()
def sessions() -> None:
    """Manage Claude Code session tracking.

    Track sessions, chats, and conversation results.
    Data stored in ~/.pbi-cli/sessions.json
    """
    pass


@sessions.command(name="list")
@click.option("--date", default=None, help="Filter by date (YYYY-MM-DD).")
@pass_context
def list_sessions(ctx: PbiContext, date: str | None) -> None:
    """List tracked sessions and their chat history."""
    tracker = SessionTracker()

    if date:
        records = tracker.get_daily_sessions(date)
    else:
        records = tracker.get_all_sessions()

    if not records:
        if ctx.json_output:
            print_json([])
        else:
            msg = f"No sessions recorded for {date}." if date else "No sessions recorded yet."
            print_info(msg)
        return

    if ctx.json_output:
        print_json(records)
    else:
        print_info(f"Total sessions: {len(records)}\n")
        for i, record in enumerate(records, 1):
            status = "✓" if record["status"] == "success" else "✗"
            date_time = record["date"]
            duration = record["duration_seconds"]
            title = record["title"]
            chats = record["chat_count"]

            print_info(f"{i}. [{status}] {title}")
            print_info(f"   Date: {date_time} | Duration: {duration}s | Chats: {chats}")
            print_info(f"   Last prompt: {record['last_prompt'][:50]}...")
            if record["last_result"]:
                print_info(f"   Last result: {record['last_result'][:50]}...")
            print_info("")


@sessions.command(name="summary")
@pass_context
def summary(ctx: PbiContext) -> None:
    """Show summary statistics of all sessions."""
    tracker = SessionTracker()
    stats = tracker.get_session_summary()

    if ctx.json_output:
        print_json(stats)
    else:
        if stats["total_sessions"] == 0:
            print_info("No sessions recorded yet.")
            return

        print_info("Claude Code Session Summary")
        print_info("=" * 40)
        print_info(f"Total sessions: {stats['total_sessions']}")
        print_info(f"Successful: {stats['successful_sessions']}")
        print_info(f"Failed: {stats['failed_sessions']}")
        print_info(f"Total duration: {stats['total_duration_seconds']}s")
        print_info(f"Average duration: {stats['average_duration_seconds']}s")
        print_info(f"Total chats: {stats['total_chats']}")


@sessions.command(name="export")
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
    help="Output file path. Defaults to sessions.json or sessions.csv in current dir.",
)
@pass_context
def export_sessions(ctx: PbiContext, format: str, output: str | None) -> None:
    """Export session records to JSON or CSV file."""
    tracker = SessionTracker()
    records = tracker.get_all_sessions()

    if not records:
        print_error("No sessions to export.")
        raise SystemExit(1)

    if output is None:
        output = f"sessions.{format}"

    output_path = Path(output)

    try:
        if format == "json":
            _export_json(records, output_path)
        else:
            _export_csv(records, output_path)

        if ctx.json_output:
            result: dict[str, str | int] = {
                "status": "success",
                "format": format,
                "output_file": str(output_path.absolute()),
                "sessions_exported": len(records),
            }
            print_json(result)
        else:
            print_success(f"Exported {len(records)} sessions to {output_path}")
    except OSError as e:
        print_error(f"Failed to export: {e}")
        raise SystemExit(1)


def _export_json(records: list[dict[str, Any]], output_path: Path) -> None:
    """Export records to JSON file."""
    import json

    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)


def _export_csv(records: list[dict[str, Any]], output_path: Path) -> None:
    """Export records to CSV file."""
    if not records:
        return

    fieldnames = [
        "id",
        "title",
        "date",
        "duration_seconds",
        "status",
        "chat_count",
        "last_prompt",
        "last_result",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = {field: str(record.get(field, "")) for field in fieldnames}
            writer.writerow(row)


@sessions.command(name="clear")
@click.confirmation_option(prompt="Are you sure you want to clear all session records?")
@pass_context
def clear_sessions(ctx: PbiContext) -> None:
    """Clear all session records."""
    tracker = SessionTracker()
    tracker.clear_sessions()

    if ctx.json_output:
        print_json({"status": "cleared"})
    else:
        print_success("All session records cleared.")
