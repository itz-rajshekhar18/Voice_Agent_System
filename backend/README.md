# Voice To-Do Agent 🤖

A voice-enabled AI assistant that manages your to-do list and remembers
important context — powered by Claude claude-sonnet-4-20250514.

---

## Project Structure

```
voice_todo_agent/
├── main.py          # Entry point — wires all components together
├── agent.py         # Claude agent with tool-calling logic
├── todo_manager.py  # CRUD + JSON persistence for tasks
├── memory.py        # Key-value memory store with persistence
├── voice.py         # STT (microphone → text) + TTS (text → speech)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **macOS** — install PortAudio first:  `brew install portaudio`
> **Ubuntu** — `sudo apt install python3-pyaudio portaudio19-dev`

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Run

```bash
python main.py
```

Press **Enter** to speak (microphone), or **type** your command and press Enter.

---

## Example Commands

| What you say/type                          | What happens                          |
|--------------------------------------------|---------------------------------------|
| `add buy groceries, high priority`         | Creates a high-priority task          |
| `add dentist appointment due 2025-05-10`   | Task with a due date                  |
| `list my tasks`                            | Summarises all pending/done tasks     |
| `mark buy groceries as done`               | Updates the task status               |
| `delete the dentist task`                  | Removes the task                      |
| `my name is Alex, remember that`           | Saves "name = Alex" to memory         |
| `what do you remember about me?`           | Agent recalls stored memories         |
| `quit`                                     | Saves everything and exits            |

---

## Architecture

```
main.py
  │
  ├─ VoiceInterface   (voice.py)
  │    ├─ listen()  → SpeechRecognition → Google STT API
  │    └─ speak()  → pyttsx3 (offline TTS)
  │
  ├─ ToDoAgent        (agent.py)
  │    ├─ chat(user_text) → Anthropic Claude API
  │    ├─ _process_tools() → parse <tool_call> blocks
  │    └─ _dispatch()      → route to manager methods
  │
  ├─ ToDoManager      (todo_manager.py)
  │    ├─ add / update / delete / all / pending / done
  │    └─ persists to todos.json
  │
  └─ MemoryStore      (memory.py)
       ├─ set / get / all / delete
       └─ persists to memory.json
```

---

## Data Files (auto-created)

| File          | Contents                     |
|---------------|------------------------------|
| `todos.json`  | All to-do tasks (persisted)  |
| `memory.json` | Agent's key-value memories   |

---

## Notes

- Voice input requires a working microphone and internet access (Google STT).
- TTS uses `pyttsx3` (fully offline). If unavailable, responses are printed.
- Both voice components degrade gracefully — the agent always works via text.
