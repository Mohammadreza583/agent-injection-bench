# Reading notes

Working notes for literature → episode design:

- Prefer **indirect** injections (document channel) over jailbreaks in the user turn.
- Keep **benign twins** so utility and ASR are not confounded by different tasks.
- Tag a minority of episodes with inspiration sources (`Greshake`, `InjecAgent`, …) while keeping payloads original.
- Scoring should be **mechanical** (tool name / substring), not LLM-as-judge, for v0 reproducibility.
- Defer defense ablations (PPL filter, sanitizer, tool allowlist, ADAPTI-GUARD) to the defense repo.
