# Cursor prompt: run eval

Paste into Cursor when you want a live evaluation pass:

```
Working directory: this agent-injection-bench repo.
1) Confirm .env has AIB_LLM_API_KEY (do not print the key).
2) Run: python scripts/validate_episodes.py
3) Run: python scripts/run_batch.py --split all
4) Run: python scripts/score_asr.py and python scripts/score_utility.py
5) Report N/successes/rate exactly as printed. If rate is null, say "no scored traces".
6) Do not invent numbers. Do not add defenses. Do not commit .env or traces.
```
