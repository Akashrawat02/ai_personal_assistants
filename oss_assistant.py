from __future__ import annotations
import os
from typing import Dict, List
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import InferenceClient

class OSSAssistant:
    def __init__(self, model_id: str | None = None, use_hf_inference: bool | None = None):
        self.model_id = model_id or os.getenv("OSS_MODEL_ID", "Qwen/Qwen2.5-0.5B-Instruct")
        self.use_hf_inference = (os.getenv("USE_HF_INFERENCE", "false").lower() == "true") if use_hf_inference is None else use_hf_inference
        self.client = None
        self.pipe = None
        if self.use_hf_inference:
            self.client = InferenceClient(model=self.model_id, token=os.getenv("HF_TOKEN"))
        else:
            tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            model = AutoModelForCausalLM.from_pretrained(self.model_id, device_map="auto")
            self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    def chat(self, messages: List[Dict[str, str]], max_new_tokens: int = 256) -> str:
        if self.use_hf_inference:
            response = self.client.chat_completion(messages=messages, max_tokens=max_new_tokens, temperature=0.2)
            return response.choices[0].message.content
        prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages]) + "\nASSISTANT:"
        output = self.pipe(prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.2)[0]["generated_text"]
        return output.split("ASSISTANT:")[-1].strip()
