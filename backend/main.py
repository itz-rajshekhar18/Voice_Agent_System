"""
Voice-Enabled AI To-Do Agent
Entry point — wires together voice, agent, and storage layers.
"""

from agent import ToDoAgent
from voice import VoiceInterface
from memory import MemoryStore
from todo_manager import ToDoManager


def main():
    print("=" * 55)
    print("  🤖  Voice To-Do Agent  |  powered by Claude")
    print("=" * 55)
    print("Commands: speak/type your request, 'quit' to exit\n")

    memory   = MemoryStore()
    todos    = ToDoManager()
    voice    = VoiceInterface()
    agent    = ToDoAgent(memory_store=memory, todo_manager=todos)

    voice.speak("Hello! I'm your voice To-Do assistant. How can I help you?")

    while True:
        print("\n[Press Enter to speak, or type your message]")
        user_text = input("You: ").strip()

        if not user_text:
            # Voice input
            spoken = voice.listen()
            if not spoken:
                print("(No speech detected — try again)")
                continue
            user_text = spoken
            print(f"You said: {user_text}")

        if user_text.lower() in ("quit", "exit", "bye"):
            voice.speak("Goodbye! Your tasks have been saved.")
            todos.save()
            memory.save()
            break

        response = agent.chat(user_text)
        print(f"\nAgent: {response}\n")
        voice.speak(response)


if __name__ == "__main__":
    main()
