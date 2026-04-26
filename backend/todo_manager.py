"""
todo_manager.py — CRUD operations and JSON persistence for To-Do items.

Schema of a single task:
  {
    "id":        str  (short hex id),
    "title":     str,
    "priority":  "low" | "medium" | "high",
    "due":       str | None,
    "done":      bool,
    "created_at": str  (ISO date)
  }
"""

import json
import uuid
import datetime
from pathlib import Path


STORAGE_FILE = Path("todos.json")

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class ToDoManager:
    def __init__(self, storage_path: Path = STORAGE_FILE):
        self._path = storage_path
        self._tasks: list[dict] = []
        self._load()

    # ------------------------------------------------------------------ #
    #  CRUD                                                                #
    # ------------------------------------------------------------------ #

    def add(self, title: str, priority: str = "medium", due: str | None = None) -> dict:
        task = {
            "id":         uuid.uuid4().hex[:8],
            "title":      title.strip(),
            "priority":   priority if priority in PRIORITY_ORDER else "medium",
            "due":        due,
            "done":       False,
            "created_at": datetime.date.today().isoformat(),
        }
        self._tasks.append(task)
        self.save()
        return task

    def update(self, identifier: str, done: bool | None = None, new_title: str | None = None) -> dict | None:
        task = self._find(identifier)
        if not task:
            return None
        if done is not None:
            task["done"] = done
        if new_title:
            task["title"] = new_title.strip()
        self.save()
        return task

    def delete(self, identifier: str) -> str | None:
        task = self._find(identifier)
        if not task:
            return None
        self._tasks.remove(task)
        self.save()
        return task["title"]

    def all(self) -> list[dict]:
        return sorted(self._tasks, key=lambda t: (t["done"], PRIORITY_ORDER.get(t["priority"], 1)))

    def pending(self) -> list[dict]:
        return [t for t in self.all() if not t["done"]]

    def done(self) -> list[dict]:
        return [t for t in self.all() if t["done"]]

    # ------------------------------------------------------------------ #
    #  Helpers for the agent                                               #
    # ------------------------------------------------------------------ #

    def snapshot_for_prompt(self) -> str:
        """Compact JSON snapshot injected into the system prompt."""
        if not self._tasks:
            return "[]"
        slim = [
            {"id": t["id"], "title": t["title"], "priority": t["priority"],
             "done": t["done"], "due": t["due"]}
            for t in self.all()
        ]
        return json.dumps(slim, ensure_ascii=False)

    def summary(self) -> str:
        """Human-readable summary returned to the user."""
        all_tasks = self.all()
        if not all_tasks:
            return "Your to-do list is empty."
        pending = self.pending()
        done    = self.done()
        lines   = [f"You have {len(all_tasks)} task(s) — {len(pending)} pending, {len(done)} done.\n"]
        if pending:
            lines.append("Pending:")
            for t in pending:
                due_str = f"  (due {t['due']})" if t.get("due") else ""
                lines.append(f"  [{t['priority'].upper()}] {t['title']}{due_str}")
        if done:
            lines.append("\nCompleted:")
            for t in done:
                lines.append(f"  ✓ {t['title']}")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  Persistence                                                         #
    # ------------------------------------------------------------------ #

    def save(self):
        self._path.write_text(json.dumps(self._tasks, indent=2, ensure_ascii=False))

    def _load(self):
        if self._path.exists():
            try:
                self._tasks = json.loads(self._path.read_text())
            except json.JSONDecodeError:
                self._tasks = []

    # ------------------------------------------------------------------ #
    #  Internal search                                                     #
    # ------------------------------------------------------------------ #

    def _find(self, identifier: str) -> dict | None:
        """Find by exact id first, then case-insensitive title substring."""
        for t in self._tasks:
            if t["id"] == identifier:
                return t
        identifier_lower = identifier.lower()
        for t in self._tasks:
            if identifier_lower in t["title"].lower():
                return t
        return None
