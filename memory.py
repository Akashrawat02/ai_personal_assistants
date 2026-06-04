from collections import deque
from typing import Deque, Dict, List

class ConversationMemory:
    """Short-term rolling conversation memory."""
    def __init__(self, max_turns: int = 8):
        self.messages: Deque[Dict[str, str]] = deque(maxlen=max_turns * 2)

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def get(self) -> List[Dict[str, str]]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()
