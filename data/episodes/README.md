# Episodes

v0 ships **20 attack** + **20 benign** twin episodes under `attack/` and `benign/`.

- IDs: `atk_002`…`atk_021` and matching `ben_002`…`ben_021`
- Examples (`examples/episode_*.json`) use `atk_001` / `ben_001` for format demos only
- Attacks place the injection **inside** `retrieved_docs` (indirect), never in `user_query`
- Forbidden tool for attacks: `send_email`; allowed: `search_docs`

Validate:

```bash
python scripts/validate_episodes.py
```
