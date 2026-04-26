"""
agent.py — Claude-powered agent with tool-calling logic via OpenRouter.

Responsibilities:
  - Maintain conversation history
  - Build the system prompt with live todo/memory context
  - Parse Claude's responses for <tool_call> blocks
  - Dispatch tool calls to ToDoManager / MemoryStore
  - Return clean text replies to the caller
"""

import json
import re
import os
import requests
from todo_manager import ToDoManager
from memory import MemoryStore


SYSTEM_PROMPT = """You are a voice-enabled AI To-Do assistant. You help users manage tasks
and remember important context from your conversations.

You have access to the following tools. Call them using the exact XML format shown below.

AVAILABLE TOOLS:
  add_todo       — Add a new task
  update_todo    — Mark done or rename a task
  delete_todo    — Remove a task
  list_todos     — List all tasks
  save_memory    — Persist an important fact about the user
  recall_memory  — Retrieve stored facts

TOOL CALL FORMAT (use inside your reply when needed):
<tool_call>
{"tool": "<name>", "params": { ... }}
</tool_call>

TOOL SCHEMAS:
  add_todo    : {"title": str, "priority": "low"|"medium"|"high", "due": str (optional)}
  update_todo : {"id": str, "done": bool (optional), "title": str (optional)}
  delete_todo : {"id": str}
  list_todos  : {}
  save_memory : {"key": str, "value": str}
  recall_memory: {"key": str (optional — omit to recall all)}

BEHAVIOUR RULES:
  1. For task commands → always use the appropriate tool.
  2. For general conversation → reply naturally with no tool calls.
  3. Confirm every tool action in plain English after executing it.
  4. Proactively call save_memory when the user shares personal preferences or context.
  5. Keep replies short and friendly — this is a voice interface.
  6. Never expose raw JSON or tool XML to the user in your final reply.
"""


class ToDoAgent:
    def __init__(self, memory_store: MemoryStore, todo_manager: ToDoManager):
        self.memory   = memory_store
        self.todos    = todo_manager
        self.api_key  = os.environ.get("OPENROUTER_API_KEY", "")
        self.api_url  = "https://openrouter.ai/api/v1/chat/completions"
        self.model    = "openai/gpt-4o-mini"  # Using GPT-4o Mini via OpenRouter
        self.history  = []          # list of {"role": ..., "content": ...}
        self.max_history = 20       # rolling window to stay within context limits

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def chat(self, user_text: str) -> str:
        """Send a user message; return the agent's plain-text reply."""
        self.history.append({"role": "user", "content": user_text})
        self._trim_history()

        raw_reply = self._call_claude()
        clean_reply, tool_results = self._process_tools(raw_reply)

        # Build assistant turn that includes tool feedback
        assistant_content = raw_reply
        if tool_results:
            assistant_content += "\n[Tools executed: " + "; ".join(tool_results) + "]"
        self.history.append({"role": "assistant", "content": assistant_content})

        return clean_reply or "(done)"

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _build_context_prefix(self) -> str:
        """Inject live state so Claude always has up-to-date data."""
        todo_snapshot  = self.todos.snapshot_for_prompt()
        memory_snapshot = self.memory.snapshot_for_prompt()
        today = __import__("datetime").date.today().strftime("%A, %d %B %Y")
        return (
            f"\n\nLIVE CONTEXT (today: {today}):\n"
            f"Current todos: {todo_snapshot}\n"
            f"Memories: {memory_snapshot}"
        )

    def _call_claude(self) -> str:
        system = SYSTEM_PROMPT + self._build_context_prefix()
        
        # Prepare messages for OpenRouter API
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in self.history]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",  # Optional: for rankings
            "X-Title": "Voice AI Assistant"  # Optional: for rankings
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 800,
            "temperature": 0.7,
        }
        
        # Add system message to the first message if using OpenRouter
        if messages:
            # OpenRouter expects system content in messages array
            messages.insert(0, {"role": "system", "content": system})
            payload["messages"] = messages
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"OpenRouter API error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return "I'm having trouble connecting to the AI service. Please try again."

    def _process_tools(self, raw: str) -> tuple[str, list[str]]:
        """
        Parse <tool_call> blocks from raw reply.
        Execute each tool, collect human-readable results.
        Return (clean_text, [result_strings]).
        """
        pattern = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
        tool_results = []

        def handle_match(m):
            try:
                payload = json.loads(m.group(1).strip())
                result  = self._dispatch(payload["tool"], payload.get("params", {}))
                tool_results.append(result)
            except (json.JSONDecodeError, KeyError) as exc:
                tool_results.append(f"Tool error: {exc}")
            return ""

        clean = pattern.sub(handle_match, raw).strip()
        return clean, tool_results

    def _dispatch(self, tool: str, params: dict) -> str:
        """Route a tool call to the correct manager method."""
        dispatch_map = {
            "add_todo":      self._tool_add,
            "update_todo":   self._tool_update,
            "delete_todo":   self._tool_delete,
            "list_todos":    self._tool_list,
            "save_memory":   self._tool_save_memory,
            "recall_memory": self._tool_recall_memory,
        }
        handler = dispatch_map.get(tool)
        if not handler:
            return f"Unknown tool: {tool}"
        return handler(params)

    # ------------------------------------------------------------------ #
    #  Tool handlers                                                       #
    # ------------------------------------------------------------------ #

    def _tool_add(self, p: dict) -> str:
        task = self.todos.add(
            title    = p.get("title", "Untitled"),
            priority = p.get("priority", "medium"),
            due      = p.get("due"),
        )
        return f"Added task '{task['title']}' [{task['priority']}] id={task['id']}"

    def _tool_update(self, p: dict) -> str:
        task = self.todos.update(
            identifier = p.get("id", ""),
            done       = p.get("done"),
            new_title  = p.get("title"),
        )
        if task:
            status = "done" if task["done"] else "pending"
            return f"Updated '{task['title']}' → {status}"
        return "Task not found"

    def _tool_delete(self, p: dict) -> str:
        removed = self.todos.delete(p.get("id", ""))
        return f"Deleted '{removed}'" if removed else "Task not found"

    def _tool_list(self, _: dict) -> str:
        return self.todos.summary()

    def _tool_save_memory(self, p: dict) -> str:
        self.memory.set(p.get("key", "note"), p.get("value", ""))
        return f"Saved memory: {p.get('key')} = {p.get('value')}"

    def _tool_recall_memory(self, p: dict) -> str:
        key = p.get("key")
        if key:
            val = self.memory.get(key)
            return f"{key}: {val}" if val else f"No memory for '{key}'"
        return self.memory.snapshot_for_prompt()

    def _trim_history(self):
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
