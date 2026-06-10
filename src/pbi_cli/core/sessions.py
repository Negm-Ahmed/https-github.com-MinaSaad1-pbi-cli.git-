"""Claude Code session and chat tracking."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class SessionTracker:
    """Track Claude Code sessions, chats, and interactions."""

    def __init__(self) -> None:
        self.config_dir = Path.home() / ".pbi-cli"
        self.sessions_file = self.config_dir / "sessions.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_sessions(self) -> list[dict[str, Any]]:
        """Load all sessions from file."""
        if not self.sessions_file.exists():
            return []
        try:
            with open(self.sessions_file) as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save_sessions(self, sessions: list[dict[str, Any]]) -> None:
        """Save sessions to file."""
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)

    def log_session(
        self,
        title: str,
        chat_history: list[dict[str, str]],
        last_prompt: str,
        last_result: str,
        session_duration_seconds: float,
        success: bool = True,
    ) -> None:
        """Log a Claude Code session with its conversation and results."""
        sessions = self._load_sessions()

        session_record: dict[str, Any] = {
            "id": f"session_{int(datetime.now().timestamp() * 1000)}",
            "title": title,
            "date": datetime.now().isoformat(),
            "duration_seconds": round(session_duration_seconds, 3),
            "status": "success" if success else "failed",
            "last_prompt": last_prompt,
            "last_result": last_result,
            "chat_count": len(chat_history),
            "chat_summary": chat_history,
        }

        sessions.append(session_record)
        self._save_sessions(sessions)

    def get_all_sessions(self) -> list[dict[str, Any]]:
        """Get all tracked sessions."""
        return self._load_sessions()

    def get_daily_sessions(self, date: str | None = None) -> list[dict[str, Any]]:
        """Get sessions from a specific date (YYYY-MM-DD format)."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        all_sessions = self.get_all_sessions()
        return [s for s in all_sessions if s["date"].startswith(date)]

    def get_session_summary(self) -> dict[str, Any]:
        """Get summary statistics of all sessions."""
        sessions = self.get_all_sessions()

        if not sessions:
            return {
                "total_sessions": 0,
                "successful_sessions": 0,
                "failed_sessions": 0,
                "total_duration_seconds": 0,
                "average_duration_seconds": 0,
                "total_chats": 0,
            }

        successful = sum(1 for s in sessions if s["status"] == "success")
        failed = len(sessions) - successful
        total_duration = sum(s.get("duration_seconds", 0) for s in sessions)
        total_chats = sum(s.get("chat_count", 0) for s in sessions)
        avg_duration = total_duration / len(sessions) if sessions else 0

        return {
            "total_sessions": len(sessions),
            "successful_sessions": successful,
            "failed_sessions": failed,
            "total_duration_seconds": round(total_duration, 3),
            "average_duration_seconds": round(avg_duration, 3),
            "total_chats": total_chats,
        }

    def clear_sessions(self) -> None:
        """Clear all session records."""
        self._save_sessions([])
