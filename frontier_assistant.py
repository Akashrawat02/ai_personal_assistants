from __future__ import annotations
import os
from typing import Dict, List
from openai import OpenAI

class FrontierAssistant:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("FRONTIER_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 256) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
