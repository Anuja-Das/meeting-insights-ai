"""Helpers to convert model JSON output into human-readable text/Markdown."""

from __future__ import annotations

import json
from typing import Any


def _as_dict(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except Exception:
            return None
        return parsed if isinstance(parsed, dict) else None
    return None


def _lines_from_tasks(tasks: Any) -> list[str]:
    if not isinstance(tasks, list):
        return []

    lines: list[str] = []
    for i, item in enumerate(tasks, start=1):
        if not isinstance(item, dict):
            lines.append(f"{i}. {str(item)}")
            continue

        task = str(item.get("task", "")).strip() or "(no task)"
        owner = str(item.get("owner", "")).strip()
        deadline = str(item.get("deadline", "")).strip()

        details: list[str] = []
        if owner:
            details.append(f"**Owner**: {owner}")
        if deadline:
            details.append(f"**Deadline**: {deadline}")

        if details:
            lines.append(
                f"{i}. **{task}**" + "\n   - " + "\n   - ".join(details)
            )
        else:
            lines.append(f"{i}. **{task}**")

    return lines


def _lines_from_actions(actions: Any) -> list[str]:
    # Some pipelines may call them actions instead of tasks.
    if not isinstance(actions, list):
        return []

    lines: list[str] = []
    for i, item in enumerate(actions, start=1):
        if not isinstance(item, dict):
            lines.append(f"{i}. {str(item)}")
            continue

        task = str(item.get("task", "")).strip() or "(no action)"
        owner = str(item.get("owner", "")).strip()
        deadline = str(item.get("deadline", "")).strip()

        details: list[str] = []
        if owner:
            details.append(f"**Owner**: {owner}")
        if deadline:
            details.append(f"**Deadline**: {deadline}")

        if details:
            lines.append(
                f"{i}. **{task}**" + "\n   - " + "\n   - ".join(details)
            )
        else:
            lines.append(f"{i}. **{task}**")

    return lines


def _lines_from_risks(risks: Any) -> list[str]:
    if not isinstance(risks, list):
        return []

    lines: list[str] = []
    for i, item in enumerate(risks, start=1):
        if not isinstance(item, dict):
            lines.append(f"{i}. {str(item)}")
            continue

        issue = str(item.get("issue", "")).strip() or "(no issue)"
        impact = str(item.get("impact", "")).strip()
        suggestion = str(item.get("suggestion", "")).strip()

        parts: list[str] = [f"**{issue}**"]
        if impact:
            parts.append(f"**Impact**: {impact}")
        if suggestion:
            parts.append(f"**Suggestion**: {suggestion}")

        # Render as a single bullet-like line with separators.
        lines.append(f"{i}. " + " — ".join(parts[:1]) + ("\n   - " + "\n   - ".join(parts[1:]) if len(parts) > 1 else ""))

    return lines


def format_insights_as_markdown(model_output: Any) -> str:
    """Convert the model JSON output into readable Markdown.

    Expected schema (best-effort):
    {
      "summary": "...",
      "tasks": [{"task": "...", "owner": "...", "deadline": "..."}],
      "risks": [{"issue": "...", "impact": "...", "suggestion": "..."}]
    }

    If parsing fails, returns the raw output as a fenced code block.
    """

    data = _as_dict(model_output)
    if data is None:
        raw = str(model_output) if model_output is not None else ""
        return "## Result\n\n```text\n" + raw + "\n```"

    summary = str(data.get("summary", "")).strip()
    tasks_lines = _lines_from_tasks(data.get("tasks"))
    # Fallback for alternate key name
    if not tasks_lines:
        tasks_lines = _lines_from_actions(data.get("actions"))

    risks_lines = _lines_from_risks(data.get("risks"))

    md: list[str] = []

    md.append("## Summary")
    md.append(summary if summary else "(No summary returned)")

    md.append("\n## Tasks")
    if tasks_lines:
        md.extend(tasks_lines)
    else:
        md.append("(No tasks returned)")

    md.append("\n## Risks")
    if risks_lines:
        # risks_lines already include numbering and optional sub-bullets
        md.extend(risks_lines)
    else:
        md.append("(No risks returned)")

    return "\n".join(md).strip() + "\n"
