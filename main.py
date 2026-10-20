import json
import os
import random
import re
from datetime import datetime


class OfflineAI:
    def __init__(self, name="Nova", memory_file="memory.json", knowledge_file="knowledge.json"):
        self.name = name
        self.memory_file = memory_file
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_json(knowledge_file, {
            "name": name,
            "creator": "Unknown",
            "description": "A local offline AI assistant.",
            "skills": ["chat"],
            "facts": []
        })
        self.memory = self.load_json(memory_file, {"chat_history": []})

    def load_json(self, file_path, default):
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
            return default

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
            return default

    def save_json(self, file_path, obj):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

    def normalize(self, text):
        return re.sub(r"\s+", " ", text.strip().lower())

    def add_memory(self, user_input, assistant_reply):
        self.memory["chat_history"].append({
            "user": user_input,
            "assistant": assistant_reply,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        if len(self.memory["chat_history"]) > 100:
            self.memory["chat_history"] = self.memory["chat_history"][-100:]

        self.save_json(self.memory_file, self.memory)

    def clear_memory(self):
        self.memory = {"chat_history": []}
        self.save_json(self.memory_file, self.memory)

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def get_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def intro(self):
        return (
            f"Hello! I am {self.name}, your offline AI assistant. "
            "I work without internet, API keys, or cloud services. "
            "Type /help to see commands."
        )

    def help_text(self):
        return (
            "Commands:\n"
            "- /help: show this help\n"
            "- /memory: show recent conversation memory\n"
            "- /clear: clear memory\n"
            "- /save: save current chat memory\n"
            "- /exit: quit the app\n"
            "\n"
            "You can also just chat naturally."
        )

    def respond(self, user_input):
        text = user_input.strip()
        if not text:
            return "Please say something."

        normalized = self.normalize(text)

        if normalized in ["/exit", "exit", "quit", "bye", "goodbye"]:
            return "Goodbye! See you later."

        if normalized in ["/help", "help", "what can you do"]:
            return self.help_text()

        if normalized in ["/memory", "memory"]:
            if not self.memory["chat_history"]:
                return "I do not have any saved memory yet."
            recent = self.memory["chat_history"][-5:]
            lines = []
            for entry in recent:
                lines.append(f"You: {entry['user']}\nAI: {entry['assistant']}")
            return "\n\n".join(lines)

        if normalized in ["/clear", "clear memory"]:
            self.clear_memory()
            return "Conversation memory has been cleared."

        if normalized in ["/save", "save"]:
            self.save_json(self.memory_file, self.memory)
            return "Memory saved."

        if normalized in ["hello", "hi", "hey"]:
            return "Hello! How can I help you today?"

        if "your name" in normalized or "who are you" in normalized:
            return f"I am {self.name}, your offline AI assistant."

        if "time" in normalized:
            return f"The current time is {self.get_time()}."

        if "date" in normalized:
            return f"Today is {self.get_date()}."

        if "joke" in normalized:
            jokes = [
                "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
                "I used to be a programmer, but now I just code at night.",
                "Why do programmers prefer dark mode? Because light attracts bugs."
            ]
            return random.choice(jokes)

        if "offline" in normalized or "local" in normalized:
            return "Yes — I run entirely on your computer without internet, APIs, or cloud services."

        if "remember" in normalized:
            return "I can remember recent conversation history in my local memory file."

        if "what can you do" in normalized:
            skills = ", ".join(self.knowledge.get("skills", ["chat"]))
            return f"I can help with {skills}. I can also remember chat history and respond in a local offline environment."

        for fact in self.knowledge.get("facts", []):
            if fact.lower() in normalized or normalized in fact.lower():
                return fact

        if "thank" in normalized:
            return "You’re welcome. I’m here to help."

        if "how are you" in normalized:
            return "I’m doing well. Running locally and ready to help."

        return (
            f"I’m {self.name}, and I’m designed to help you locally. "
            "I can answer simple questions, remember chat, and be extended with your own rules."
        )


def main():
    ai = OfflineAI()

    print(ai.intro())
    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["/exit", "exit", "quit", "bye", "goodbye"]:
            print("AI: Goodbye! See you later.")
            break

        reply = ai.respond(user_input)
        print(f"AI: {reply}")

        ai.add_memory(user_input, reply)


if __name__ == "__main__":
    main()
