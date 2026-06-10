"""Routine progress tracking for pbi-cli."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any


class RoutineTracker:
    """Track execution time and status of marked routines."""

    def __init__(self) -> None:
        self.config_dir = Path.home() / ".pbi-cli"
        self.routines_file = self.config_dir / "routines.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_routines(self) -> list[dict[str, Any]]:
        """Load all routines from file."""
        if not self.routines_file.exists():
            return []
        try:
            with open(self.routines_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_routines(self, routines: list[dict[str, Any]]) -> None:
        """Save routines to file."""
        with open(self.routines_file, "w") as f:
            json.dump(routines, f, indent=2)

    def start_routine(self, name: str, command: str) -> tuple[str, float]:
        """Start tracking a routine. Returns routine ID and start time."""
        routine_id = f"{name}_{int(time.time() * 1000)}"
        start_time = time.time()
        return routine_id, start_time

    def end_routine(
        self,
        routine_id: str,
        name: str,
        command: str,
        start_time: float,
        success: bool,
        error_message: str | None = None,
    ) -> None:
        """Record completed routine."""
        execution_time = time.time() - start_time
        routines = self._load_routines()

        routine_record: dict[str, Any] = {
            "id": routine_id,
            "name": name,
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "execution_time_seconds": round(execution_time, 3),
            "status": "success" if success else "failed",
        }

        if error_message:
            routine_record["error"] = error_message

        routines.append(routine_record)
        self._save_routines(routines)

    def get_all_routines(self) -> list[dict[str, Any]]:
        """Get all tracked routines."""
        return self._load_routines()

    def get_routine_summary(self) -> dict[str, Any]:
        """Get summary statistics of all routines."""
        routines = self.get_all_routines()

        if not routines:
            return {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "total_time_seconds": 0,
                "average_time_seconds": 0,
            }

        successful = sum(1 for r in routines if r["status"] == "success")
        failed = len(routines) - successful
        total_time = sum(r.get("execution_time_seconds", 0) for r in routines)
        avg_time = total_time / len(routines) if routines else 0

        return {
            "total": len(routines),
            "successful": successful,
            "failed": failed,
            "total_time_seconds": round(total_time, 3),
            "average_time_seconds": round(avg_time, 3),
        }

    def clear_routines(self) -> None:
        """Clear all routine records."""
        self._save_routines([])
