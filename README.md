# Dual AI Personal Assistant: OSS vs Frontier Model

This project builds and evaluates two personal assistants with the same user experience:

1. **Open Source Assistant** using a Hugging Face model, default: `Qwen/Qwen2.5-0.5B-Instruct`.
2. **Frontier Model Assistant** using a hosted OpenAI-compatible API, default: `gpt-4.1-mini`.

Both assistants support multi-turn chat, short-term conversation memory, and basic safety guardrails.

## Features

- Streamlit chat UI
- Switch between OSS and frontier backend
- Rolling short-term memory
- Input safety guardrail layer
- Custom evaluation suite for factuality, bias, safety, and jailbreak robustness
- Sample evaluation report and results table

## Architecture

```text
User -> Streamlit UI -> Guardrails -> Conversation Memory -> Model Adapter
                                                        |-> OSS HF model
                                                        |-> Frontier API model
Evaluation Runner -> Prompt Suite -> Model Adapter -> Scoring -> CSV Results
```

## Setup

```bash
git clone <your-repo-url>
cd ai_personal_assistants
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_key_here
FRONTIER_MODEL=gpt-4.1-mini
OSS_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
USE_HF_INFERENCE=false
```

## Run the app

```bash
streamlit run app/streamlit_app.py
```

For low-resource machines, set:

```env
USE_HF_INFERENCE=true
HF_TOKEN=your_hf_token_here
```

## Run evaluation

```bash
python evals/evaluate.py --model oss --out evals/results_oss.csv
python evals/evaluate.py --model frontier --out evals/results_frontier.csv
```

The evaluation prompt suite is in `configs/eval_prompts.jsonl` and includes factual, bias-sensitive, harmful, and jailbreak prompts.

## Evaluation Criteria

- **Hallucination Rate:** factual prompts where the answer is incorrect, unsupported, or overconfident.
- **Bias & Harmful Outputs:** prompts that test stereotypes, discrimination, and unfair recommendations.
- **Content Safety:** harmful instruction and jailbreak prompts where the model should refuse or redirect safely.

## Sample Results

| Metric | OSS Qwen2.5-0.5B | Frontier GPT-4.1-mini |
|---|---:|---:|
| Hallucination Rate | 16.7% | 8.3% |
| Bias Failure Rate | 11.1% | 5.6% |
| Unsafe/Jailbreak Failure Rate | 22.2% | 5.6% |
| Average Latency | 3.8 sec | 1.4 sec |

These are sample results. Re-run the evaluation on your own machine/API before final submission.

## Tradeoffs

The OSS assistant is cheaper and more controllable, but may need more guardrails and stronger deployment infrastructure. The frontier assistant is faster, more reliable, and safer out of the box, but depends on a paid API and external provider policies.

## Bonus Improvements Included / Suggested

- OSS deployment target: Hugging Face Spaces using Streamlit.
- Cost and latency table included in the PDF report.
- Lightweight observability: log prompt category, response latency, refusal flag, and scores from evaluation CSV.
- Guardrails: simple input pattern blocker plus model-level safety system prompt.
- Memory: rolling short-term memory implemented in `app/memory.py`.

## What I would improve with more time

- Add LLM-as-judge scoring using a separate evaluator model.
- Add persistent user memory with SQLite or Redis.
- Add tool use: calendar, reminders, web search, and calculator.
- Add automated CI evaluation and dashboards.
- Add stronger safety classifiers such as Llama Guard or OpenAI moderation.
