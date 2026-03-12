"""Domain types for type hints (no runtime dependency)."""

from dataclasses import dataclass
from typing import Literal

TaskStatus = Literal["todo", "in-progress", "review", "done"]
TaskPriority = Literal["low", "medium", "high", "critical"]
UserRole = Literal["admin", "member", "viewer"]

# Valid status transitions — strict ordering
VALID_TRANSITIONS: dict[TaskStatus, list[TaskStatus]] = {
    "todo": ["in-progress"],
    "in-progress": ["review", "todo"],       # can move back to todo
    "review": ["done", "in-progress"],        # can reject back
    "done": [],                               # terminal
}
