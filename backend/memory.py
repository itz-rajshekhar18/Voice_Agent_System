"""
memory.py — Key-value memory store with JSON persistence.

The agent uses this to remember facts about the user across sessions:
  - name, preferences, timezone, recurring notes, etc.

Each entry is stored as:
  { "key": str, "value": str, "updated_at": ISO-datetime }
"""

import json
import datetime
from pathlib import Path


STORAGE_FILE = Path("memory.json")


class MemoryStore:
    def __init__(self, storage_path: Path = STORAGE_FILE):
        self._path = storage_path
        self._store: dict[str, dict] = {}
        self._load()

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def set(self, key: str, value: str):
        """Persist a key-value memory entry."""
        self._store[key.strip().lower()] = {
            "value":      value,
            "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self.save()

    def get(self, key: str) -> str | None:
        """Retrieve the value for a key, or None if not found."""
        entry = self._store.get(key.strip().lower())
        return entry["value"] if entry else None

    def all(self) -> dict[str, str]:
        """Return a flat {key: value} mapping of all memories."""
        return {k: v["value"] for k, v in self._store.items()}

    def delete(self, key: str) -> bool:
        """Remove a memory entry. Returns True if it existed."""
        key = key.strip().lower()
        if key in self._store:
            del self._store[key]
            self.save()
            return True
        return False

    def snapshot_for_prompt(self) -> str:
        """Compact representation injected into the system prompt."""
        if not self._store:
            return "{}"
        flat = {k: v["value"] for k, v in self._store.items()}
        return json.dumps(flat, ensure_ascii=False)

    # ------------------------------------------------------------------ #
    #  Persistence                                                         #
    # ------------------------------------------------------------------ #

    def save(self):
        self._path.write_text(json.dumps(self._store, indent=2, ensure_ascii=False))

    def _load(self):
        if self._path.exists():
            try:
                data = json.loads(self._path.read_text())
                # Support both legacy flat format and current nested format
                for k, v in data.items():
                    if isinstance(v, dict) and "value" in v:
                        self._store[k] = v
                    else:
                        self._store[k] = {
                            "value":      str(v),
                            "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
                        }
            except json.JSONDecodeError:
                self._store = {}

    def __len__(self) -> int:
        return len(self._store)

    def __repr__(self) -> str:
        return f"<MemoryStore entries={len(self._store)}>"
