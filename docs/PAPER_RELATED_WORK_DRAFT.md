# Paper — related work draft

Indirect prompt injection demonstrates that untrusted retrieved content can override an LLM agent's goals and induce tool misuse (Greshake et al.). Recent agent benchmarks such as InjecAgent and AgentDojo stress tool-calling policies under adversarial instructions. Defense-oriented studies (including sanitization, detection, and tool filtering) typically require a stable attack corpus and utility baseline.

**agent-injection-bench** contributes a minimal, schema-frozen twin-episode suite (attack/benign) with offline tools and auditable traces, enabling reproducible ASR and utility measurement before defense comparison. Unlike large dynamic environments, v0 prioritizes transparency and scoring simplicity over coverage.
